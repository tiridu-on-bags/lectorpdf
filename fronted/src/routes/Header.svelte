<script lang="ts">
	import { page } from '$app/stores'; // Corregido de $app/state a $app/stores
	import { onMount } from 'svelte';
	// La importación del logo no es necesaria si lo sirves desde /static
</script>

<header class="header-container">
	<nav>
		<div class="logo-container">
			<a href="/">
				<!-- Actualizado para usar el SVG desde /static -->
				<img src="/pdfindex.svg" alt="PDF INDEX" class="logo" />
			</a>
		</div>
		<ul>
			<li aria-current={$page.url.pathname.startsWith('/pdf') ? 'page' : undefined}>
				<a href="/pdf">PDF</a>
			</li>
			<li aria-current={$page.url.pathname.startsWith('/simple-upload') ? 'page' : undefined}>
				<a href="/simple-upload">Subida Simple</a>
			</li>
		</ul>
	</nav>
</header>

<style>
	/* Variables de colores mantenidas */
	:root {
		--color-ebony: #2c332d;
		--color-sage: #747c71;
		--color-cream: #f9f4e9;
		--color-khaki: #6d5542;
	}

	.header-container {
		display: flex;
		width: 100%;
		background-color: var(--color-ebony);
		padding: 0.5rem 1rem;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	nav {
		display: flex;
		width: 100%;
		justify-content: space-between;
		align-items: center; /* Alineación vertical centrada */
	}

	/* Optimizado para SVG */
	.logo-container {
		background-color: rgba(231, 223, 206, 0.1);
		height: 100px; /* Altura fija en pixels para precisión */
		padding-right: 0.1rem; /* Espacio de separación con la navegación */
		display: flex;
		align-items: center;
		border-radius: 15px;
	}
	.logo {
		height: 100%; /* SVG se ajusta a la altura del contenedor */
		width: auto; /* Mantiene proporción automáticamente */
		max-width: 180px; /* Limita el ancho máximo */
		filter: contrast(1.2) brightness(0.9) drop-shadow(0 0 1px rgba(0, 0, 0, 0.5));
	}
	
	ul {
		display: flex;
		align-items: center;
		list-style: none;
		margin: 0;
		padding: 0;
		height: 3em;
	}

	li {
		position: relative;
		height: 100%;
	}

	li[aria-current='page']::before {
		--size: 6px;
		content: '';
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-top: var(--size) solid var(--color-khaki);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.8rem;
		color: var(--color-cream);
		font-weight: 700;
		font-size: 0.9rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-khaki);
	}
</style>
