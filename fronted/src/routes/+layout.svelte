<script lang="ts">
	import '@pdfslick/core/dist/pdf_viewer.css';
	import '../app.css';
</script>

<div class="min-h-screen font-sans">
	<header class="sticky top-0 z-10 bg-header shadow-sm">
		<nav class="container mx-auto flex items-center px-4 py-3">
			<a href="/" class="flex items-center">
				<!-- Imagen del logo con tamaño aumentado -->
				<img 
					src="/pdfindex_v4.jpeg" 
					alt="PDFIndex Logo" 
					class="h-16 mr-3"
				/>
			</a>
			<!-- Navegación principal -->
			<div class="ml-auto flex items-center">
				<a href="/" class="text-primary hover:text-accent transition-colors mr-6">Inicio</a>
				<a href="/pdf" class="text-primary hover:text-accent transition-colors mr-6">Cargar PDF</a>
				<a href="/auth" class="bg-accent hover:bg-accent-hover text-white py-2 px-4 rounded-md shadow-sm transition-colors">
					Iniciar Sesión
				</a>
			</div>
		</nav>
	</header>

	<main>
		<slot />
	</main>

	<footer class="bg-white py-8 border-t border-structure/20">
		<div class="container mx-auto px-4 text-center text-secondary">
			<p>© {new Date().getFullYear()} PDFIndex - La forma inteligente de leer documentos</p>
		</div>
	</footer>
</div>

<style>
	/* Paleta de colores correcta */
	:global(:root) {
		--color-background: #faf4ea;
		--color-primary: #747C71;
		--color-secondary: #8a7769;
		--color-accent: #4A6B8A;
		--color-text: #333333;
		--color-text-light: #666666;
		--color-white: #ffffff;
	}

	:global(body) {
		background-color: var(--color-background);
		color: var(--color-text);
		font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
	}

	/* Clases de tailwind personalizadas */
	:global(.bg-header) {
		background-color: var(--color-background);
	}

	:global(.bg-accent) {
		background-color: var(--color-accent);
	}

	:global(.bg-accent-hover) {
		background-color: #3d5a75; /* Versión ligeramente más oscura del acento */
	}

	:global(.text-primary) {
		color: var(--color-primary);
	}

	:global(.text-secondary) {
		color: var(--color-secondary);
	}

	:global(.text-accent) {
		color: var(--color-accent);
	}

	:global(.border-structure) {
		border-color: var(--color-primary);
	}
</style>
