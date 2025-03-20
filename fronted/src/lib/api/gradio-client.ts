/**
 * @file gradio-client.ts
 * @description Cliente para comunicación con API de Gradio
 */

import type { 
    GradioClientConfig, 
    GradioResponse, 
    BackendResponse,
    PredictionInput,
    PredictionResult
  } from '$lib/api/types';
  
  /**
   * Cliente para comunicación con servidor Gradio
   * Implementa patrón Repository para acceso a datos
   */
  export class GradioClient {
    private baseUrl: string;
    private maxRetries: number;
    private initialDelay: number;
    private timeout: number;
  
    /**
     * Constructor del cliente Gradio
     * @param config Configuración del cliente
     */
    constructor(config: GradioClientConfig) {
      this.baseUrl = config.baseUrl;
      this.maxRetries = config.maxRetries ?? 3;
      this.initialDelay = config.initialDelay ?? 1000;
      this.timeout = config.timeout ?? 30000;
    }
  
    /**
     * Realiza una petición con reintentos y retroceso exponencial
     * @param fn Función a ejecutar con reintentos
     * @returns Resultado de la función
     */
    private async withRetry<T>(fn: () => Promise<T>, retries = this.maxRetries): Promise<T> {
      try {
        return await Promise.race([
          fn(),
          new Promise<never>((_, reject) => 
            setTimeout(() => reject(new Error('Request timeout')), this.timeout)
          )
        ]);
      } catch (error) {
        if (retries <= 0) throw error;
        
        // Implementación de retroceso exponencial
        const delay = this.initialDelay * Math.pow(2, this.maxRetries - retries);
        await new Promise(resolve => setTimeout(resolve, delay));
        
        return this.withRetry(fn, retries - 1);
      }
    }
  
    /**
     * Realiza una predicción utilizando el servidor Gradio
     * @param endpoint Ruta del endpoint
     * @param data Datos para la predicción
     * @returns Resultado de la predicción
     */
    async predict<TInput, TOutput>(endpoint: string, data: TInput): Promise<TOutput> {
      return this.withRetry(async () => {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ data: [data] })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json() as GradioResponse<BackendResponse<TOutput>>;
        
        if (!result.data?.[0]) {
          throw new Error('Invalid response format from Gradio API');
        }
        
        const backendResponse = result.data[0];
        
        if (!backendResponse.success) {
          throw new Error(backendResponse.error || 'Unknown backend error');
        }
        
        return backendResponse.data as TOutput;
      });
    }
  
    /**
     * Verifica el estado de salud del servidor Gradio
     * @returns true si el servidor está disponible
     */
    async checkHealth(): Promise<boolean> {
        try {
          const response = await fetch(`${this.baseUrl}/health`, {
            method: 'GET',
            headers: { 
              'Accept': 'application/json',
              'Cache-Control': 'no-cache' 
            },
            signal: AbortSignal.timeout(5000)
          });
          
          return response.ok;
        } catch (error) {
          // Implementación de registro estructurado
          console.error('Error en verificación de salud del servidor Gradio:', 
            error instanceof Error ? error.message : String(error));
          return false;
        }
      }
  
    /**
     * Método de conveniencia para realizar predicciones estándar
     * @param input Datos de entrada para la predicción
     * @returns Resultado de la predicción
     */
    async predictModel(input: PredictionInput): Promise<PredictionResult> {
      return this.predict<PredictionInput, PredictionResult>('/api/predict', input);
    }
  }