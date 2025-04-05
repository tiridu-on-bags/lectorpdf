from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import shutil
from pydantic import BaseModel

class Question(BaseModel):
    question: str

app = FastAPI()

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origen específico del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear directorio para uploads si no existe
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        
        return {
            "url": f"/api/pdf-basic/{file_id}",
            "document_id": file_id,
            "filename": file.filename,
            "message": "PDF cargado exitosamente"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {str(e)}")

# Endpoint para recuperar un PDF por ID
@app.get("/api/pdf-basic/{file_id}")
async def get_pdf_basic(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    
    print(f"Solicitando archivo: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Archivo no encontrado: {file_path}")
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    
    try:
        return FileResponse(
            path=file_path, 
            media_type="application/pdf",
            filename=f"{file_id}.pdf"
        )
    except Exception as e:
        print(f"Error al servir el archivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al servir el archivo: {str(e)}")

# Endpoint simplificado para preguntas
@app.post("/api/ask/{document_id}")
async def ask_question(document_id: str, query: Question):
    file_path = os.path.join(UPLOAD_DIR, f"{document_id}.pdf")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    
    # Respuesta simulada
    responses = {
        "título": f"Este documento se titula 'Documento PDF {document_id}'",
        "autor": "El autor de este documento es Jonathan",
        "fecha": "Este documento fue creado recientemente",
        "contenido": "Este documento trata sobre arquitectura de software y patrones de diseño MVC"
    }
    
    # Buscar una palabra clave simple en la pregunta
    for keyword, response in responses.items():
        if keyword in query.question.lower():
            return {"answer": response, "document_id": document_id}
    
    return {
        "answer": "No tengo suficiente información para responder a esta pregunta específica. ¿Podrías reformularla?",
        "document_id": document_id
    }

# Endpoint raíz
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de LectorPDF"} 