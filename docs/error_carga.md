# Error de pantalla blanca al iniciar la aplicación

**Descripción**
Al arrancar la app en modo desarrollo con SSR habilitado, la página queda en blanco y sólo se ve contenido tras recargar manualmente.

## Pasos para replicar y solucionar (5 pasos)

1. Clona el repositorio y ejecuta:
   ```bash
   npm install
   npm run dev
   ```
2. Abre el navegador en `http://localhost:3000` y observa que la UI no se muestra (pantalla en blanco).
3. Abre las herramientas de desarrollo (DevTools) y en la consola verás un error similar a:
   ```text
   Access is denied for this document. Failed to read the 'localStorage' property from 'Window'.
   ```
4. Edita `src/routes/+layout.ts`, envuelve el acceso a `localStorage` en un guard `if (browser)` y un bloque `try/catch`, o simplemente desactiva el SSR añadiendo:
   ```ts
   import { browser } from '$app/environment';
   export const ssr = false;
   ```
5. Guarda los cambios, recarga la página y confirma que la aplicación se carga correctamente sin pantalla en blanco.

---

**Notas**
- Con `export const ssr = false;` fuerzas que todo el render sea en cliente y evitas errores de SSR.
- Para mantener SSR y seguridad, solo accede a `localStorage` dentro de:
  ```ts
  if (browser) {
    try {
      // localStorage...
    } catch { /* fallback */ }
  }
  ```
