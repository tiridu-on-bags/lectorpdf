// src/lib/stores/prediction-cache.ts
import { writable, get } from 'svelte/store';

/**
 * Interfaz para entradas en la caché
 */
export interface CacheEntry<T> {
  data: T;
  timestamp: number;
  isStale: boolean;
}

// Tiempo de expiración de la caché: 5 minutos
const CACHE_TTL = 5 * 60 * 1000;

/**
 * Store reactivo para cachear resultados de predicciones
 * Implementa el patrón Stale-While-Revalidate para mejorar rendimiento
 */
function createPredictionCache<T>() {
  const cache = writable<Map<string, CacheEntry<T>>>(new Map());
  
  return {
    subscribe: cache.subscribe,
    
    /**
     * Obtiene una entrada de caché y verifica su frescura
     */
    get(key: string): CacheEntry<T> | undefined {
      const cacheMap = get(cache);
      const entry = cacheMap.get(key);
      
      if (entry) {
        // Marcar como obsoleto si ha pasado el TTL
        const isStale = Date.now() - entry.timestamp > CACHE_TTL;
        if (isStale && !entry.isStale) {
          entry.isStale = true;
          cache.update(map => {
            map.set(key, entry);
            return map;
          });
        }
      }
      
      return entry;
    },
    
    /**
     * Almacena un resultado de predicción en caché
     */
    set(key: string, data: T) {
      cache.update(map => {
        map.set(key, {
          data,
          timestamp: Date.now(),
          isStale: false
        });
        return map;
      });
    },
    
    /**
     * Invalida una entrada de caché
     */
    invalidate(key: string) {
      cache.update(map => {
        map.delete(key);
        return map;
      });
    },
    
    /**
     * Limpia toda la caché
     */
    clear() {
      cache.set(new Map());
    }
  };
}

export const predictionCache = createPredictionCache<unknown>();