<!-- src/lib/components/ContextualPdfViewer.svelte -->
<script lang="ts">
  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
  import { browser } from '$app/environment';
  import ContextualMenu from './ContextualMenu.svelte';
  import AiTooltip from './AiTooltip.svelte';
  
  export let pdfUrl: string | null = null;
  export let documentId: string = '';
  
  let container: HTMLDivElement;
  let pdfSlick: any;
  let unsubscribe: () => void;
  let pageNumber = 1;
  let numPages = 0;
  let loading = false;
  let error: string | null = null;
  
  // Estado para el menú contextual
  let showContextMenu = false;
  let contextMenuX = 0;
  let contextMenuY = 0;
  let selectedText = '';
  let textRange: any = null;
  
  // Estado para tooltips de IA
  let showAiTooltip = false;
  let aiTooltipType = '';  // 'summary', 'explanation', 'answer'
  let aiTooltipContent = '';
  let aiTooltipX = 0;
  let aiTooltipY = 0;
  let isAiLoading = false;
  
  const dispatch = createEventDispatcher();

  onMount(async () => {
    // Solo cargar PDFSlick en el cliente
    if (!browser) return;
    
    try {
      console.log('ContextualPdfViewer - Inicializando PDFSlick');
      // Importar dinámicamente para evitar errores SSR
      const { create, PDFSlick } = await import('@pdfslick/core');
      
      // Crear store de PDFSlick
      const store = create();
      
      console.log('ContextualPdfViewer - Container:', container);
      
      pdfSlick = new PDFSlick({
        container,
        store,
        options: {
          scaleValue: 'page-fit'
        }
      });
      
      // Suscribirse para actualizar estado reactivo
      unsubscribe = store.subscribe((s) => {
        pageNumber = s.pageNumber;
        numPages = s.numPages;
      });
      
      // Configurar listener para selección de texto
      if (container) {
        container.addEventListener('mouseup', handleTextSelection);
        
        // Listener para cerrar menú contextual cuando se hace clic afuera
        document.addEventListener('mousedown', (e) => {
          if (showContextMenu && !isClickInsideMenu(e)) {
            showContextMenu = false;
          }
          
          if (showAiTooltip && !isClickInsideTooltip(e)) {
            showAiTooltip = false;
          }
        });
      }
      
      // Cargar el documento si hay URL
      if (pdfUrl) {
        console.log('ContextualPdfViewer - Cargando documento:', pdfUrl);
        loading = true;
        try {
          await pdfSlick.loadDocument(pdfUrl);
          console.log('ContextualPdfViewer - Documento cargado correctamente');
        } catch (err) {
          console.error('ContextualPdfViewer - Error al cargar documento:', err);
          error = err.message || 'Error al cargar el PDF';
        } finally {
          loading = false;
        }
      }
    } catch (err) {
      console.error('ContextualPdfViewer - Error al inicializar:', err);
      error = err.message || 'Error al inicializar visor';
    }
  });

  onDestroy(() => {
    // Limpiar suscripción
    if (unsubscribe) unsubscribe();
    
    // Limpiar event listeners
    if (browser && container) {
      container.removeEventListener('mouseup', handleTextSelection);
    }
    
    // Limpiar instancia PDFSlick
    if (pdfSlick && typeof pdfSlick.destroy === 'function') {
      pdfSlick.destroy();
    }
  });
  
  // Función para manejar la selección de texto
  function handleTextSelection(event: MouseEvent) {
    if (window.getSelection) {
      const selection = window.getSelection();
      
      if (selection && selection.toString().trim().length > 0) {
        selectedText = selection.toString().trim();
        textRange = selection;
        
        // Posicionar el menú contextual cerca de la selección
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        
        // Calcular posición relativa al contenedor
        const containerRect = container.getBoundingClientRect();
        contextMenuX = rect.left + rect.width / 2 - containerRect.left;
        contextMenuY = rect.bottom - containerRect.top;
        
        showContextMenu = true;
      } else {
        // No cerramos el menú aquí para permitir hacer clic en él
        // Se cerrará si se hace clic fuera del menú
      }
    }
  }
  
  // Verificar si un clic está dentro del menú contextual
  function isClickInsideMenu(event: MouseEvent) {
    const menu = document.querySelector('.contextual-menu');
    return menu ? menu.contains(event.target as Node) : false;
  }
  
  // Verificar si un clic está dentro del tooltip de IA
  function isClickInsideTooltip(event: MouseEvent) {
    const tooltip = document.querySelector('.ai-tooltip');
    return tooltip ? tooltip.contains(event.target as Node) : false;
  }
  
  // Actualizar cuando cambia la URL
  $: if (browser && pdfSlick && pdfUrl) {
    console.log('ContextualPdfViewer - URL actualizada:', pdfUrl);
    loading = true;
    error = null;
    pdfSlick.loadDocument(pdfUrl)
      .catch((err: Error) => {
        console.error('ContextualPdfViewer - Error al cargar documento:', err);
        error = err.message;
      })
      .finally(() => {
        loading = false;
      });
  }
  
  // Handlers para las acciones del menú contextual
  async function handleHighlight() {
    // Implementación futura: Resaltar texto
    showContextMenu = false;
  }
  
  async function handleAddNote() {
    // Implementación futura: Añadir nota
    showContextMenu = false;
  }
  
  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(selectedText);
      showContextMenu = false;
    } catch (err) {
      console.error('Error al copiar texto:', err);
    }
  }
  
  async function handleSummarize() {
    isAiLoading = true;
    showContextMenu = false;
    
    // Posicionar el tooltip cerca de donde estaba el menú
    aiTooltipX = contextMenuX;
    aiTooltipY = contextMenuY + 10;
    aiTooltipType = 'summary';
    showAiTooltip = true;
    
    try {
      // Llamada real al endpoint de resumen
      const response = await fetch(`http://localhost:8000/api/summarize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          text: selectedText, 
          document_id: documentId 
        })
      });
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }
      
      const data = await response.json();
      aiTooltipContent = data.summary;
    } catch (err) {
      console.error('Error al resumir texto:', err);
      aiTooltipContent = 'Error al generar el resumen: ' + err.message;
    } finally {
      isAiLoading = false;
    }
  }
  
  async function handleExplain() {
    isAiLoading = true;
    showContextMenu = false;
    
    aiTooltipX = contextMenuX;
    aiTooltipY = contextMenuY + 10;
    aiTooltipType = 'explanation';
    showAiTooltip = true;
    
    try {
      // Llamada real al endpoint de explicación
      const response = await fetch(`http://localhost:8000/api/explain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          text: selectedText, 
          document_id: documentId 
        })
      });
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${await response.text()}`);
      }
      
      const data = await response.json();
      aiTooltipContent = data.explanation;
    } catch (err) {
      console.error('Error al explicar texto:', err);
      aiTooltipContent = 'Error al generar la explicación: ' + err.message;
    } finally {
      isAiLoading = false;
    }
  }
  
  async function handleAsk() {
    isAiLoading = true;
    showContextMenu = false;
    
    aiTooltipX = contextMenuX;
    aiTooltipY = contextMenuY + 10;
    aiTooltipType = 'ask';
    showAiTooltip = true;
    
    try {
      // Inicialmente solo mostrar un mensaje invitando a preguntar
      aiTooltipContent = `¿Qué quieres saber sobre "${selectedText.substring(0, 30)}..."?`;
      
      // Aquí posteriormente se implementaría una UI para hacer preguntas
      // La llamada real sería como:
      /*
      const response = await fetch(`http://localhost:8000/api/ask-selected`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          question: preguntaDelUsuario,
          context: selectedText,
          document_id: documentId 
        })
      });
      const data = await response.json();
      aiTooltipContent = data.answer;
      */
    } catch (err) {
      console.error('Error al procesar pregunta:', err);
      aiTooltipContent = 'Error al procesar la pregunta: ' + err.message;
    } finally {
      isAiLoading = false;
    }
  }
  
  // Navegación de páginas
  function prevPage() {
    if (pdfSlick && pageNumber > 1) {
      pdfSlick.gotoPage(pageNumber - 1);
    }
  }
  
  function nextPage() {
    if (pdfSlick && pageNumber < numPages) {
      pdfSlick.gotoPage(pageNumber + 1);
    }
  }
  
  // Cerrar tooltip de IA
  function closeAiTooltip() {
    showAiTooltip = false;
  }
