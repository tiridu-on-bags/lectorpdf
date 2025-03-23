<!-- src/lib/components/PDFChat.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    
    export let documentId: string | null = null;
    export let apiUrl: string = '/api/ask';
    
    let question = '';
    let answer = '';
    let isLoading = false;
    let error = '';
    let chatHistory = [];
    
    async function askQuestion() {
      if (!question.trim() || !documentId) return;
      
      isLoading = true;
      error = '';
      
      try {
        const response = await fetch(`${apiUrl}/${documentId}`, {
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
        answer = data.answer;
        
        // Añadir a historial
        chatHistory = [
          ...chatHistory, 
          { 
            type: 'question', 
            text: question 
          },
          { 
            type: 'answer', 
            text: data.answer,
            contexts: data.contexts 
          }
        ];
        
        // Limpiar pregunta
        question = '';
        
      } catch (e) {
        error = e.message || 'Error al procesar tu pregunta';
      } finally {
        isLoading = false;
      }
    }
  </script>
  
  <div class="pdf-chat">
    <div class="chat-history">
      {#each chatHistory as message}
        <div class="message {message.type}">
          <div class="message-text">{message.text}</div>
          {#if message.type === 'answer' && message.contexts}
            <details class="contexts">
              <summary>Ver fuentes</summary>
              <div class="context-list">
                {#each message.contexts as context}
                  <div class="context-item">{context}</div>
                {/each}
              </div>
            </details>
          {/if}
        </div>
      {/each}
      
      {#if isLoading}
        <div class="loading">Procesando tu pregunta...</div>
      {/if}
      
      {#if error}
        <div class="error">{error}</div>
      {/if}
    </div>
    
    <div class="chat-input">
      <input
        type="text"
        bind:value={question}
        placeholder="Haz una pregunta sobre el PDF..."
        on:keydown={e => e.key === 'Enter' && askQuestion()}
        disabled={isLoading || !documentId}
      />
      <button 
        on:click={askQuestion} 
        disabled={isLoading || !question.trim() || !documentId}
      >
        Preguntar
      </button>
    </div>
  </div>
  
  <style>
    .pdf-chat {
      display: flex;
      flex-direction: column;
      height: 100%;
      border: 1px solid #ddd;
      border-radius: 8px;
      overflow: hidden;
    }
    
    .chat-history {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    
    .message {
      padding: 10px 14px;
      border-radius: 8px;
      max-width: 85%;
    }
    
    .message.question {
      align-self: flex-end;
      background-color: #f0f4f8;
    }
    
    .message.answer {
      align-self: flex-start;
      background-color: #e7f3ff;
    }
    
    .contexts {
      margin-top: 8px;
      font-size: 0.8em;
    }
    
    .context-list {
      margin-top: 8px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    
    .context-item {
      padding: 8px;
      background-color: #f5f5f5;
      border-radius: 4px;
      font-size: 0.9em;
    }
    
    .chat-input {
      display: flex;
      padding: 12px;
      border-top: 1px solid #eee;
      background: white;
    }
    
    input {
      flex: 1;
      padding: 10px 14px;
      border: 1px solid #ddd;
      border-radius: 4px;
      margin-right: 8px;
    }
    
    button {
      padding: 10px 20px;
      background-color: #0072e5;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    
    button:disabled {
      background-color: #ccc;
      cursor: not-allowed;
    }
    
    .loading {
      align-self: center;
      color: #666;
      font-style: italic;
    }
    
    .error {
      color: #e53935;
      background-color: #ffebee;
      padding: 8px 12px;
      border-radius: 4px;
      align-self: center;
    }
  </style>