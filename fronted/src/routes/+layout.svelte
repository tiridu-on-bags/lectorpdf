<script lang="ts">
	import '@pdfslick/core/dist/pdf_viewer.css';
	import '../app.css';
</script>

<div class="bg-background text-primary-text min-h-screen font-sans">
	<header class="sticky top-0 z-10 bg-white shadow-md">
		<nav class="container mx-auto flex items-center px-4 py-4">
			<a href="/" class="flex items-center">
				<!-- Imagen del logo -->
				<img 
					src="/pdfindex_v4.jpeg" 
					alt="LectorPDF Logo" 
					class="h-14 mr-3"
				/>
			</a>
			<!-- Navegación principal -->
			<div class="ml-auto flex items-center">
				<a href="/" class="text-secondary-text hover:text-accent transition-colors mr-6">Inicio</a>
				<a href="/pdf" class="text-secondary-text hover:text-accent transition-colors mr-6">Cargar PDF</a>
				<a href="/auth" class="bg-accent hover:bg-accent-hover text-white py-2 px-4 rounded-md shadow-sm transition-colors">
					Iniciar Sesión
				</a>
			</div>
		</nav>
	</header>

	<main>
		<slot />
	</main>

	<footer class="bg-white py-8 border-t border-structure-alt/20">
		<div class="container mx-auto px-4 text-center text-secondary-text">
			<p>© {new Date().getFullYear()} LectorPDF - La forma inteligente de leer documentos</p>
		</div>
	</footer>
</div>

<style>
	/* Estilos globales específicos aquí si es necesario */
</style>
