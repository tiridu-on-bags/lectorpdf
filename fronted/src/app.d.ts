// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

// Declaración para el módulo PDF.js importado dinámicamente
declare module '/pdfjs/pdf.mjs' {
    const pdfjsLib: unknown;
    export default pdfjsLib;
}

export {};
