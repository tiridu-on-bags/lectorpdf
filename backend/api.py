# Modificación para backend/api.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Union, Optional
from pydantic import BaseModel
import time
import json

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="SvelteKit-Gradio Integration API",
    description="API Gateway para integración de componentes ML",
    version="1.0.0"
)

# Configuración CORS para comunicación cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restringir en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos para validación y documentación
class PredictionInput(BaseModel):
    data: List[Union[float, str, None]]

class PredictionResponse(BaseModel):
    status: str
    data: List[Union[float, str]]
    message: str

# Simulador de ML para desarrollo inicial
class MLPredictor:
    """Implementación del patrón Strategy para procesamiento ML."""
    
    def process_value(self, value: float) -> float:
        """Aplica transformación al valor de entrada."""
        return value * 1.5
    
    def predict(self, value: float, text: Optional[str] = None) -> str:
        """Genera predicción basada en inputs procesados."""
        base_prediction = f"Predicción para valor {value:.2f}"
        if text and len(text.strip()) > 0:
            return f"{base_prediction} con contexto: '{text}'"
        return base_prediction

# Inicialización del predictor como singleton
predictor = MLPredictor()

@app.get("/api/health", summary="Verificación de estado del sistema")
async def health_check() -> Dict[str, Any]:
    """
    Endpoint de health-check para supervisión del sistema.
    
    Implementa el patrón Circuit Breaker para detección de fallos.
    """
    return {
        "status": "ok",
        "message": "API Gateway operativo",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.post("/api/predict", response_model=PredictionResponse, 
          summary="Procesamiento de predicciones ML")
async def predict(input_data: PredictionInput) -> Dict[str, Any]:
    """
    Endpoint para procesamiento de predicciones ML.
    
    Implementa el patrón Command para encapsular solicitudes como objetos.
    """
    try:
        if not input_data.data or len(input_data.data) < 1:
            raise HTTPException(
                status_code=400, 
                detail="Se requiere al menos un valor numérico"
            )
        
        # Extracción y validación de parámetros
        numeric_value = float(input_data.data[0])
        text_value = input_data.data[1] if len(input_data.data) > 1 else ""
        
        # Procesamiento ML utilizando el patrón Strategy
        processed_value = predictor.process_value(numeric_value)
        prediction = predictor.predict(processed_value, text_value)
        
        # Respuesta estructurada
        return {
            "status": "success",
            "data": [processed_value, prediction],
            "message": "Predicción completada"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error de formato en los parámetros: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el procesamiento ML: {str(e)}"
        )

# Endpoint alternativo para mayor flexibilidad
@app.post("/api/predict-flexible")
async def predict_flexible(request: Request) -> Dict[str, Any]:
    """
    Endpoint flexible que acepta diferentes formatos de entrada.
    
    Implementa el patrón Adapter para normalizar diferentes estructuras de datos.
    """
    try:
        # Obtener el cuerpo de la petición como diccionario
        request_data = await request.json()
        
        # Lógica de adaptación para diferentes formatos
        numeric_value = None
        text_value = ""
        
        # Caso 1: Estructura esperada con 'data' como array
        if isinstance(request_data, dict) and 'data' in request_data and isinstance(request_data['data'], list):
            if len(request_data['data']) > 0:
                numeric_value = float(request_data['data'][0])
            if len(request_data['data']) > 1:
                text_value = request_data['data'][1] or ""
        
        # Caso 2: Estructura directa con propiedades 'value' y 'text'
        elif isinstance(request_data, dict) and 'value' in request_data:
            numeric_value = float(request_data['value'])
            text_value = request_data.get('text', '')
        
        # Caso 3: Objeto simple con valor numérico
        elif isinstance(request_data, (int, float)):
            numeric_value = float(request_data)
        
        # Validación final
        if numeric_value is None:
            raise HTTPException(
                status_code=400,
                detail="No se pudo extraer un valor numérico de la petición"
            )
        
        # Procesamiento ML
        processed_value = predictor.process_value(numeric_value)
        prediction = predictor.predict(processed_value, text_value)
        
        # Respuesta estructurada
        return {
            "status": "success",
            "data": [processed_value, prediction],
            "message": "Predicción completada"
        }
    
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Error al decodificar JSON"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error de formato en los parámetros: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el procesamiento: {str(e)}"
        )

# Punto de entrada para servidor Uvicorn cuando se ejecuta directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=7860, reload=True)