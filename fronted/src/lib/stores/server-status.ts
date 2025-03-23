// src/lib/stores/server-status.ts
import { writable, derived } from 'svelte/store';

// Configuración consistente con cliente API
const API_CONFIG = {
  baseUrl: import.meta.env.VITE_GRADIO_API_URL || 'http://localhost:7860',
  healthEndpoint: '/api/health',
  checkInterval: 5000
};

// Interfaz para estado del servidor - patrón Value Object
interface ServerStatusState {
  isOnline: boolean;
  lastCheck: Date | null;
  error: string | null;
}

// Implementación del patrón Observer con Store
function createServerStatusStore() {
  // Estado inicial
  const initialState: ServerStatusState = {
    isOnline: false,
    lastCheck: null,
    error: null
  };

  const { subscribe, set, update } = writable<ServerStatusState>(initialState);

  // Verificación de estado - patrón Circuit Breaker
  async function checkServerStatus(): Promise<boolean> {
    try {
      // Petición con timeout - patrón Timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);
      
      const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.healthEndpoint}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);

      // Actualización del estado
      const isOnline = response.ok;
      update(state => ({
        ...state,
        isOnline,
        lastCheck: new Date(),
        error: isOnline ? null : `El servidor respondió con código: ${response.status}`
      }));
      
      return isOnline;
    } catch (error) {
      // Manejo de errores de red
      update(state => ({
        ...state,
        isOnline: false,
        lastCheck: new Date(),
        error: error instanceof Error ? error.message : 'Error de conexión desconocido'
      }));
      
      return false;
    }
  }

  // Gestión de ciclo de vida - patrón Lifecycle
  let intervalId: ReturnType<typeof setInterval> | null = null;

  function startMonitoring() {
    if (intervalId) return;
    
    // Verificación inmediata
    checkServerStatus();
    
    // Monitoreo periódico
    intervalId = setInterval(checkServerStatus, API_CONFIG.checkInterval);
  }

  function stopMonitoring() {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  }

  // Inicialización automática en cliente
  if (typeof window !== 'undefined') {
    startMonitoring();
  }

  // Interfaz pública del store
  return {
    subscribe,
    checkNow: checkServerStatus,
    startMonitoring,
    stopMonitoring,
    reset: () => set(initialState)
  };
}

// Exportación de store singleton
export const serverStatus = createServerStatusStore();

// Store derivado para mensajes de UI - patrón Decorator
export const serverStatusMessage = derived(
  serverStatus,
  $status => $status.isOnline 
    ? 'Conectado' 
    : $status.error ? `Desconectado: ${$status.error}` : 'Desconectado'
);