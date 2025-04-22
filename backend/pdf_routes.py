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
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import logging
from pydantic import BaseModel

# Modelo para solicitudes de texto seleccionado
class SelectedTextRequest(BaseModel):
    text: str
    document_id: str = ""

# Modelo para preguntas sobre texto seleccionado
class QuestionRequest(BaseModel):
    text: str
    question: str
    document_id: str = ""

logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Quitar el prefijo /api del router ya que app.py lo maneja
router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
VECTOR_DIR = "vector_db"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

# Diccionario para mantener seguimiento de los vectorstores de cada PDF
pdf_indexes = {}

@router.post("/upload-pdf", response_model=dict)
async def upload_pdf(file: UploadFile = File(...)):
    logger.info(f"Recibiendo archivo: {file.filename}")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    try:
        # Generar un nombre único para el archivo
        file_id = str(uuid.uuid4())
        file_name = f"{file_id}.pdf"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        logger.info(f"Guardando archivo en: {file_path}")
        
        # Guardar el archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Archivo guardado exitosamente: {file_path}")
        
        # Retornar la URL del archivo
        return {
            "url": f"/uploads/{file_name}",
            "document_id": file_id,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error al procesar el archivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

@router.get("/pdf/{file_id}")
async def get_pdf(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    
    return FileResponse(file_path, media_type="application/pdf")

@router.post("/ask/{document_id}")
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

# Nuevos endpoints para el Lápiz Inteligente Contextual

@router.post("/summarize")
async def summarize_text(request: SelectedTextRequest):
    """Genera un resumen del texto seleccionado por el usuario."""
    try:
        logger.info(f"Solicitando resumen de texto de {len(request.text)} caracteres")
        
        # LLM para resumir
        llm = OpenAI(temperature=0.3)
        prompt = f"""
        Resume el siguiente texto de forma concisa, manteniendo las ideas clave:
        
        {request.text}
        
        Resumen:
        """
        
        summary = llm.predict(prompt)
        
        return {
            "summary": summary,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error al resumir texto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al resumir texto: {str(e)}")

@router.post("/explain")
async def explain_text(request: SelectedTextRequest):
    """Proporciona una explicación del texto seleccionado."""
    try:
        logger.info(f"Solicitando explicación de texto de {len(request.text)} caracteres")
        
        # LLM para explicación
        llm = OpenAI(temperature=0.3)
        prompt = f"""
        Explica el siguiente texto o concepto de manera clara y sencilla:
        
        {request.text}
        
        Explicación:
        """
        
        explanation = llm.predict(prompt)
        
        return {
            "explanation": explanation,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error al explicar texto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al explicar texto: {str(e)}")

@router.post("/ask-selected")
async def ask_about_selected(request: QuestionRequest):
    """Responde preguntas específicas sobre el texto seleccionado."""
    try:
        logger.info(f"Respondiendo pregunta sobre texto seleccionado")
        
        # LLM para responder preguntas sobre texto seleccionado
        llm = OpenAI(temperature=0.3)
        prompt = f"""
        Basándote únicamente en el siguiente texto, responde a la pregunta del usuario.
        Si la respuesta no se encuentra en el texto, di "No puedo responder a esta pregunta basándome solo en el texto seleccionado."
        
        Texto seleccionado:
        {request.text}
        
        Pregunta: {request.question}
        
        Respuesta:
        """
        
        answer = llm.predict(prompt)
        
        return {
            "answer": answer,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error al responder pregunta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al responder pregunta: {str(e)}")