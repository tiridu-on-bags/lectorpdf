# Informe Técnico Complementario de Cambios en PDFIndex (MVP)

**Autor:** Equipo de Desarrollo PDFIndex (Asistente AI)
**Fecha:** `26 de Abril, 2025`
**Versión:** 1.1

---

## 1. Objetivo del Informe

Este documento complementa el reporte de UX/UI existente (reporte_gemini.md) con un enfoque técnico, detallando:

- La **estructura actual** del proyecto y cómo se organizan los archivos.
- Los **cambios de código** realizados en la fase de implementación del MVP.
- **Fragmentos de código** clave para ilustrar cada cambio.
- **Flujos técnicos** y **pasos futuros** recomendados para avanzar en el desarrollo.

Se busca ofrecer un panorama claro para que cualquier desarrollador del equipo entienda el estado del código, las decisiones técnicas adoptadas y las líneas de trabajo pendientes.

---

## 2. Estructura de Proyecto

A continuación se muestra la organización de carpetas y archivos más relevantes tras las últimas iteraciones:

```
lectorpdf/
├── docs/
│   ├── reporte_gemini.md        # Reporte UX/UI inicial
│   ├── Reporteo4.md             # <-- Este informe
│   └── ...
├── fronted/                     # Frontend en SvelteKit
│   ├── src/
│   │   ├── app.css              # Estilos globales
│   │   ├── routes/
│   │   │   ├── +layout.svelte   # Layout principal, incluye <Header />
│   │   │   ├── +page.svelte     # Landing page y sistema de subida PDF
│   │   │   ├── +page.ts         # Carga de datos (vacío por ahora)
│   │   │   ├── Header.svelte    # Componente de cabecera
│   │   │   ├── Document.svelte  # Icono PDF
│   │   │   ├── User.svelte      # Icono Usuario
│   │   │   ├── ContextualPdfViewer.svelte # Visor principal de PDF con IA
│   │   └── lib/components/      # Componentes reutilizables
│   │       ├── ContextualMenu.svelte
│   │       ├── PDFChat.svelte
│   │       └── ...
│   └── ...
└── backend/                     # API en FastAPI
    ├── app/
    │   ├── main.py              # Servidor principal
    │   ├── routers/
    │   │   ├── upload.py        # Endpoint /api/upload-pdf
    │   │   ├── summarize.py     # Endpoint /api/summarize
    │   │   └── qa.py            # Endpoint /api/qa
    │   └── core/
    │       ├── pdf_processing.py
    │       └── llm_client.py    # Cliente para llamar al LLM
    └── requirements.txt
```

---

## 3. Resumen de Cambios Realizados

En las últimas iteraciones del proyecto se han aplicado múltiples cambios en el frontend para incorporar:

1. **Flow de Subida de PDF**: desde la `+page.svelte`, agregando un input oculto, lógica de `handleFileUpload` y la función `openFileDialog()`.
2. **Nuevo componente de Header**: centralización de la cabecera en `Header.svelte`, importado en `+layout.svelte`.
3. **Iconografía SVG**: creación y parametrización de `PdfIndexLogo.svelte`, `Document.svelte` y `User.svelte`.
4. **Estilos globales**: clases `:global(...)` en Svelte para aplicar CSS a iconos y contenedores.
5. **Relleno y hover**: contenedores circulares con color de fondo y efectos de brillo para iconos de navegación.

A continuación se detallan estos cambios con fragmentos de código.

---

### 3.1. Lógica de Subida de PDF (`+page.svelte`)

Se modificó el componente de página para:

- Añadir una referencia `fileInput` que permite abrir el selector de archivos desde un botón.
- Implementar la función **`openFileDialog()`**.
- Actualizar el botón primario para usar dicha función.

Fragmento:

```svelte
<script lang="ts">
  let fileInput: HTMLInputElement;
  let isUploading = false;
  let uploadError = '';

  function openFileDialog() {
    fileInput?.click();
  }

  async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file || file.type !== 'application/pdf') {
      uploadError = 'Selecciona un PDF válido';
      return;
    }
    isUploading = true;
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/upload-pdf', { method: 'POST', body: formData });
      const data = await res.json();
      pdfUrl = data.url;
    } catch (e) {
      uploadError = e.message;
    } finally {
      isUploading = false;
    }
  }
</script>

<button class="btn-upload" on:click={openFileDialog} disabled={isUploading}>
  {isUploading ? 'Procesando...' : 'Sube un PDF ahora'}
</button>

<input
  bind:this={fileInput}
  type="file"
  accept="application/pdf"
  class="hidden"
  on:change={handleFileUpload}
  disabled={isUploading} />
```

Este patrón se puede replicar en cualquier componente que requiera invocar un diálogo de selección de archivos.

---

### 3.2. Componente de Header (`Header.svelte`)

Se creó un componente `Header.svelte` que centraliza:

- El **logo** con `PdfIndexLogo`.
- La **navegación** usando iconos `Document` y `User`.
- La lógica de rutas activas (atributo `aria-current`).
- Estilos globales para contenedores circulares y efectos hover.

