<script lang="ts">
  let file: File | null = null;
  let isUploading = false;
  let uploadError = '';
  let uploadSuccess = false;
  let pdfUrl = '';
  
  async function handleFileUpload(event) {
    const selectedFile = event.target.files[0];
    if (!selectedFile || selectedFile.type !== 'application/pdf') {
      uploadError = 'Por favor selecciona un archivo PDF válido';
      return;
    }
    
    file = selectedFile;
    isUploading = true;
    uploadError = '';
    uploadSuccess = false;
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      console.log('Enviando archivo al servidor (prueba simple)...');
      console.log('Archivo:', file.name, file.size, file.type);
      
      // Endpoint simplificado
      const response = await fetch('http://localhost:7860/api/upload-basic', {
        method: 'POST',
        body: formData
      });
      
      console.log('Estado de respuesta:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error en texto:', errorText);
        throw new Error(`Error al subir el archivo: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Respuesta de carga:', data);
      
      // Actualizar la URL del PDF
      pdfUrl = `http://localhost:7860${data.url}`;
      uploadSuccess = true;
      
    } catch (error) {
      console.error('Error capturado:', error);
      uploadError = error.message || 'Error desconocido al subir el archivo';
      file = null;
    } finally {
      isUploading = false;
    }
  }
</script>

<div class="container">
  <h1>Subida de PDF - Prueba Simple</h1>
  
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
  
  {#if uploadSuccess}
    <div class="success-message">
      <p>¡Archivo subido correctamente!</p>
      <a href={pdfUrl} target="_blank" rel="noopener noreferrer">Ver PDF</a>
    </div>
    
    <div class="pdf-viewer">
      <iframe src={pdfUrl} width="100%" height="500px" title="PDF Viewer"></iframe>
    </div>
  {/if}
</div>

<style>
  .container {
    max-width: 800px;
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
  
  .success-message {
    background-color: #e8f5e9;
    color: #2e7d32;
    padding: 10px 16px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .success-message a {
    display: inline-block;
    margin-top: 8px;
    color: #0072e5;
    text-decoration: none;
  }
  
  .pdf-viewer {
    border: 1px solid #ddd;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 20px;
  }
</style> 