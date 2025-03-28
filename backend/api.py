from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import shutil

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
    
    return FileResponse(file_path, media_type="application/pdf")

# Endpoint raíz
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de LectorPDF"}