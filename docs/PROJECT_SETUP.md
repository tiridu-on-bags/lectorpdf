# Configuración y Mantenimiento del Proyecto LectorPDF

## Estructura del Proyecto
```
lectorpdf/
├── backend/
│   ├── app.py              # Aplicación principal FastAPI (ÚNICO punto de entrada)
│   ├── pdf_routes.py       # Rutas específicas para PDFs
│   ├── uploads/            # Directorio para archivos PDF
│   ├── vector_db/          # Base de datos vectorial
│   └── .env                # Variables de entorno
├── fronted/
│   ├── src/
│   │   └── routes/
│   │       └── pdf/        # Componentes de PDF
│   └── .env                # Variables de entorno
└── docs/                   # Documentación
```

## Configuración Inicial

1. **Ejecutar el script de inicialización**:
   ```bash
   chmod +x init_project.sh
   ./init_project.sh
   ```

2. **Configurar variables de entorno**:
   - Backend: Editar `backend/.env`
   - Frontend: Editar `fronted/.env`

## Inicio del Proyecto

1. **Iniciar el Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   # IMPORTANTE: Usar app.py como punto de entrada
   uvicorn app:app --reload --port 8000 --host 0.0.0.0
   ```

2. **Iniciar el Frontend**:
   ```bash
   cd fronted
   npm run dev
   ```

## Notas Importantes
- **Siempre usar `app.py` como punto de entrada del backend**
- No usar `api.py` ya que está obsoleto
- El archivo `app.py` contiene toda la configuración necesaria y usa routers para modularizar el código

## Mantenimiento

### Verificación Diaria
- [ ] Verificar que los directorios `uploads` y `vector_db` existen
- [ ] Comprobar que las variables de entorno están configuradas
- [ ] Verificar que los servicios están corriendo en los puertos correctos

### Resolución de Problemas Comunes

1. **Error 404 en subida de PDFs**:
   - Verificar que el backend está corriendo usando `app.py`
   - Comprobar la URL en `fronted/.env`
   - Asegurar que el directorio `uploads` tiene permisos correctos

2. **Problemas de CORS**:
   - Verificar la configuración en `backend/app.py`
   - Asegurar que los orígenes están correctamente configurados

3. **Problemas de Permisos**:
   - Ejecutar `chmod 755` en los directorios necesarios
   - Verificar la propiedad de los archivos

## Mejores Prácticas

1. **Backend**:
   - Usar siempre `app.py` como punto de entrada
   - Mantener el entorno virtual activado
   - Usar logging para debugging
   - Verificar rutas y permisos regularmente

2. **Frontend**:
   - Mantener las dependencias actualizadas
   - Usar variables de entorno para configuraciones
   - Implementar manejo de errores robusto

## Referencias
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SvelteKit Documentation](https://kit.svelte.dev/)
- [Documentación de Solución de Problemas](./pdf-upload-troubleshooting.md) 