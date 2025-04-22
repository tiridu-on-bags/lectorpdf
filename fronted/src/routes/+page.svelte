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

<!-- Contenedor principal que ajusta su altura -->
<div class="flex flex-col" style="height: calc(100vh - 64px);"> <!-- Ajusta 64px a la altura real de tu header -->
	<!-- Sección de carga solo visible si no hay PDF cargado -->
	{#if !pdfLoaded}
		<div class="flex flex-col items-center justify-center flex-grow p-8 bg-background">
			<h1 class="text-3xl font-bold text-primary-text mb-2 text-center">
				PDFIndex: Tu Lector Inteligente de PDF
			</h1>
			<p class="text-lg text-secondary-text mb-6 text-center max-w-xl">
				Sube un PDF para extraer ideas, resumir contenido y obtener respuestas al instante con IA.
			</p>

			<div class="w-full max-w-md">
				<label
					for="pdf-upload"
					class="flex flex-col items-center px-4 py-6 bg-white text-accent rounded-lg shadow border border-accent cursor-pointer hover:bg-accent hover:text-white transition duration-300 ease-in-out"
				>
					<svg class="w-8 h-8 mb-2" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
						<path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
					</svg>
					<span class="font-semibold text-base leading-normal">
						{#if isUploading}
							Procesando...
						{:else}
							Selecciona o arrastra un PDF
						{/if}
					</span>
					<input id="pdf-upload" type="file" class="hidden" accept="application/pdf" on:change={handleFileUpload} disabled={isUploading} />
				</label>

				{#if file && !isUploading}
					<p class="mt-2 text-sm text-center text-secondary-text">Archivo seleccionado: {file.name}</p>
				{/if}

				{#if uploadError}
					<div class="mt-4 text-center p-2 bg-red-100 text-red-700 rounded">
						{uploadError}
					</div>
				{/if}
			</div>
		</div>
	{/if}

	<!-- Visor de PDF (ocupa todo el espacio disponible cuando está cargado) -->
	{#if pdfLoaded && pdfUrl}
		<div class="flex-grow relative">
			<!-- Contenedor absoluto para PDFSlick -->
			<div class="absolute inset-0">
				<ContextualPdfViewer pdfUrl={pdfUrl} documentId={documentId} />
			</div>
		</div>
	{/if}
</div>

<!-- Estilos globales específicos si son necesarios (pueden ir en app.css) -->
<style>
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