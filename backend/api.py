from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
import os
import uuid
import shutil
from pydantic import BaseModel
from typing import List, Union, Any

# IMPORTANTE: Definir app ANTES de usar los decoradores
app = FastAPI()

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origen del frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["*"],
)

# Crear directorio para uploads si no existe
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Definir los modelos de datos
class FlexibleInput(BaseModel):
    data: List[Any]

class TextRequest(BaseModel):
    text: str
    document_id: str = None

class QuestionRequest(BaseModel):
    question: str
    context: str = None
    document_id: str = None

# Endpoint para resumir texto
@app.post("/api/summarize")
async def summarize_text(request: TextRequest):
    """
    Genera un resumen del texto proporcionado.
    """
    try:
        # Simulación - en producción llamaría a un LLM como OpenAI
        summary = f"Resumen del texto: {request.text[:50]}..."
        
        return {
            "summary": summary,
            "document_id": request.document_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resumir texto: {str(e)}")

# Endpoint para explicar texto
@app.post("/api/explain")
async def explain_text(request: TextRequest):
    """
    Genera una explicación para el texto seleccionado.
    """
    try:
        # Simulación - en producción llamaría a un LLM como OpenAI
        explanation = f"El texto '{request.text[:30]}...' se refiere a un concepto que..."
        
        return {
            "explanation": explanation,
            "document_id": request.document_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al explicar texto: {str(e)}")

# Endpoint para responder preguntas sobre texto seleccionado
@app.post("/api/ask-selected")
async def ask_about_text(request: QuestionRequest):
    """
    Responde a una pregunta sobre un texto específico seleccionado.
    """
    try:
        # Simulación - en producción usaría el contexto y llamaría a un LLM
        answer = f"Respuesta a '{request.question}' basada en el contexto seleccionado."
        
        return {
            "answer": answer,
            "document_id": request.document_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar pregunta: {str(e)}")

@app.post("/api/predict-flexible")
async def predict_flexible(input_data: FlexibleInput):
    # Implementación básica - ajusta según tus necesidades
    value = input_data.data[0] if len(input_data.data) > 0 else 0
    text = input_data.data[1] if len(input_data.data) > 1 else ""
    
    # Lógica de procesamiento aquí
    processed_value = value * 2  # Ejemplo simple
    
    return {
        "status": "success",
        "message": "Predicción realizada correctamente",
        "data": [processed_value, f"Procesado: {text}"]
    }

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

# Agregar handler específico para OPTIONS y HEAD
@app.options("/api/pdf-basic/{file_id}")
@app.head("/api/pdf-basic/{file_id}")
async def pdf_preflight(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    
    # Respuesta vacía con headers adecuados para OPTIONS/HEAD
    return Response(
        status_code=200,
        headers={
            "Content-Type": "application/pdf",
            "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
            "Access-Control-Allow-Origin": "*"
        }
    )
    
# Endpoint raíz
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de LectorPDF"}

# Si necesitas iniciar el servidor directamente con "python api.py"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)