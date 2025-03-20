// Configuración simplificada sin adaptador específico
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		// Usando configuración mínima sin adaptador específico
	}
};

export default config;