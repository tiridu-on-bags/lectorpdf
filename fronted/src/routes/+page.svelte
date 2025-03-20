<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fetchPrediction } from '$lib/api/client';
  import { serverStatus, serverStatusMessage } from '$lib/stores/server-status';
  import { predictionCache } from '$lib/stores/prediction-cache';
  
  // Tipos y estado
  type InputData = {
    value: number;
    text?: string;
  };
  
  type ResultData = {
    processed_value: number;
    prediction: string;
  };
  
  let inputValue = 0;
  let inputText = '';
  let result: ResultData | null = null;
  let loading = false;
  let error = '';
  
  // Iniciar verificación periódica del servidor
  onMount(() => {
    serverStatus.check();
    serverStatus.startPeriodicCheck();
  });
  
  onDestroy(() => {
    serverStatus.stopPeriodicCheck();
  });
  
  async function handleSubmit() {
    if (!$serverStatus.isOnline) {
      const isOnline = await serverStatus.check();
      if (!isOnline) {
        error = "El servidor de Gradio no está en línea. Verifica que esté ejecutándose.";
        return;
      }
    }
    
    loading = true;
    error = '';
    
    try {
      const data: InputData = {
        value: inputValue,
        text: inputText || undefined
      };
      
      // Clave de caché basada en los inputs
      const cacheKey = `prediction:${inputValue}:${inputText}`;
      const cachedEntry = predictionCache.get<ResultData>(cacheKey);
      
      // Patrón stale-while-revalidate
      if (cachedEntry) {
        result = cachedEntry.data;
        
        // Si está obsoleto, revalidar en segundo plano
        if (cachedEntry.isStale) {
          fetchPrediction<InputData, ResultData>(data)
            .then(freshResult => {
              result = freshResult;
              predictionCache.set(cacheKey, freshResult);
            })
            .catch(console.error);
        }
      } else {
        // Sin caché, hacer petición normal
        result = await fetchPrediction<InputData, ResultData>(data);
        predictionCache.set(cacheKey, result);
      }
    } catch (err) {
      error = err instanceof Error ? err.message : 'Error desconocido';
      result = null;
    } finally {
      loading = false;
    }
  }
</script>

<!-- Resto del HTML se mantiene similar -->