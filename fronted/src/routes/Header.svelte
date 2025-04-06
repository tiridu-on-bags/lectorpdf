<script lang="ts">
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import logo from '$lib/images/pdfindex.svg';
	import pdfindex from '$lib/images/pdfindex.jpg';
</script>

<header class="header-container">
	<nav>
		<ul>
			<li aria-current={page.url.pathname === '/' ? 'page' : undefined}>
				<div class="fill corner">
					<a href="/">
						<img src={logo} alt="PDF Index" class="" />
					</a>
				</div>
			</li>
			<li aria-current={page.url.pathname.startsWith('/pdf') ? 'page' : undefined}>
				<a href="/pdf">PDF</a>
			</li>
			<li aria-current={page.url.pathname.startsWith('/simple-upload') ? 'page' : undefined}>
				<a href="/simple-upload">Subida Simple</a>
			</li>
		</ul>
	</nav>
</header>

<style>
	/* Definir variables con la paleta de colores */
	:root {
		--color-ebony: #2c332d;
		--color-sage: #747c71;
		--color-cream: #f9f4e9;
		--color-khaki: #6d5542;
	}

	.header-container {
		display: flex;
		width: 100%;
		background-color: var(--color-ebony); /* Fondo oscuro para contrastar */
		padding: 0.5rem 1rem;
		margin: 0;
		box-sizing: border-box;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	nav {
		display: flex;
		width: 100%;
		justify-content: space-between;
		--background: transparent; /* Anula el background anterior */
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: transparent; /* Fondo transparente para mostrar el color del header */
		width: 100%;
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
		border-top: var(--size) solid var(--color-khaki); /* Cambiado del theme original */
	}

	.corner {
		width: 3em;
		height: 3em;
		background-color: var(--color-cream);
		border-radius: 50%;
		border: 2px solid var(--color-khaki);
		padding: 0.3rem;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
		transition: transform 0.2s ease;
	}

	.corner:hover {
		transform: scale(1.05);
	}

	.corner img {
		width: 2.2em;
		height: 2.2em;
		object-fit: contain;
		filter: brightness(0.9); /* Ajusta para mayor contraste si es necesario */
	}

	.corner img {
		width: 2.2em; /* Aumentado para mayor visibilidad */
		height: 2.2em;
		object-fit: contain;
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.8rem;
		color: var(--color-cream); /* Texto claro para contrastar con fondo oscuro */
		font-weight: 700;
		font-size: 0.9rem; /* Ligeramente más grande */
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-khaki); /* Color de hover más cálido */
	}
</style>