```svelte
<script lang="ts">
  import PdfIndexLogo from './PdfIndexLogo.svelte';
  import Document from './Document.svelte';
  import User from './User.svelte';
  import { page } from '$app/stores';
</script>

<header class="header-container">
  <nav>
    <div class="logo-container">
      <a href="/">
        <PdfIndexLogo size={50} className="logo" />
      </a>
    </div>
    <ul>
      <li aria-current={$page.url.pathname.startsWith('/pdf') ? 'page' : undefined}>
        <a href="/pdf">
          <div class="nav-icon-container">
            <Document size={16} className="nav-icon" />
          </div>
        </a>
      </li>
      <li aria-current={$page.url.pathname.startsWith('/auth') ? 'page' : undefined}>
        <a href="/auth">
          <div class="nav-icon-container">
            <User size={16} className="nav-icon" />
          </div>
        </a>
      </li>
    </ul>
  </nav>
</header>
```

#### Estilos relevantes

```css
:global(.nav-icon-container) {
  width: 2.5rem;
  height: 2.5rem;
  background-color: #faf4ea;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: filter 0.2s ease;
}

:global(.nav-icon-container:hover) {
  filter: brightness(1.05);
}

:global(.nav-icon-container .nav-icon) {
  width: 1.2rem;
  height: 1.2rem;
}
```

---

### 3.3. Componente `PdfIndexLogo.svelte`

Este SVG se parametrizó para aceptar `size` y `className`, y aplicar `border-radius` y `overflow`:

```svelte
<script lang="ts">
  export let size: number = 80;
  export let rounded: number = 50;
  export let className: string = '';
</script>

<svg
  class={className}
  width={size}
  height={size}
  viewBox="0 0 512 512"
  style="border-radius: {rounded}px; overflow:hidden;"
  fill="none"
  xmlns="http://www.w3.org/2000/svg">
  <!-- Paths del logo... -->
</svg>
```

---

### 3.4. Componentes `Document.svelte` y `User.svelte`

Ambos se refactorizaron para usar `size` y `className`:

```svelte
<script lang="ts">
  export let size: number = 80;
  export let className: string = '';
</script>

<svg
  class={className}
  width={size}
  height={size}
  viewBox="0 0 1024 1024"
  xmlns="http://www.w3.org/2000/svg"
  fill="#000000">
  <!-- Paths del icono... -->
</svg>
```

Luego se insertan en `Header.svelte` con contenedores.

---

## 4. Flujo Técnico y Pasos Futuros

A continuación se describen los próximos pasos a nivel técnico para avanzar hacia el MVP completo.

### 4.1. Menú Contextual - "Lápiz Inteligente Contextual"

**Objetivo**: Aparecer inline sobre la selección de texto en el visor de PDF, ofreciendo acciones IA.

**Tareas**:

1. **Detectar selección de texto** en `ContextualPdfViewer.svelte`.
   - Usar el API de PDFSlick para capturar rangos y coordenadas.
   - Lanzar un evento Svelte (`dispatch('textSelected', { text, rect })`).
2. **Crear componente `ContextualMenu.svelte`**, recibiendo props `{ x, y, actions[] }` y renderizar botones de acción.
3. **Integrar en `ContextualPdfViewer`**: reposicionar el menú absoluto respecto a la coordenada del rect. Ejemplo:

   ```svelte
   <script lang="ts">
     import ContextualMenu from './ContextualMenu.svelte';
     import { createEventDispatcher } from 'svelte';
     const dispatch = createEventDispatcher();
   
     function onTextSelected(e) {
       dispatch('showMenu', { x: e.detail.rect.x, y: e.detail.rect.y });
     }
   </script>

   <ContextualPdfSlick on:textSelected={onTextSelected} />
   {#if menuVisible}
     <ContextualMenu {x} {y} actions={menuActions} />
   {/if}
   ```

4. **Acciones de IA**: cada botón de `ContextualMenu` dispara una llamada:
   ```ts
   async function summarizeSelected() {
     const res = await fetch('/api/summarize', {
       method: 'POST',
       body: JSON.stringify({ text: selectedText })
     });
     const summary = await res.json();
     showTooltip(summary, { x, y });
   }
   ```

5. **Componente `Tooltip.svelte`**: mostrar resultados IA cerca de la selección.
   - Se crean animaciones de aparición/desaparición suaves.

---

### 4.2. Backend - Endpoints para IA

Tres rutas principales ya estructuradas:

- **`POST /api/upload-pdf`** ➔ Recibe `multipart/form-data` con el PDF, guarda en `/uploads` y devuelve `{ url, document_id }`.
- **`POST /api/summarize`** ➔ Recibe `{ text }`, llama a LLM (`llm_client.summarize(text)`), devuelve `{ summary }`.
- **`POST /api/qa`** ➔ Recibe `{ text, question }`, llama a LLM (`llm_client.qa(text, question)`), devuelve `{ answer }`.

**Pasos**:

1. Añadir validaciones de tamaño y tipo en `upload.py`.
2. Incluir tests unitarios con `pytest` para cada endpoint.
3. Registrar métricas y tiempos de respuesta.

---

### 4.3. Testeo y QA

- **Unit tests** (Frontend): Con `vitest` y `@testing-library/svelte`, cubrir:
  - `Header.svelte` render y clases activas.
  - `+page.svelte` lógica de subida (mock fetch).
  - `ContextualMenu` y `Tooltip`.
- **E2E tests**: Con `Playwright`, scripts para:
  1. Subir un PDF desde UI.
  2. Seleccionar texto y probar `Lápiz Inteligente`.



