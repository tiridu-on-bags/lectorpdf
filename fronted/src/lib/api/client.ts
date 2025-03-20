// Cliente para comunicarse con el backend de Gradio

// URL base de la API de Gradio
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:7860';

// Definición de tipos para los datos
interface GradioResponse<T> {
  data: T[];
  [key: string]: unknown;
}

interface BackendResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

/**
 * Realiza una petición a la API de Gradio
 * @param inputData - Datos a enviar a la API
 * @returns Respuesta de la API
 */
export async function fetchPrediction<T, R>(inputData: T): Promise<R> {
  try {
    // Gradio espera los datos en un formato específico
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
    
    const gradioResult = await response.json() as GradioResponse<BackendResponse<R>>;
    
    // Verificar si la respuesta tiene el formato esperado
    if (gradioResult && Array.isArray(gradioResult.data) && gradioResult.data.length > 0) {
      const backendResponse = gradioResult.data[0];
      
      // Verificar si la operación fue exitosa según nuestra API
      if (backendResponse.success && backendResponse.data) {
        return backendResponse.data;
      } else {
        throw new Error(backendResponse.error || 'Error en el procesamiento del backend');
      }
    }
    
    throw new Error('Formato de respuesta inválido');
  } catch (error) {
    console.error('Error al comunicarse con la API:', 
      error instanceof Error ? error.message : String(error));
    throw error;
  }
}

/**
 * Verifica si el servidor de Gradio está en línea
 * @returns true si el servidor está disponible
 */
export async function checkServerStatus(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/`, { method: 'HEAD' });
    return response.ok;
  } catch (error) {
    console.error('Error al verificar el estado del servidor:', 
      error instanceof Error ? error.message : String(error));
    return false;
  }
}