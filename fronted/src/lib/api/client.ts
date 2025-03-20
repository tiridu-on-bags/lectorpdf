// Configuración base
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:7860';
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // ms

/**
 * Implementación de retroceso exponencial para peticiones fallidas
 * @param fn - Función a ejecutar con reintentos
 * @param retries - Número máximo de reintentos
 * @param delay - Retraso inicial entre reintentos (ms)
 */
async function withRetry<T>(
  fn: () => Promise<T>,
  retries = MAX_RETRIES,
  delay = RETRY_DELAY
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (retries <= 0) throw error;
    
    // Retroceso exponencial
    await new Promise(resolve => setTimeout(resolve, delay));
    return withRetry(fn, retries - 1, delay * 2);
  }
}

/**
 * Interfaz para respuestas de Gradio
 */
interface GradioResponse<T> {
  data: T[];
  [key: string]: unknown;
}

/**
 * Interfaz para respuestas del backend
 */
interface BackendResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

/**
 * Realiza una petición a la API de Gradio
 * @param inputData - Datos a enviar a la API
 * @returns Promesa con el resultado de la predicción
 */
export async function fetchPrediction<T, R>(inputData: T): Promise<R> {
  return withRetry(async () => {
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
  });
}

/**
 * Verifica si el servidor de Gradio está en línea
 * @returns true si el servidor está disponible
 */
export async function checkServerStatus(): Promise<boolean> {
  try {
    // Implementación con retroceso exponencial
    return await withRetry(async () => {
      const response = await fetch(`${API_URL}/`, { 
        method: 'HEAD',
        // Evitar caché del navegador
        headers: { 'Cache-Control': 'no-cache' }
      });
      return response.ok;
    }, 1); // Solo un intento para verificación rápida
  } catch (error) {
    console.error('Error al verificar el estado del servidor:', 
      error instanceof Error ? error.message : String(error));
    return false;
  }
}