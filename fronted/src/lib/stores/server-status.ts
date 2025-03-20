// src/lib/stores/server-status.ts
import { writable, derived } from 'svelte/store';

// Configuración de la API
const API_URL = import.meta.env.VITE_GRADIO_API_URL || 'http://localhost:7860/api';
const HEALTH_CHECK_INTERVAL = 5000; // Intervalo de comprobación en ms

// Interfaz para el estado del servidor
interface ServerStatusState {
  isOnline: boolean;
  lastCheck: Date | null;
  error: string | null;
}

// Estado inicial
const initialState: ServerStatusState = {
  isOnline: false,
  lastCheck: null,
  error: null
};

// Crear el store para el estado del servidor
function createServerStatusStore() {
  const { subscribe, set, update } = writable<ServerStatusState>(initialState);

  // Función para comprobar el estado del servidor
  async function checkServerStatus() {
    try {
      // Intentar realizar una petición al endpoint de salud del servidor
      const response = await fetch(`${API_URL}/health`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        // Timeout para evitar esperas largas si el servidor no responde
        signal: AbortSignal.timeout(3000)
      });

      if (response.ok) {
        update(state => ({
          ...state,
          isOnline: true,
          lastCheck: new Date(),
          error: null
        }));
        return true;
      } else {
        throw new Error(`El servidor respondió con código: ${response.status}`);
      }
    } catch (error) {
      update(state => ({
        ...state,
        isOnline: false,
        lastCheck: new Date(),
        error: error instanceof Error ? error.message : 'Error de conexión desconocido'
      }));
      return false;
    }
  }

  // Función para iniciar el intervalo de comprobación del estado
  let intervalId: ReturnType<typeof setInterval> | null = null;

  function startMonitoring() {
    if (intervalId) return; // Evitar iniciar múltiples intervalos
    
    // Comprobar inmediatamente al iniciar
    checkServerStatus();
    
    // Establecer el intervalo para comprobaciones periódicas
    intervalId = setInterval(checkServerStatus, HEALTH_CHECK_INTERVAL);
  }

  function stopMonitoring() {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  }

  // Iniciar monitoreo automáticamente en el cliente (no en SSR)
  if (typeof window !== 'undefined') {
    startMonitoring();
  }

  return {
    subscribe,
    checkNow: checkServerStatus,
    startMonitoring,
    stopMonitoring,
    reset: () => set(initialState)
  };
}

// Exportar la instancia del store
export const serverStatus = createServerStatusStore();

// Store derivado para mensajes de estado amigables
export const serverStatusMessage = derived(
  serverStatus,
  $serverStatus => {
    if ($serverStatus.isOnline) {
      return 'Conectado';
    } else {
      return $serverStatus.error ? `Desconectado: ${$serverStatus.error}` : 'Desconectado';
    }
  }
);