import gradio as gr
from models.predictor import predict_something

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
    
    # Configuración importante para permitir solicitudes desde SvelteKit
    demo.launch(
        server_name="0.0.0.0",  # Permite conexiones externas
        server_port=7860,       # Puerto estándar de Gradio
        share=False,            # No compartir públicamente
        enable_cors=True,       # Crítico para permitir peticiones desde SvelteKit
    )
    
    return demo

# Ejecutar la API si este archivo es el punto de entrada
if __name__ == "__main__":
    create_api()