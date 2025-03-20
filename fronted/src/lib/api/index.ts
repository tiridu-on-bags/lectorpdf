/**
 * @file index.ts
 * @description Punto de entrada centralizado para el módulo API de Gradio
 */

// Exportaciones principales
export * from './gradio-client';
export * from '$lib/api/types';
export * from '$lib/api/utils';

// Re-exportación de la creación de cliente con valores por defecto
import { GradioClient } from './gradio-client';
import type { GradioClientConfig } from '$lib/api/types';

/**
 * Crea una instancia del cliente Gradio con configuración predeterminada
 * @param config Configuración parcial para sobreescribir valores por defecto
 * @returns Instancia configurada del cliente Gradio
 */
export function createGradioClient(config: Partial<GradioClientConfig> = {}): GradioClient {
  return new GradioClient({
    baseUrl: import.meta.env.VITE_GRADIO_URL || 'http://localhost:7860',
    maxRetries: config.maxRetries ?? 3,
    initialDelay: config.initialDelay ?? 1000,
    timeout: config.timeout ?? 30000
  });
}