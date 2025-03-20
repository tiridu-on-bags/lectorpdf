import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.predictor import predict_something

# Crear la aplicación FastAPI para mayor control
app = FastAPI()

# Configurar CORS para permitir solicitudes desde SvelteKit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, restringe esto a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API para ser consumida por el frontend
def create_api():
    # Definición de la función que procesará las solicitudes
    def process_input(input_data):
        try:
            result = predict_something(input_data)
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Crear la interfaz Gradio como API
    demo = gr.Interface(
        fn=process_input,
        inputs=gr.JSON(),
        outputs=gr.JSON(),
        title="API Backend",
        description="API interna - No es una interfaz de usuario"
    )
    
    # Montar Gradio en la aplicación FastAPI
    # Esto permitirá que Gradio gestione correctamente la ruta /api/predict
    gr.mount_gradio_app(app, demo, path="/")
    
    return app

# Función para ejecutar la aplicación
def start_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

# Ejecutar la API si este archivo es el punto de entrada
if __name__ == "__main__":
    create_api()  # Crea la API y la monta en FastAPI
    start_server()  # Inicia el servidor