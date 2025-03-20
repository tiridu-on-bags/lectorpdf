// src/lib/api/client.ts
import { serverStatus } from '$lib/stores/server-status';
import { get } from 'svelte/store';

// Configuración de la API
const API_URL = import.meta.env.VITE_GRADIO_API_URL || 'http://localhost:7860/api';

// Interfaz para los parámetros de predicción
interface PredictionParams {
  value: number;
  text?: string;
}

// Función para realizar la petición de predicción
export async function fetchPrediction(params: PredictionParams) {
  // Comprobar si el servidor está online
  const isServerOnline = get(serverStatus).isOnline;
  if (!isServerOnline) {
    // Si no está en línea, intentar comprobar una vez más
    const nowOnline = await serverStatus.checkNow();
    if (!nowOnline) {
      throw new Error('El servidor no está disponible. Por favor, verifica la conexión.');
    }
  }

  try {
    // Estructura correcta según la expectativa de la API FastAPI
    const requestBody = {
      data: [
        params.value,
        params.text || ''
      ]
    };

    console.log('Enviando petición:', requestBody);
    
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error en respuesta:', response.status, errorText);
      throw new Error(`Error en la solicitud: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    
    // Verificar la estructura esperada de la respuesta
    if (!data || !data.data) {
      throw new Error('Respuesta del servidor inválida');
    }

    // Procesar y devolver la respuesta estructurada
    return {
      processed_value: parseFloat(data.data[0]) || 0,
      prediction: data.data[1] || 'Sin predicción',
      raw_response: data
    };
  } catch (error) {
    console.error('Error al realizar la predicción:', error);
    throw error instanceof Error 
      ? error 
      : new Error('Error desconocido al procesar la solicitud');
  }
}