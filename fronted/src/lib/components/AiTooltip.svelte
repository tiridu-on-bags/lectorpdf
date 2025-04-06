<!-- src/lib/components/AiTooltip.svelte -->
<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';

  export let x: number = 0;  // Posición horizontal
  export let y: number = 0;  // Posición vertical
  export let type: string = 'summary';  // Tipo de tooltip: 'summary', 'explanation', 'ask'
  export let content: string = '';  // Contenido del tooltip
  export let loading: boolean = false;  // Si está cargando
  export let onClose: () => void = () => {};  // Función para cerrar el tooltip
  
  // Limitar la posición para que no se salga de la ventana
  let tooltipElement: HTMLDivElement;
  let adjustedX = x;
  let adjustedY = y;
  
  const dispatch = createEventDispatcher();
  
  // Copiar contenido al portapapeles
  async function copyContent() {
    try {
      await navigator.clipboard.writeText(content);
      showCopySuccess = true;
      setTimeout(() => {
        showCopySuccess = false;
      }, 2000);
    } catch (err) {
      console.error('Error al copiar texto:', err);
    }
  }
  
  let showCopySuccess = false;
  
  // Obtener título según el tipo
  $: title = type === 'summary' 
    ? 'Resumen IA' 
    : type === 'explanation' 
      ? 'Explicación IA' 
      : 'Pregunta sobre el texto';
  
  // Ajustar posición en pantalla
  onMount(() => {
    if (tooltipElement) {
      const rect = tooltipElement.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      
      // Ajustar posición horizontal si se sale de la ventana
      if (x + rect.width > viewportWidth) {
        adjustedX = Math.max(10, x - rect.width);
      }
      
      // Ajustar posición vertical si se sale de la ventana
      if (y + rect.height > viewportHeight) {
        adjustedY = Math.max(10, y - rect.height - 20); // 20px de espacio extra
      }
    }
  });
</script>

<div
  class="ai-tooltip"
  bind:this={tooltipElement}
  style="left: {adjustedX}px; top: {adjustedY}px;"
>
  <div class="tooltip-header">
    <div class="tooltip-title">✨ {title}</div>
    <button class="close-button" on:click={onClose}>×</button>
  </div>
  
  <div class="tooltip-content">
    {#if loading}
      <div class="loading-indicator">
        <div class="spinner-small"></div>
        <span>Generando respuesta...</span>
      </div>
    {:else}
      <p>{content}</p>
    {/if}
  </div>
  
  <div class="tooltip-footer">
    <button 
      class="action-button copy-button" 
      on:click={copyContent}
      disabled={loading}
    >
      {showCopySuccess ? '✓ Copiado' : 'Copiar'}
    </button>
    
    {#if type === 'ask'}
      <button class="action-button follow-up-button" disabled={loading}>
        Hacer pregunta de seguimiento
      </button>
    {/if}
  </div>
</div>

<style>
  .ai-tooltip {
    position: absolute;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 3px 14px rgba(0, 0, 0, 0.25);
    width: 300px;
    max-width: 90vw;
    overflow: hidden;
    z-index: 1000;
    animation: fadeIn 0.2s ease-out;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .tooltip-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    background-color: #f0f7ff;
    border-bottom: 1px solid #d0e3ff;
  }
  
  .tooltip-title {
    font-weight: 500;
    color: #0066cc;
    font-size: 14px;
  }
  
  .close-button {
    background: none;
    border: none;
    font-size: 20px;
    line-height: 1;
    color: #666;
    cursor: pointer;
    padding: 0 4px;
  }
  
  .tooltip-content {
    padding: 12px 16px;
    font-size: 14px;
    color: #333;
    line-height: 1.5;
    max-height: 200px;
    overflow-y: auto;
  }
  
  .tooltip-footer {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding: 8px 16px;
    background-color: #f9f9f9;
    border-top: 1px solid #eee;
  }
  
  .action-button {
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    font-size: 12px;
    cursor: pointer;
    background-color: #f0f0f0;
    color: #333;
  }
  
  .action-button:hover {
    background-color: #e0e0e0;
  }
  
  .action-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .copy-button {
    background-color: #e0f2ff;
    color: #0066cc;
  }
  
  .copy-button:hover {
    background-color: #cce7ff;
  }
  
  .follow-up-button {
    background-color: #e6f4ea;
    color: #137333;
  }
  
  .follow-up-button:hover {
    background-color: #d7eadd;
  }
  
  .loading-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #666;
    font-size: 14px;
  }
  
  .spinner-small {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(0, 114, 229, 0.2);
    border-radius: 50%;
    border-top-color: #0072e5;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style> 