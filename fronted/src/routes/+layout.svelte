<script lang="ts">
	import '../app.css';
	import Header from './Header.svelte';
	import '@pdfslick/core/dist/pdf_viewer.css';
</script>

<div class="min-h-screen font-sans">
	<Header />

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

	/* Estilos para PDFSlick */
	:global(.pdfSlick) {
		height: 100%;
		width: 100%;
		display: flex;
		flex-direction: column;
	}

	:global(.pdfSlickContainer) {
		position: relative;
		height: 100%;
		overflow: auto;
		background-color: #f1f1f1;
	}

	:global(.pdfViewer) {
		margin: 0 auto;
	}
</style>
