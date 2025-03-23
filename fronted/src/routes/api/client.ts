// src/routes/api/client.ts
// Configuración correcta de la API utilizando la variable de entorno adecuada
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:7860';

// Interfaz para los parámetros de predicción
interface PredictionParams {
  value: number;
  text?: string;
}

// Solución directa - Enviar datos exactamente como espera el backend
export async function fetchPrediction(params: PredictionParams) {
  try {
    // Verificar estado del servidor primero
    const response = await fetch(`${API_URL}/api/health`);
    if (!response.ok) {
      throw new Error('El servidor no está disponible');
    }
    
    // Usar el formato exacto que funciona con curl
    const payload = JSON.stringify({
      data: [
        Number(params.value), // Asegurar que es un número
        String(params.text || "") // Asegurar que es un string
      ]
    });
    
    console.log('Enviando datos:', payload);
    
    // Petición simplificada - USAR ENDPOINT FLEXIBLE que sabemos que funciona
    const fetchResponse = await fetch(`${API_URL}/api/predict-flexible`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: payload
    });
    
    // Manejar errores con más detalle
    if (!fetchResponse.ok) {
      const errorText = await fetchResponse.text();
      console.error('Error en respuesta:', fetchResponse.status, errorText);
      throw new Error(`Error ${fetchResponse.status}: ${errorText}`);
    }
    
    // Procesar la respuesta
    const data = await fetchResponse.json();
    console.log('Respuesta recibida:', data);
    
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
      : new Error('Error desconocido al procesar la solicitud');
  }
}