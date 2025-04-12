// vite.config.js
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  
  // Configuración del proxy para backend FastAPI
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  
  // Resolución de módulos optimizada
  resolve: {
    dedupe: ['svelte']
  },

  // Configuración de optimización de dependencias
  optimizeDeps: {
    include: ['@sveltejs/kit', 'svelte'],
    force: true
  }
});