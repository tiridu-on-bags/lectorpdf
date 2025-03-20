# backend/app.py
import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de desarrollo de SvelteKit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Función de predicción
def predict(value, text=None):
    # Lógica de procesamiento
    processed_value = value * 2
    prediction = f"Predicción para {value}" + (f" con texto: {text}" if text else "")
    
    return {
        "success": True,
        "data": {
            "processed_value": processed_value,
            "prediction": prediction
        }
    }

# Definición de la interfaz Gradio
with gr.Blocks() as demo:
    gr.Interface(
        fn=predict,
        inputs=[gr.Number(label="Valor"), gr.Textbox(label="Texto opcional")],
        outputs=gr.JSON(),
        title="API de Predicción"
    )

# Montaje de la interfaz Gradio en FastAPI
app = gr.mount_gradio_app(app, demo, path="/")

# Ejecución con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)