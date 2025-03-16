// Cliente para comunicarse con el backend de Gradio

// URL base de la API de Gradio
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:7860';

// Definición de tipos para los datos
interface GradioResponse<T> {
  data: T[];
  [key: string]: unknown;
}

/**
 * Realiza una petición a la API de Gradio
 * @param inputData - Datos a enviar a la API
 * @returns Respuesta de la API
 */
export async function fetchPrediction<T, R>(inputData: T): Promise<R> {
  try {
    const response = await fetch(`${API_URL}/api/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ data: [inputData] })
    });
    
    if (!response.ok) {
      throw new Error(`Error en la petición: ${response.status}`);
    }
    
    const result = await response.json() as GradioResponse<R>;
    
    // Gradio devuelve { data: [...] } donde el primer elemento es nuestro resultado
    if (result && Array.isArray(result.data) && result.data.length > 0) {
      return result.data[0];
    }
    
    throw new Error('Formato de respuesta inválido');
  } catch (error) {
    console.error('Error al comunicarse con la API:', 
      error instanceof Error ? error.message : String(error));
    throw error;
  }
}