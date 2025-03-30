# backend/app.py
import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

# Inicialización del Gateway API
app = FastAPI(title="ML Gateway API")


# Configuración CORS - crítico para comunicación cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # SvelteKit dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de health check - patrón Circuit Breaker
@app.get("/api/health")
async def health_check():
    """Endpoint para monitoring de estado del sistema"""
    return {
        "status": "ok",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

# Implementación del servicio ML - patrón Strategy
def predict_ml(value, text=None):
    """Función de predicción para interfaz Gradio y API REST"""
    # Lógica de procesamiento ML
    processed_value = float(value) * 1.5
    prediction = f"Predicción para valor {processed_value:.2f}"
    if text:
        prediction += f" con contexto: '{text}'"
    
    return {
        "status": "success",
        "data": [processed_value, prediction],
        "message": "Predicción completada"
    }

# Interfaz Gradio - patrón Facade para UI
with gr.Blocks() as demo:
    gr.Markdown("# API de Predicción ML")
    with gr.Row():
        with gr.Column():
            num_input = gr.Number(label="Valor numérico")
            text_input = gr.Textbox(label="Texto contextual (opcional)")
            btn = gr.Button("Predecir")
        with gr.Column():
            output = gr.JSON()
    
    btn.click(
        fn=predict_ml,
        inputs=[num_input, text_input],
        outputs=output
    )

# Integración del REST API - patrón Command
@app.post("/api/predict")
async def predict_api(input_data: dict):
    """Endpoint REST para procesamiento de predicciones"""
    try:
        # Validación y extracción de parámetros
        if "data" not in input_data or not isinstance(input_data["data"], list):
            return {"status": "error", "message": "Formato inválido"}
        
        data = input_data["data"]
        value = float(data[0]) if data and len(data) > 0 else 0
        text = data[1] if len(data) > 1 else None
        
        # Utiliza la misma función de predicción que Gradio
        return predict_ml(value, text)
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Montaje de Gradio en FastAPI - patrón Adapter
app = gr.mount_gradio_app(app, demo, path="/gradio")

# Punto de entrada para desarrollo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)