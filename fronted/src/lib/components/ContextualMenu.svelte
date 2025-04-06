<!-- src/lib/components/ContextualMenu.svelte -->
<script lang="ts">
  export let x: number = 0;  // Posición horizontal
  export let y: number = 0;  // Posición vertical
  
  // Funciones callback para las acciones del menú
  export let onHighlight: () => void = () => {};
  export let onAddNote: () => void = () => {};
  export let onCopy: () => void = () => {};
  export let onSummarize: () => void = () => {};
  export let onExplain: () => void = () => {};
  export let onAsk: () => void = () => {};
  
  // Limitar la posición para que no se salga de la ventana
  import { onMount } from 'svelte';
  let menuElement: HTMLDivElement;
  let adjustedX = x;
  let adjustedY = y;
  
  onMount(() => {
    if (menuElement) {
      const rect = menuElement.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      
      // Ajustar posición horizontal si se sale de la ventana
      if (x + rect.width > viewportWidth) {
        adjustedX = x - rect.width;
      }
      
      // Ajustar posición vertical si se sale de la ventana
      if (y + rect.height > viewportHeight) {
        adjustedY = y - rect.height - 20; // 20px de espacio extra
      }
    }
  });
</script>

<div
  class="contextual-menu"
  bind:this={menuElement}
  style="left: {adjustedX}px; top: {adjustedY}px;"
>
  <div class="menu-section standard-actions">
    <button class="menu-item" on:click={onHighlight}>
      <span class="icon">🖌️</span> Resaltar
    </button>
    <button class="menu-item" on:click={onAddNote}>
      <span class="icon">📝</span> Añadir nota
    </button>
    <button class="menu-item" on:click={onCopy}>
      <span class="icon">📋</span> Copiar
    </button>
  </div>
  
  <div class="menu-divider"></div>
  
  <div class="menu-section ai-actions">
    <button class="menu-item" on:click={onSummarize}>
      <span class="icon">✨</span> Resumir selección
    </button>
    <button class="menu-item" on:click={onExplain}>
      <span class="icon">✨</span> Explicar selección
    </button>
    <button class="menu-item" on:click={onAsk}>
      <span class="icon">✨</span> Preguntar sobre esto
    </button>
  </div>
</div>

<style>
  .contextual-menu {
    position: absolute;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    width: 200px;
    overflow: hidden;
    z-index: 1000;
    transform-origin: top center;
    animation: popup 0.15s ease-out;
  }
  
  @keyframes popup {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  .menu-section {
    padding: 8px 0;
  }
  
  .menu-divider {
    height: 1px;
    background-color: #e0e0e0;
    margin: 0 8px;
  }
  
  .menu-item {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 8px 16px;
    border: none;
    background: none;
    text-align: left;
    font-size: 14px;
    cursor: pointer;
    color: #333;
    transition: background-color 0.15s;
  }
  
  .menu-item:hover {
    background-color: #f0f0f0;
  }
  
  .icon {
    display: inline-block;
    width: 20px;
    margin-right: 8px;
    text-align: center;
  }
  
  .ai-actions .menu-item {
    color: #0066cc;
  }
  
  .ai-actions .icon {
    color: #0072e5;
  }
</style> 