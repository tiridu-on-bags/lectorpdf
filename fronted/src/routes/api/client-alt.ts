// src/routes/api/client-alt.ts
// Cliente alternativo simplificado usando fetch directamente

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Función simplificada para realizar peticiones al backend 
 * usando la estructura exacta que sabemos que funciona con curl
 */
export async function predictValue(value: number, text: string = ""): Promise<any> {
  try {
    // Convertir a tipos exactos como los que funcionan con curl
    const numValue = parseFloat(value.toString());
    const strText = text.toString();
    
    // Usar exactamente la misma estructura que curl
    const payload = {
      data: [numValue, strText]
    };
    
    console.log('Enviando datos:', JSON.stringify(payload));
    
    // Añadir timestamp para evitar caché
    const response = await fetch(`${API_URL}/api/predict?t=${Date.now()}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Error ${response.status}: ${errorText}`);
      throw new Error(`Error: ${response.statusText}`);
    }
    
    const result = await response.json();
    console.log('Respuesta:', result);
    
    return {
      success: true,
      value: result.data[0],
      text: result.data[1],
      raw: result
    };
    
  } catch (error) {
    console.error('Error en petición:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Error desconocido'
    };
  }
}

/**
 * Función simple para comprobar si el servidor está disponible
 */
export async function checkServerStatus(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/api/health?t=${Date.now()}`);
    return response.ok;
  } catch {
    return false;
  }
} 