</script>

<div class="contextual-pdf-viewer">
  {#if loading}
    <div class="loading-indicator">
      <span class="spinner"></span>
      <p>Cargando documento...</p>
    </div>
  {/if}
  
  {#if error}
    <div class="pdf-error">
      <p>Error: {error}</p>
      <button on:click={() => pdfUrl && pdfSlick?.loadDocument(pdfUrl)}>
        Reintentar
      </button>
    </div>
  {/if}
  
  <!-- Contenedor principal del PDF -->
  <div class="pdf-view-container" bind:this={container}>
    <div class="pdfSlickViewer pdfViewer"></div>
  </div>
  
  <!-- Menú contextual (aparece al seleccionar texto) -->
  {#if showContextMenu}
    <ContextualMenu
      x={contextMenuX}
      y={contextMenuY}
      onHighlight={handleHighlight}
      onAddNote={handleAddNote}
      onCopy={handleCopy}
      onSummarize={handleSummarize}
      onExplain={handleExplain}
      onAsk={handleAsk}
    />
  {/if}
  
  <!-- Tooltip de IA (aparece después de seleccionar una acción de IA) -->
  {#if showAiTooltip}
    <AiTooltip
      x={aiTooltipX}
      y={aiTooltipY}
      type={aiTooltipType}
      content={aiTooltipContent}
      loading={isAiLoading}
      onClose={closeAiTooltip}
    />
  {/if}
  
  <!-- Controles de navegación -->
  <div class="pdf-controls">
    <button on:click={prevPage} disabled={pageNumber <= 1 || loading}>
      ← Anterior
    </button>
    <span class="page-indicator">{pageNumber} / {numPages}</span>
    <button on:click={nextPage} disabled={pageNumber >= numPages || loading}>
      Siguiente →
    </button>
  </div>
</div>

<style>
  .contextual-pdf-viewer {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: #f5f5f5;
  }
  
  .pdf-view-container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 40px; /* Espacio para controles */
    overflow: auto;
  }
  
  .loading-indicator {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #333;
    z-index: 10;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(0, 114, 229, 0.2);
    border-radius: 50%;
    border-top-color: #0072e5;
    animation: spin 1s ease-in-out infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .pdf-error {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #ffebee;
    color: #c62828;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    z-index: 10;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .pdf-error button {
    margin-top: 10px;
    padding: 8px 16px;
    background-color: #0072e5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .pdf-controls {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    background-color: #f0f0f0;
    border-top: 1px solid #ddd;
    z-index: 5;
    padding: 0 16px;
  }
  
  .pdf-controls button {
    padding: 5px 12px;
    background-color: #0072e5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }
  
  .pdf-controls button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  .page-indicator {
    font-size: 14px;
    color: #555;
  }
</style> 