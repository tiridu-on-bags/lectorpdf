<script lang="ts">
  import { onMount } from 'svelte';
  
  export let documentId: string = '';
  export let isEnabled: boolean = false;
  
  let question: string = '';
  let answer: string = '';
  let isLoading: boolean = false;
  let error: string = '';
  let chatHistory: {question: string, answer: string}[] = [];
  
  async function handleSubmit() {
    if (!question.trim() || !documentId) return;
    
    isLoading = true;
    error = '';
    
    try {
      console.log('Enviando pregunta para documento:', documentId);
      console.log('Pregunta:', question);
      
      const response = await fetch(`http://localhost:7860/api/ask/${documentId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error al procesar la pregunta: ${response.status} - ${errorText}`);
      }
      
      const data = await response.json();
      console.log('Respuesta del LLM:', data);
      
      answer = data.answer;
      chatHistory = [...chatHistory, {question, answer}];
      question = '';
      
    } catch (e) {
      console.error('Error al hacer la pregunta:', e);
      error = e.message || 'Error desconocido al consultar el LLM';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="qa-container">
  <h2>Preguntas sobre el PDF</h2>
  
  {#if !isEnabled}
    <div class="disabled-message">
      <p>Carga un documento PDF para poder hacer preguntas sobre su contenido</p>
    </div>
  {:else}
    <div class="chat-history">
      {#if chatHistory.length === 0}
        <div class="empty-history">
          <p>Haz una pregunta sobre el documento cargado</p>
        </div>
      {:else}
        {#each chatHistory as chat, i}
          <div class="chat-item">
            <div class="question">
              <span class="label">Pregunta:</span>
              <p>{chat.question}</p>
            </div>
            <div class="answer">
              <span class="label">Respuesta:</span>
              <p>{chat.answer}</p>
            </div>
          </div>
        {/each}
      {/if}
    </div>
    
    <form on:submit|preventDefault={handleSubmit} class="question-form">
      <div class="input-container">
        <textarea 
          bind:value={question} 
          placeholder="Haz una pregunta sobre el documento..."
          rows="3"
          disabled={isLoading}
        ></textarea>
      </div>
      
      <button type="submit" disabled={!question.trim() || isLoading}>
        {isLoading ? 'Procesando...' : 'Preguntar'}
      </button>
    </form>
    
    {#if error}
      <div class="error-message">
        {error}
      </div>
    {/if}
  {/if}
</div>

<style>
  .qa-container {
    margin-top: 30px;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    background-color: #fcfcfc;
  }
  
  h2 {
    color: #333;
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 1.5rem;
  }
  
  .disabled-message {
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 6px;
    text-align: center;
    color: #666;
  }
  
  .chat-history {
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 20px;
  }
  
  .empty-history {
    color: #666;
    text-align: center;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 6px;
  }
  
  .chat-item {
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 20px;
  }
  
  .chat-item:last-child {
    border-bottom: none;
  }
  
  .question, .answer {
    margin-bottom: 10px;
  }
  
  .label {
    font-weight: bold;
    color: #0072e5;
    display: block;
    margin-bottom: 5px;
  }
  
  .question p, .answer p {
    margin: 0;
    padding: 10px;
    border-radius: 6px;
  }
  
  .question p {
    background-color: #e1f5fe;
  }
  
  .answer p {
    background-color: #f1f8e9;
  }
  
  .question-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .input-container {
    width: 100%;
  }
  
  textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    resize: vertical;
    font-family: inherit;
    font-size: 1rem;
  }
  
  button {
    padding: 12px 20px;
    background-color: #0072e5;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    align-self: flex-end;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  .error-message {
    margin-top: 10px;
    padding: 10px;
    background-color: #ffebee;
    color: #c62828;
    border-radius: 4px;
  }
</style> 