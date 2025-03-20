<script lang="ts">
    import { fetchPrediction, checkServerStatus } from '$lib/api/client';
    import { onMount } from 'svelte';
    
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
    let isServerOnline = false;
    
    // Verificar si el servidor está en línea al cargar el componente
    onMount(async () => {
        isServerOnline = await checkServerStatus();
        if (!isServerOnline) {
            error = "El servidor de Gradio no está en línea. Verifica que esté ejecutándose.";
        }
    });
    
    async function handleSubmit() {
        // Verificar nuevamente el estado del servidor antes de enviar
        if (!isServerOnline) {
            isServerOnline = await checkServerStatus();
            if (!isServerOnline) {
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
            
            result = await fetchPrediction<InputData, ResultData>(data);
        } catch (err) {
            error = err instanceof Error ? err.message : 'Error desconocido';
            result = null;
        } finally {
            loading = false;
        }
    }
</script>

<div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Mi App Gradio + SvelteKit</h1>
    
    <!-- Indicador de estado del servidor -->
    <div class="mb-4">
        <p>
            Estado del servidor: 
            {#if isServerOnline}
                <span class="text-green-600 font-semibold">En línea</span>
            {:else}
                <span class="text-red-600 font-semibold">Desconectado</span>
            {/if}
        </p>
    </div>
    
    <div class="mb-4">
        <label class="block mb-2">
            Valor numérico:
            <input type="number" bind:value={inputValue} class="border p-2 w-full" />
        </label>
        
        <label class="block mb-2">
            Texto (opcional):
            <input type="text" bind:value={inputText} class="border p-2 w-full" />
        </label>
        
        <button 
            on:click={handleSubmit} 
            disabled={loading || !isServerOnline}
            class="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
            {loading ? 'Procesando...' : 'Enviar a la API'}
        </button>
    </div>
    
    {#if error}
        <div class="bg-red-100 border border-red-400 text-red-700 p-4 mb-4 rounded">
            {error}
        </div>
    {/if}
    
    {#if result}
        <div class="bg-green-100 border border-green-400 p-4 rounded">
            <h2 class="font-bold mb-2">Resultado:</h2>
            <p>Valor procesado: {result.processed_value}</p>
            <p>Predicción: {result.prediction}</p>
            <pre class="bg-gray-100 p-2 mt-2">{JSON.stringify(result, null, 2)}</pre>
        </div>
    {/if}
</div>