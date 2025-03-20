/**
 * @file utils.ts
 * @description Utilidades para manipulación de datos y comunicación con Gradio
 */

import type { PredictionInput, PredictionResult } from './types';

/**
 * Genera una clave de caché basada en los parámetros de entrada
 * @param input Datos de entrada para predicción
 * @returns Clave única para caché
 */
export function generateCacheKey(input: PredictionInput): string {
  return `prediction:${input.value}:${input.text || ''}:${JSON.stringify(input.params || {})}`;
}

/**
 * Normaliza los datos de entrada antes de enviarlos a Gradio
 * @param input Datos de entrada crudos
 * @returns Datos normalizados
 */
export function normalizeInput(input: Partial<PredictionInput>): PredictionInput {
  return {
    value: input.value ?? 0,
    text: input.text || undefined,
    params: input.params || undefined
  };
}

/**
 * Formatea el resultado de la predicción para presentación
 * @param result Resultado de la predicción
 * @returns Resultado formateado para UI
 */
export function formatPredictionResult(result: PredictionResult): Record<string, string | number> {
  return {
    processedValue: result.processed_value,
    prediction: result.prediction,
    confidence: result.metrics?.confidence.toFixed(2) ?? 'N/A',
    processingTime: result.metrics?.processingTime 
      ? `${result.metrics.processingTime.toFixed(0)}ms` 
      : 'N/A'
  };
}

/**
 * Analiza errores de comunicación con Gradio
 * @param error Error capturado
 * @returns Mensaje de error amigable
 */
export function parseGradioError(error: unknown): string {
  if (error instanceof Error) {
    if (error.message.includes('timeout')) {
      return 'La conexión con el servidor Gradio ha excedido el tiempo de espera. Por favor, inténtelo de nuevo.';
    }
    
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      return 'No se puede conectar al servidor Gradio. Verifique que el servidor esté en ejecución.';
    }
    
    return error.message;
  }
  
  return 'Error desconocido en la comunicación con Gradio';
}