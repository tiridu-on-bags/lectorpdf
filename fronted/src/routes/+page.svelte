<script lang="ts">
	// IMPORTANTE: Importar los estilos CSS de PDFSlick
	import '@pdfslick/core/dist/pdf_viewer.css';
	import { onMount } from 'svelte';
	import ContextualPdfViewer from '$lib/components/ContextualPdfViewer.svelte';

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

	// Función para navegar a la página de carga de PDF
	function navigateToPDFUpload() {
		window.location.href = '/pdf';
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
		pdfUrl = null; // Resetear pdfUrl al iniciar nueva subida
		pdfLoaded = false;
		documentId = '';

		try {
			const formData = new FormData();
			formData.append('file', file);

			console.log('Iniciando subida de archivo...');
			const endpoint = '/api/upload-pdf'; // Usar el proxy configurado en Vite
			console.log('Endpoint de subida:', endpoint);

			const response = await fetch(endpoint, {
				method: 'POST',
				body: formData
			});

			console.log('Estado de la respuesta:', response.status);

			if (!response.ok) {
				let errorDetail = 'Error desconocido al subir el archivo';
				try {
					const errorData = await response.json();
					errorDetail = errorData.detail || `Error ${response.status}`;
				} catch (e) {
					console.error('No se pudo parsear el JSON de error');
				}
				throw new Error(errorDetail);
			}

			const data = await response.json();
			console.log('Respuesta completa del servidor:', data);

			if (!data.url || !data.document_id) {
				throw new Error('Respuesta inválida del servidor: faltan datos.');
			}

			// Construir la URL completa usando el origen actual (manejado por el proxy)
			pdfUrl = data.url; // La URL ya viene prefijada con /uploads/
			documentId = data.document_id;
			pdfLoaded = true;
			console.log('PDF cargado exitosamente:', pdfUrl, 'ID:', documentId);
		} catch (error) {
			console.error('Error en la subida:', error);
			uploadError = error instanceof Error ? error.message : 'Error desconocido';
			file = null;
			pdfUrl = null;
			pdfLoaded = false;
		} finally {
			isUploading = false;
		}
	}

	// Función para verificar si una URL es válida y accesible
	async function checkUrl(url: string): Promise<boolean> {
		try {
			// Usar la URL relativa para que el proxy la maneje
			const response = await fetch(url, { method: 'HEAD' });
			return response.ok;
		} catch (error) {
			console.error('Error verificando URL:', error);
			return false;
		}
	}

	// Verificar la URL del PDF cuando cambie y esté cargado
	$: if (pdfUrl && pdfLoaded) {
		checkUrl(pdfUrl).then((isValid) => {
			if (!isValid) {
				console.error('La URL del PDF no es accesible:', pdfUrl);
				// Opcional: Mostrar error al usuario
				// uploadError = "No se pudo cargar el PDF desde el servidor.";
				// pdfUrl = null;
				// pdfLoaded = false;
			} else {
				console.log('URL del PDF verificada y accesible');
			}
		});
	}
</script>

