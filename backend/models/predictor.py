# Función principal de predicción/procesamiento
def predict_something(input_data):
    """
    Función principal de predicción/procesamiento
    
    Args:
        input_data: Los datos proporcionados por el frontend
        
    Returns:
        Resultados procesados
    """
    # Implementa tu lógica aquí
    # Por ejemplo:
    return { 
        "processed_value": input_data["value"] * 2,
        "prediction": "ejemplo"
    }  # Eliminado el punto extra que causaría error