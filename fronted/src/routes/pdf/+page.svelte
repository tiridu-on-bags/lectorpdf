<!-- src/routes/pdf/+page.svelte -->
<script lang="ts">
  // IMPORTANTE: Importar los estilos CSS de PDFSlick
  import "@pdfslick/core/dist/pdf_viewer.css";
  import { onMount } from 'svelte';
  import SimplePDFViewer from '$lib/components/SimplePDFViewer.svelte';
  
  let pdfUrl: string | null = null;
  let file: File | null = null;
  let isUploading = false;
  let uploadError = '';
  let documentId = '';
  let pdfLoaded = false;
  
  // Registrar cambios en pdfUrl para depuración
  $: if (pdfUrl) {
    console.log('pdfUrl actualizada:', pdfUrl);
  }
  
  async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const selectedFile = input.files?.[0] || null;
    
    if (!selectedFile || selectedFile.type !== 'application/pdf') {
      uploadError = 'Por favor selecciona un archivo PDF válido';
      return;
    }
    
    file = selectedFile;
    isUploading = true;
    uploadError = '';
    pdfUrl = null; // Reset URL to force reload
    
    try {
      // Crear FormData para enviar el archivo
      const formData = new FormData();
      formData.append('file', file);
      
      console.log('Enviando archivo al servidor...');
      console.log('Archivo:', file.name, file.size, file.type);
      
      const endpoint = 'http://localhost:8000/api/upload-basic';
      console.log('Usando endpoint:', endpoint);
      
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        throw new Error(`Error al subir el archivo: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Respuesta del servidor:', data);
      
      // CAMBIO IMPORTANTE: Esperar un momento antes de asignar la URL
      // Esto permite que el componente se actualice correctamente
      setTimeout(() => {
        pdfUrl = `http://localhost:8000${data.url}`;
        documentId = data.document_id || '';
        pdfLoaded = true;
        isUploading = false;
        console.log('PDF URL asignada:', pdfUrl);
      }, 100);
      
    } catch (error) {
      console.error('Error capturado:', error);
      uploadError = error.message || 'Error desconocido al subir el archivo';
      isUploading = false;
      file = null;
    }
  }
  
  // Función para verificar si una URL es válida y accesible
  async function checkUrl(url: string): Promise<boolean> {
    try {
      const response = await fetch(url, { method: 'HEAD' });
      return response.ok;
    } catch (error) {
      console.error('Error verificando URL:', error);
      return false;
    }
  }
  
  // Verificar la URL del PDF cuando cambie
  $: if (pdfUrl) {
    checkUrl(pdfUrl).then(isValid => {
      if (!isValid) {
        console.error('La URL del PDF no es accesible:', pdfUrl);
      } else {
        console.log('URL del PDF verificada y accesible');
      }
    });
  }
</script>

<div class="container">
  <h1>Visor de PDF con consultas</h1>
  
  <div class="upload-section">
    <input 
      type="file" 
      accept="application/pdf" 
      on:change={handleFileUpload}
      id="pdf-upload"
      class="file-input"
      disabled={isUploading}
    />
    <label for="pdf-upload" class="file-label">
      {#if isUploading}
        Procesando...
      {:else}
        Seleccionar PDF
      {/if}
    </label>
    
    {#if file}
      <span class="file-name">{file.name}</span>
    {/if}
  </div>
  
  {#if uploadError}
    <div class="error-message">{uploadError}</div>
  {/if}
  
  <!-- Contenedor principal para el visor de PDF y las preguntas -->
  <div class="content-grid">
    <!-- Contenedor del visor con altura fija -->
    <div class="viewer-container">
      <!-- Debug info -->
      {#if pdfUrl}
        <div class="debug-bar">
          URL: {pdfUrl}
        </div>
      {/if}
      
      <!-- Solo renderizamos el componente si tenemos una URL -->
      <SimplePDFViewer 
        pdfUrl={pdfUrl} 
        height={550} 
      />
    </div>
    
    <!-- Panel de preguntas -->
    <div class="questions-panel">
      <h2>Preguntas sobre el PDF</h2>
      
      {#if !pdfLoaded}
        <p class="info-message">Carga un documento PDF para poder hacer preguntas sobre su contenido</p>
      {:else}
        <!-- Aquí irá el componente de preguntas cuando esté implementado -->
        <div class="questions-form">
          <textarea 
            placeholder="Escribe tu pregunta sobre el documento..." 
            class="question-input"
          ></textarea>
          <button class="submit-btn">Preguntar</button>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  /* Asegurarnos de que PDFSlick tenga el espacio correcto */
  :global(.pdfSlickViewer) {
    margin: 0 !important;
  }
  
  :global(.pdfSlickContainer .pdfViewer) {
    position: relative;
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  h1 {
    font-size: 28px;
    margin-bottom: 20px;
    color: #333;
  }
  
  h2 {
    font-size: 20px;
    margin-bottom: 16px;
    color: #333;
  }
  
  .upload-section {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .file-input {
    display: none;
  }
  
  .file-label {
    padding: 8px 16px;
    background-color: #0072e5;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
  }
  
  .file-name {
    font-size: 14px;
    color: #555;
  }
  
  .error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 10px 16px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .debug-bar {
    background-color: #f0f8ff;
    padding: 4px 8px;
    font-size: 12px;
    color: #0066cc;
    border-bottom: 1px solid #ccc;
    word-break: break-all;
  }
  
  .content-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .viewer-container {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    height: 600px; /* Altura fija para el contenedor */
  }
  
  .questions-panel {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .info-message {
    color: #666;
    text-align: center;
    padding: 20px;
  }
  
  .questions-form {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .question-input {
    width: 100%;
    height: 100px;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: none;
    font-family: inherit;
  }
  
  .submit-btn {
    padding: 8px 16px;
    background-color: #0072e5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    align-self: flex-end;
  }
  
  @media (min-width: 1024px) {
    .content-grid {
      grid-template-columns: 2fr 1fr;
    }
  }
</style>