<!-- Landing Page -->
<div class="landing-page">
	<!-- Hero Section -->
	<section class="hero-section">
		<div class="hero-content">
			<h1>¿Ahogado en PDFs? Tu Lector Inteligente para Entender Más Rápido.</h1>
			<p>
				Extrae ideas clave, aclara dudas y encuentra respuestas sin esfuerzo. La IA que necesitas,
				integrada directamente en tu lector de PDF del navegador.
			</p>

			<div class="hero-buttons">
				<button class="btn-upload" on:click={navigateToPDFUpload}>Sube un PDF ahora</button>
				<a href="#features" class="btn-demo">
					<span class="icon-play">▶</span>
					Ver Demo Rápida
				</a>
			</div>
		</div>

		<div class="hero-demo">
			<div class="pdf-preview">
				<div class="preview-header">
					<div class="dots">
						<span class="dot"></span>
						<span class="dot"></span>
						<span class="dot"></span>
					</div>
					<span class="filename">Informe_Trimestral_Q2_2023.pdf</span>
				</div>
				<div class="preview-content">
					<h3>Resumen Ejecutivo</h3>
					<p>
						El segundo trimestre de 2023 ha mostrado resultados positivos en todas las áreas de
						negocio, con un crecimiento del 12% en comparación con el mismo período del año
						anterior.
					</p>
					<p>
						El análisis de mercado indica que nuestra estrategia de expansión regional ha sido
						efectiva, resultando en un aumento del 18% en nuevos clientes y una retención del 94% de
						la base existente.
					</p>
				</div>
			</div>
		</div>
	</section>

	<!-- Features Section -->
	<section class="features-section" id="features">
		<h2>Presentamos PDFlex: La Forma Inteligente y Simple de Leer PDFs</h2>

		<p class="features-intro">
			PDFlex transforma tu lector de PDF habitual. Integra un asistente IA directamente en tu flujo
			de trabajo. Selecciona cualquier texto y obtén al instante:
		</p>

		<div class="features-grid">
			<div class="feature-card">
				<div class="feature-num">1</div>
				<h3>Resume al Instante</h3>
				<p>
					Convierte párrafos o páginas enteras en puntos clave en segundos. Perfecto para informes,
					artículos y contratos.
				</p>
			</div>

			<div class="feature-card">
				<div class="feature-num">2</div>
				<h3>Explica con Claridad</h3>
				<p>
					Descompila jerga técnica, legal o conceptos difíciles. Entiende todo sin buscar fuera del
					documento.
				</p>
			</div>

			<div class="feature-card">
				<div class="feature-num">3</div>
				<h3>Pregunta y Encuentra Rápido</h3>
				<p>
					¿Buscas un dato específico? Pregúntale directamente al texto seleccionado. Obtén
					respuestas precisas al momento.
				</p>
			</div>
		</div>
	</section>

	<!-- Call to Action -->
	<section class="cta-section">
		<!-- Contenedor principal que ajusta su altura (se muestra cuando se carga un PDF) -->
		<div class="flex flex-col" style="height: calc(100vh - 64px);">
			<!-- Ajusta 64px a la altura real de tu header -->
			<!-- Sección de carga solo visible si no hay PDF cargado -->
			{#if !pdfLoaded}
				<div class="bg-background flex flex-grow flex-col items-center justify-center p-8">
					<h1 class="text-primary-text mb-2 text-center text-3xl font-bold">
						PDFIndex: Tu Lector Inteligente de PDF
					</h1>
					<p class="text-secondary-text mb-6 max-w-xl text-center text-lg">
						Sube un PDF para extraer ideas, resumir contenido y obtener respuestas al instante con
						IA.
					</p>

					<div class="w-full max-w-md">
						<label
							for="pdf-upload"
							class="text-accent border-accent hover:bg-accent flex cursor-pointer flex-col items-center rounded-lg border bg-white px-4 py-6 shadow transition duration-300 ease-in-out hover:text-white"
						>
							<svg
								class="mb-2 h-8 w-8"
								fill="currentColor"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
							>
								<path
									d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z"
								/>
							</svg>
							<span class="text-base font-semibold leading-normal">
								{#if isUploading}
									Procesando...
								{:else}
									Selecciona o arrastra un PDF
								{/if}
							</span>
							<input
								id="pdf-upload"
								type="file"
								class="hidden"
								accept="application/pdf"
								on:change={handleFileUpload}
								disabled={isUploading}
							/>
						</label>

						{#if file && !isUploading}
							<p class="text-secondary-text mt-2 text-center text-sm">
								Archivo seleccionado: {file.name}
							</p>
						{/if}

						{#if uploadError}
							<div class="mt-4 rounded bg-red-100 p-2 text-center text-red-700">
								{uploadError}
							</div>
						{/if}
					</div>
				</div>
			{/if}

			<!-- Visor de PDF (ocupa todo el espacio disponible cuando está cargado) -->
			{#if pdfLoaded && pdfUrl}
				<div class="relative flex-grow">
					<!-- Contenedor absoluto para PDFSlick -->
					<div class="absolute inset-0">
						<ContextualPdfViewer {pdfUrl} {documentId} />
					</div>
				</div>
			{/if}
		</div>
	</section>
</div>

<!-- Estilos globales específicos si son necesarios (pueden ir en app.css) -->
<style>
	/* Variables de colores correctas */
	:root {
		--color-background: #faf4ea;
		--color-primary: #747c71;
		--color-secondary: #8a7769;
		--color-accent: #4a6b8a;
		--color-text: #333333;
		--color-text-light: #666666;
		--color-white: #ffffff;
	}

	.landing-page {
		background-color: var(--color-background);
		color: var(--color-text);
		font-family: 'Inter', system-ui, sans-serif;
	}

	/* Hero Section */
	.hero-section {
		padding: 4rem 2rem;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 2rem;
		max-width: 1200px;
		margin: 0 auto;
	}

	.hero-content {
		flex: 1;
		min-width: 300px;
	}

	.hero-content h1 {
		font-size: 2.5rem;
		font-weight: 700;
		line-height: 1.2;
		margin-bottom: 1.5rem;
		color: var(--color-text);
	}

	.hero-content p {
		font-size: 1.1rem;
		line-height: 1.6;
		margin-bottom: 2rem;
		color: var(--color-text-light);
	}

	.hero-buttons {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
	}

	.btn-upload {
		background-color: var(--color-accent);
		color: var(--color-white);
		border: none;
		border-radius: 6px;
		padding: 0.75rem 1.5rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.btn-upload:hover {
		filter: brightness(90%);
	}

	.btn-demo {
		background-color: transparent;
		color: var(--color-accent);
		border: 2px solid var(--color-accent);
		border-radius: 6px;
		padding: 0.75rem 1.5rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		transition: all 0.2s ease;
		text-decoration: none;
	}

	.btn-demo:hover {
		background-color: var(--color-accent);
		color: var(--color-white);
	}

	.icon-play {
		font-size: 0.8rem;
	}

	.hero-demo {
		flex: 1;
		min-width: 300px;
		max-width: 500px;
	}

	.pdf-preview {
		background-color: var(--color-white);
		border-radius: 8px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		overflow: hidden;
	}

	.preview-header {
		background-color: #f5f5f5;
		padding: 0.75rem 1rem;
		display: flex;
		align-items: center;
	}

	.dots {
		display: flex;
		gap: 0.25rem;
		margin-right: 1rem;
	}

	.dot {
		width: 12px;
		height: 12px;
		border-radius: 50%;
		background-color: #ccc;
	}

	.dot:nth-child(1) {
		background-color: #ff5f57;
	}

	.dot:nth-child(2) {
		background-color: #ffbd2e;
	}

	.dot:nth-child(3) {
		background-color: #28ca41;
	}

	.filename {
		font-size: 0.85rem;
		color: #666;
	}

	.preview-content {
		padding: 1.5rem;
	}

	.preview-content h3 {
		margin-top: 0;
		margin-bottom: 1rem;
		color: var(--color-text);
	}

	.preview-content p {
		font-size: 0.95rem;
		line-height: 1.6;
		margin-bottom: 1rem;
		color: var(--color-text-light);
	}

	/* Features Section */
	.features-section {
		padding: 5rem 2rem;
		text-align: center;
		max-width: 1200px;
		margin: 0 auto;
	}

	.features-section h2 {
		font-size: 2rem;
		font-weight: 700;
		margin-bottom: 1rem;
		color: var(--color-text);
	}

	.features-intro {
		max-width: 800px;
		margin: 0 auto 3rem;
		font-size: 1.1rem;
		line-height: 1.6;
		color: var(--color-text-light);
	}

	.features-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 2rem;
	}

	.feature-card {
		background-color: var(--color-white);
		border-radius: 8px;
		padding: 2rem;
		text-align: left;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
	}

	.feature-num {
		width: 40px;
		height: 40px;
		background-color: var(--color-accent);
		color: var(--color-white);
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 700;
		margin-bottom: 1rem;
	}

	.feature-card h3 {
		font-size: 1.3rem;
		margin-bottom: 0.75rem;
		color: var(--color-text);
	}

	.feature-card p {
		color: var(--color-text-light);
		line-height: 1.6;
	}

	/* CTA Section */
	.cta-section {
		padding: 4rem 2rem;
		text-align: center;
		background-color: var(--color-background);
		border-top: 1px solid rgba(0, 0, 0, 0.05);
		margin-top: 2rem;
	}

	.cta-section p {
		font-size: 1.3rem;
		font-weight: 600;
		margin-bottom: 1.5rem;
		color: var(--color-text);
	}

	/* Responsive Adjustments */
	@media (max-width: 768px) {
		.hero-section {
			flex-direction: column;
			padding: 3rem 1.5rem;
		}

		.hero-content h1 {
			font-size: 2rem;
		}

		.hero-demo {
			width: 100%;
		}

		.features-section {
			padding: 3rem 1.5rem;
		}

		.features-section h2 {
			font-size: 1.75rem;
		}
	}

	/* Asegurar que los estilos de PDFSlick no entren en conflicto */
	:global(.pdfSlickContainer) {
		position: absolute !important; /* Necesario para el contenedor absoluto */
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: #e0e0e0; /* Fondo mientras carga el PDF */
	}
	:global(.pdfSlickViewer) {
		margin: 0 !important; /* Sobreescribir márgenes si los hubiera */
	}
</style>
