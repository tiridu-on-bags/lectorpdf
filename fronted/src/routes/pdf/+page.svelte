<!-- src/routes/pdf-viewer/+page.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import SimplePDFViewer from '$lib/components/SimplePDFViewer.svelte';
  import PDFQuestionAnswering from '$lib/components/PDFQuestionAnswering.svelte';
  
  let pdfUrl: string | null = null;
  let file: File | null = null;
  let isUploading = false;
  let uploadError = '';
  let documentId = '';
  let pdfLoaded = false;
  
  // Obtener la URL correcta para la carga de PDFs
  function getUploadUrl() {
    const baseUrl = 'http://localhost:8000';
    // Usar siempre el endpoint que funciona
    return `${baseUrl}/api/upload-basic`;
  }
  
  // Función mejorada para manejar la carga de archivos
  async function handleFileUpload(event) {
    const selectedFile = event.target.files[0];
    if (!selectedFile || selectedFile.type !== 'application/pdf') {
      uploadError = 'Por favor selecciona un archivo PDF válido';
      return;
    }
    
    file = selectedFile;
    isUploading = true;
    uploadError = '';
    pdfLoaded = false;
    
    try {
      // Crear FormData para enviar el archivo
      const formData = new FormData();
      formData.append('file', file);
      
      // Enviar petición con logs detallados
      console.log('Enviando archivo al servidor...');
      console.log('Archivo:', file.name, file.size, file.type);
      
      const url = getUploadUrl();
      console.log('Usando endpoint:', url);
      
      // Comprobar si el servidor está disponible
      try {
        const healthCheck = await fetch(`http://localhost:7860/api/health`);
        console.log('Estado del servidor:', healthCheck.status, healthCheck.ok ? 'OK' : 'Error');
      } catch (healthError) {
        console.error('Error al verificar estado del servidor:', healthError);
        throw new Error('No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose en el puerto 7860.');
      }
      
      // Usar la URL del endpoint que funciona
      const response = await fetch(url, {
        method: 'POST',
        body: formData
      });
      
      console.log('Estado de respuesta:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error en texto:', errorText);
        throw new Error(`Error al subir el archivo: ${response.status} - ${errorText}`);
      }
      
      const data = await response.json();
      console.log('Respuesta de carga:', data);
      
      // Actualizar la URL y el ID del documento
      pdfUrl = `http://localhost:7860${data.url}`;
      documentId = data.document_id;
      pdfLoaded = true;
      
    } catch (error) {
      console.error('Error capturado:', error);
      uploadError = error.message || 'Error desconocido al subir el archivo';
      file = null;
    } finally {
      isUploading = false;
    }
  }
  
  // Función para hacer preguntas (se implementará más adelante)
  async function askQuestion(question) {
    if (!documentId || !question) return;
    
    try {
      const response = await fetch(`http://localhost:7860/api/ask/${documentId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
      });
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      
      const data = await response.json();
      return data.answer;
    } catch (error) {
      console.error('Error al hacer la pregunta:', error);
      return null;
    }
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
      {isUploading ? 'Procesando...' : 'Seleccionar PDF'}
    </label>
    
    {#if file}
      <span class="file-name">{file.name}</span>
    {/if}
  </div>
  
  {#if uploadError}
    <div class="error-message">{uploadError}</div>
  {/if}
  
  <div class="content-grid">
    <!-- Contenedor de visualización -->
    <div class="viewer-container">
      <SimplePDFViewer pdfUrl={pdfUrl} height={600} />
    </div>
    
    <!-- Componente de preguntas sobre el PDF -->
    <PDFQuestionAnswering documentId={documentId} isEnabled={pdfLoaded} />
  </div>
</div>

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  h1 {
    color: #333;
    margin-bottom: 20px;
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
  }
  
  .file-name {
    font-size: 0.9em;
    color: #333;
  }
  
  .error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 10px 16px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .content-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .viewer-container {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-radius: 8px;
    overflow: hidden;
  }
  
  @media (min-width: 1024px) {
    .content-grid {
      grid-template-columns: 1fr 1fr;
    }
  }
</style>