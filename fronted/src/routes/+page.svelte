<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fetchPrediction } from '$lib/api/client';
  import { serverStatus, serverStatusMessage } from '$lib/stores/server-status';
  import { predictionCache } from '$lib/stores/prediction-cache';
  
  // Definición correcta del tipo ResultData
  interface ResultData {
    processed_value: number;
    prediction: string;
    [key: string]: any; // Para campos adicionales
  }
  
  let inputValue = 0;
  let inputText = '';
  let result: ResultData | null = null; // Inicializado como null para evitar el error TS2739
  let loading = false;
  let error = '';
  
  async function handleSubmit() {
    loading = true;
    error = '';
    try {
      const response = await fetchPrediction({ value: inputValue, text: inputText });
      result = response as ResultData; // Aseguramos que sea del tipo ResultData
      predictionCache.set(`${inputValue}-${inputText}`, response);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Error desconocido';
    } finally {
      loading = false;
    }
  }

  // Si necesitas realizar acciones al montar/desmontar el componente
  onMount(() => {
    // Código que se ejecuta al montar el componente
  });

  onDestroy(() => {
    // Código que se ejecuta al desmontar el componente
  });
</script>


<!-- Capa de presentación -->
<div class="container mx-auto p-6 max-w-4xl">
  <h1 class="text-3xl font-bold mb-6">Integración SvelteKit-Gradio</h1>
  
  <!-- Indicador de estado del servidor -->
  <div class="mb-6 p-3 rounded bg-gray-100 flex items-center justify-between">
    <span>Estado del servidor:</span>
    <span class={$serverStatus.isOnline ? "text-green-600 font-medium" : "text-red-600 font-medium"}>
      {$serverStatusMessage}
    </span>
  </div>
  
  <!-- Formulario de entrada -->
  <div class="bg-white shadow rounded-lg p-6 mb-6">
    <div class="space-y-4">
      <div>
        <label for="valueInput" class="block text-sm font-medium text-gray-700 mb-1">
          Valor numérico:
        </label>
        <input
          id="valueInput"
          type="number" 
          bind:value={inputValue}
          class="w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      <div>
        <label for="textInput" class="block text-sm font-medium text-gray-700 mb-1">
          Texto (opcional):
        </label>
        <input
          id="textInput"
          type="text" 
          bind:value={inputText}
          class="w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      <button 
        on:click={handleSubmit}
        disabled={loading || !$serverStatus.isOnline}
        class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {loading ? 'Procesando...' : 'Enviar a Gradio'}
      </button>
    </div>
  </div>
  
  <!-- Mensaje de error -->
  {#if error}
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
      {error}
    </div>
  {/if}
  
  <!-- Resultados -->
  {#if result}
    <div class="bg-green-50 border border-green-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold mb-3">Resultado del procesamiento</h2>
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div class="bg-white p-3 rounded shadow-sm">
          <span class="text-sm text-gray-500">Valor procesado:</span>
          <p class="font-medium">{result.processed_value}</p>
        </div>
        <div class="bg-white p-3 rounded shadow-sm">
          <span class="text-sm text-gray-500">Predicción:</span>
          <p class="font-medium">{result.prediction}</p>
        </div>
      </div>
      <details class="bg-gray-50 p-3 rounded">
        <summary class="cursor-pointer text-sm text-gray-600">Datos técnicos</summary>
        <pre class="mt-2 text-xs overflow-auto p-2 bg-gray-100 rounded">{JSON.stringify(result, null, 2)}</pre>
      </details>
    </div>
  {/if}
</div>

<style>
  /* Estilos adicionales específicos del componente */
  .container {
    min-height: 100vh;
    background-color: #f9fafb;
  }
  
  input:focus {
    outline: none;
  }
  
  button {
    transition: all 0.2s ease;
  }
</style>