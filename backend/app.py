# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time
from pdf_routes import router as pdf_router
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialización del Gateway API
app = FastAPI(title="PDF Processing API")

# Configuración CORS más permisiva para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear directorio de uploads si no existe
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Montar el directorio de uploads como archivos estáticos
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Registrar las rutas de PDF con el prefijo /api
app.include_router(pdf_router, prefix="/api", tags=["pdf"])

@app.get("/")
async def root():
    """Root endpoint para verificar que el servidor está funcionando"""
    logger.info("Root endpoint called")
    return {
        "status": "ok",
        "message": "Bienvenido a la API de Procesamiento de PDF",
        "endpoints": {
            "upload": "/api/upload-pdf",
            "health": "/api/health",
            "get_pdf": "/api/pdf/{file_id}",
            "ask": "/api/ask/{document_id}"
        }
    }

@app.get("/api/health")
async def health_check():
    """Endpoint para monitoring de estado del sistema"""
    logger.info("Health check endpoint called")
    return {
        "status": "ok",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")