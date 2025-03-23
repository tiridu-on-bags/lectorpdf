from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import shutil
from typing import Dict
from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import openai

class Question(BaseModel):
    question: str

app = FastAPI()

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear directorio para uploads si no existe
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Endpoint de prueba simple
@app.get("/test")
async def test():
    return {"message": "API funcionando correctamente"}

# Endpoint para verificar la salud del servicio
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Endpoint básico para subir PDF (simplificado)
@app.post("/api/upload-basic")
async def upload_basic(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    # Generar un nombre único para el archivo
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    
    # Guardar el archivo
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Procesar el PDF para RAG
        try:
            # Cargar PDF con PyPDFLoader
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            # Dividir en chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(pages)
            
            # Crear embeddings y vectorstore
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(chunks, embeddings)
            
            # Guardar vectorstore a disco
            vector_path = os.path.join(UPLOAD_DIR, file_id)
            vectorstore.save_local(vector_path)
            
            # Devolver respuesta
            return {
                "url": f"/api/pdf-basic/{file_id}",
                "document_id": file_id,
                "filename": file.filename,
                "chunks": len(chunks),
                "message": "PDF cargado y procesado exitosamente"
            }
        except Exception as e:
            raise HTTPException(status_code=500, 
                detail=f"Error al procesar el PDF: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {str(e)}")

# Endpoint para recuperar un PDF por ID
@app.get("/api/pdf-basic/{file_id}")
async def get_pdf_basic(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    
    return FileResponse(file_path, media_type="application/pdf")

# Endpoint para hacer preguntas sobre el PDF
@app.post("/api/ask/{document_id}")
async def ask_question(document_id: str, query: Question):
    vector_path = os.path.join(UPLOAD_DIR, document_id)
    
    if not os.path.exists(vector_path):
        raise HTTPException(status_code=404, 
            detail="Vectorstore no encontrado para este documento")
    
    try:
        # Cargar vectorstore
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(vector_path, embeddings)
        
        # Crear retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        
        # Obtener contextos relevantes
        contexts = retriever.get_relevant_documents(query.question)
        context_text = "\n\n".join([doc.page_content for doc in contexts])
        
        # Generar respuesta con OpenAI
        llm = OpenAI(temperature=0)
        prompt = f"""
        Basándote en el siguiente contexto extraído de un PDF, responde a la pregunta del usuario.
        Si la respuesta no se encuentra en el contexto, di "No tengo suficiente información para responder a esta pregunta."
        
        Contexto:
        {context_text}
        
        Pregunta: {query.question}
        
        Respuesta:
        """
        
        response = llm.predict(prompt)
        
        return {
            "answer": response,
            "document_id": document_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, 
            detail=f"Error al procesar la pregunta: {str(e)}")

# Endpoint raíz
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de LectorPDF"}


