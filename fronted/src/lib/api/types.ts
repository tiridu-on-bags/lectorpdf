/**
 * @file types.ts
 * @description Definiciones de tipos para la integración SvelteKit-Gradio
 */

/**
 * Configuración del cliente Gradio
 */
export interface GradioClientConfig {
    /** URL base del servidor Gradio */
    baseUrl: string;
    /** Número máximo de reintentos para peticiones fallidas */
    maxRetries?: number;
    /** Tiempo de espera inicial entre reintentos (ms) */
    initialDelay?: number;
    /** Tiempo máximo de espera para peticiones (ms) */
    timeout?: number;
  }
  
  /**
   * Estructura de datos para entrada de predicción
   */
  export interface PredictionInput {
    /** Valor numérico para procesamiento */
    value: number;
    /** Texto opcional para contextualización */
    text?: string;
    /** Parámetros adicionales específicos del modelo */
    params?: Record<string, unknown>;
  }
  
  /**
   * Estructura de datos para resultado de predicción
   */
  export interface PredictionResult {
    /** Valor procesado por el modelo */
    processed_value: number;
    /** Texto de predicción generado */
    prediction: string;
    /** Métricas de confianza y rendimiento */
    metrics?: {
      confidence: number;
      processingTime: number;
    };
  }
  
  /**
   * Estructura de respuesta del servidor Gradio
   */
  export interface GradioResponse<T> {
    /** Array de datos en formato específico de Gradio */
    data: T[];
    /** Metadatos adicionales de la respuesta */
    [key: string]: unknown;
  }
  
  /**
   * Estructura de respuesta estandarizada del backend
   */
  export interface BackendResponse<T> {
    /** Indicador de éxito de la operación */
    success: boolean;
    /** Datos de resultado en caso de éxito */
    data?: T;
    /** Mensaje de error en caso de fallo */
    error?: string;
  }
  
  /**
   * Estado de conexión con el servidor
   */
  export interface ServerConnectionState {
    /** Indicador de conexión activa */
    isOnline: boolean;
    /** Timestamp de última verificación */
    lastCheck: number;
    /** Indicador de verificación en progreso */
    checkInProgress: boolean;
  }