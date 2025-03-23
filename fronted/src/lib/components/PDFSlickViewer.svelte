<!-- src/lib/components/PDFSlickViewer.svelte -->
<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { create, PDFSlick } from "@pdfslick/core";
    
    export let pdfUrl = null;
    export let onLoad = () => {};
    
    let container;
    let pdfSlick;
    let store;
    
    onMount(() => {
      if (!container) return;
      
      store = create();
      
      // Una vez montado el componente, cargamos el PDF si está disponible
      if (pdfUrl) {
        loadPDF(pdfUrl);
      }
      
      return () => {
        if (pdfSlick) {
          pdfSlick.cleanup();
        }
      };
    });
    
    $: if (pdfUrl && container && !pdfSlick) {
      loadPDF(pdfUrl);
    }
    
    function loadPDF(url) {
      if (!url || !container) return;
      
      if (pdfSlick) {
        pdfSlick.cleanup();
      }
      
      pdfSlick = new PDFSlick({
        container,
        store,
        options: { 
          scaleValue: "page-fit"
        }
      });
      
      pdfSlick.loadDocument(url).then(() => {
        onLoad();
      }).catch(error => {
        console.error("Error cargando PDF:", error);
      });
    }
  </script>
  
  <div class="pdfslick-container" bind:this={container}></div>
  
  <style>
    .pdfslick-container {
      width: 100%;
      height: 100%;
      min-height: 500px;
      background-color: #f5f5f5;
    }
  </style>