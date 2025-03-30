// flexible-client.ts - Cliente optimizado para el endpoint flexible

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'; //Puerto 8000 configuarado en el backend

// Interfaz para parámetros
export interface PredictionParams {
  value: number;
  text?: string;
}

// Interfaz para la respuesta API original
interface ApiResponse {
  status: string;
  data: [number, string];
  message: string;
  [key: string]: unknown;
}

// Interfaz para respuesta
export interface PredictionResult {
  processed_value: number;
  prediction: string;
  status: string;
  message: string;
  raw_response: ApiResponse;
}

/**
 * Cliente simplificado para el endpoint flexible
 */
export async function predictWithFlexibleAPI(params: PredictionParams): Promise<PredictionResult> {
  try {
    // Verificar si el servidor está disponible
    const healthCheck = await fetch(`${API_URL}/api/health`);
    if (!healthCheck.ok) {
      throw new Error('El servidor no está disponible');
    }
    
    // Formatear los datos como se espera
    const payload = {
      data: [
        Number(params.value),
        String(params.text || "")
      ]
    };
    
    console.log('Enviando datos al API flexible:', JSON.stringify(payload));
    
    // Hacer la petición al endpoint flexible
    const response = await fetch(`${API_URL}/api/predict-flexible`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error API:', response.status, errorText);
      throw new Error(`Error ${response.status}: ${errorText}`);
    }
    
    const data = await response.json() as ApiResponse;
    console.log('Respuesta API:', data);
    
    // Transformar los datos al formato esperado por la aplicación
    return {
      processed_value: data.data[0],
      prediction: data.data[1],
      status: data.status,
      message: data.message,
      raw_response: data
    };
  } catch (error) {
    console.error('Error:', error);
    throw error instanceof Error 
      ? error 
      : new Error('Error desconocido');
  }
}

/**
 * Verificar disponibilidad del servidor
 */
export async function isServerAvailable(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/api/health`);
    return response.ok;
  } catch {
    return false;
  }
} 