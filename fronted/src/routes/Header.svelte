<script lang="ts">
	import PdfIndexLogo from './PdfIndexLogo.svelte';
	import Document from './Document.svelte';
	import User from './User.svelte';
	import { page } from '$app/stores'; // Corregido de $app/state a $app/stores
	import { onMount } from 'svelte';
	// La importación del logo no es necesaria si lo sirves desde /static
</script>

<header class="header-container">
	<nav>
		<div class="logo-container flex items-center">
			<a href="/">
				<!-- Actualizado para usar el SVG desde /static 
				<img src="/pdfindex.svg" alt="PDF INDEX" class="logo" />
				-->
				<PdfIndexLogo size={50} rounded={100} className="logo" />
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
			<!--
			<li aria-current={$page.url.pathname.startsWith('/simple-upload') ? 'page' : undefined}>
				<a href="/simple-upload">Subida Simple</a>
			</li>
			-->
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

<style>
	/* Variables de colores mantenidas */
	:root {
		--color-ebony: #4A6B8A;
		--color-sage: #747c71;
		--color-cream: #f9f4e9;
		--color-khaki: #FFBD2D;
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
		/*background-color: rgba(231, 223, 206, 0.1);*/
		height: 100px; /* Altura fija en pixels para precisión */
		padding-right: 0.1rem; /* Espacio de separación con la navegación */
		display: flex;
		align-items: center;
		/*border-radius: 15px;  Para la circulación del logo, se circula con silueta si se activa background-color: rgba(231, 223, 206, 0.1);*/
		border: 2px solid transparent; /* Borde inicial transparente */
		transition: filter 0.2s ease; /* Animación suave del color de borde */
	}

	/* Cambiar color del borde al pasar el cursor o al hacer tap 
	:global(.logo-container:hover) {
		filter: brightness(1.1);
	}*/

	:global(.logo) {
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

	/* Efecto hover sutil: iluminar ligeramente el logo */
	:global(.logo-container:hover svg) {
		filter: brightness(1.1);
	}

	/* Uncomment below to add silhouette fill on hover: */
	/* :global(.logo-container:hover) { background-color: var(--color-khaki); } */

	/* Hover de enlaces con color principal de acento */
	nav a:hover {
		color: var(--color-ebony);
		/* opcional: opacity: 0.8; */
	}

	/* Circular white background for nav icons */
	:global(nav a .nav-icon) {
		width: 2.5rem;
		height: 2.5rem;
		background-color: var(--color-white);
		border-radius: 50%;
		display: flex;
		justify-content: center;
		align-items: center;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		transition: filter 0.2s ease;
		/* Color the icon paths to match header background */
		color: var(--color-ebony);
	}

	/* Brighten icon on hover of link */
	:global(nav a:hover .nav-icon) {
		
		filter: brightness(1.2);
	}

	/* Container for nav icons: white circle like logo */
	:global(.nav-icon-container) {
		width: 3.5rem;
		height: 3.5rem;
		background-color: #faf4ea;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		transition: filter 0.2s ease;
	}

	/* Slight brightness on hover container */
	:global(.nav-icon-container:hover) {
		filter: brightness(1.05);
	}

	/* Icon inside container smaller */
	:global(.nav-icon-container .nav-icon) {
		width: 1.2rem;
		height: 1.2rem;
	}
</style>
