# backend/pdf_routes.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
import os
import uuid
import shutil
import fitz  # PyMuPDF
from typing import List, Dict, Any
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

UPLOAD_DIR = "uploads"
VECTOR_DIR = "vector_db"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

# Diccionario para mantener seguimiento de los vectorstores de cada PDF
pdf_indexes = {}

@router.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    # Generar un nombre único para el archivo
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    
    # Guardar el archivo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extraer información básica y texto
    try:
        # Información básica con PyMuPDF (fitz)
        doc = fitz.open(file_path)
        info = {
            "pages": len(doc),
            "title": doc.metadata.get("title", "Sin título"),
            "author": doc.metadata.get("author", "Desconocido"),
        }
        
        # Extracción de texto completo
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            full_text += page.get_text()
        doc.close()
        
        # Crear chunks y embeddings para RAG
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(full_text)
        
        # Crear vectorstore
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(chunks, embeddings)
        
        # Guardar referencia al vectorstore
        pdf_indexes[file_id] = vectorstore
        
        # Guardar el vectorstore a disco (opcional)
        vectorstore.save_local(os.path.join(VECTOR_DIR, file_id))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")
    
    # Devolver la URL para acceder al PDF y la información extraída
    return {
        "url": f"/api/pdf/{file_id}",
        "document_id": file_id,
        "info": info,
        "text_length": len(full_text),
        "chunks": len(chunks),
        "message": "PDF cargado y procesado exitosamente"
    }

@router.get("/api/pdf/{file_id}")
async def get_pdf(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    
    return FileResponse(file_path, media_type="application/pdf")

@router.post("/api/ask/{document_id}")
async def ask_question(document_id: str, query: Dict[str, str]):
    if document_id not in pdf_indexes:
        # Intentar cargar desde disco si existe
        vector_path = os.path.join(VECTOR_DIR, document_id)
        if os.path.exists(vector_path):
            embeddings = OpenAIEmbeddings()
            pdf_indexes[document_id] = FAISS.load_local(vector_path, embeddings)
        else:
            raise HTTPException(status_code=404, detail="Documento no encontrado o no procesado")
    
    try:
        # Obtener el vectorstore
        vectorstore = pdf_indexes[document_id]
        
        # Crear cadena de recuperación
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        
        # Realizar búsqueda de contextos relevantes
        question = query.get("question", "")
        contexts = retriever.get_relevant_documents(question)
        
        # Formatear contextos para el prompt
        context_text = "\n\n".join([doc.page_content for doc in contexts])
        
        # Generar respuesta con el LLM
        llm = OpenAI(temperature=0)
        prompt = f"""
        Basándote en el siguiente contexto extraído de un PDF, responde a la pregunta del usuario.
        Si la respuesta no se encuentra en el contexto, di "No tengo suficiente información para responder a esta pregunta."
        
        Contexto:
        {context_text}
        
        Pregunta: {question}
        
        Respuesta:
        """
        
        response = llm.predict(prompt)
        
        return {
            "answer": response,
            "contexts": [doc.page_content for doc in contexts],
            "document_id": document_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la pregunta: {str(e)}")