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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["*"],
)

# Crear directorio para uploads si no existe
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Definir el modelo de datos después de app pero antes de usarlo
class FlexibleInput(BaseModel):
    data: List[Any]

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
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    
    # Configuraciones críticas para streaming de PDF
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        headers={
            "Accept-Ranges": "bytes",
            "Cache-Control": "public, max-age=3600"
        }
    )
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