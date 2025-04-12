# Solución de Problemas de Integración Backend-Frontend para Subida de PDFs

## Problema Original
La aplicación presentaba problemas de conexión entre el backend (FastAPI) y el frontend (SvelteKit) específicamente en la funcionalidad de subida y visualización de PDFs.

### Síntomas
1. Error 404 en la subida de archivos
2. PDFs no se mostraban después de la subida
3. Errores de CORS
4. Conflictos con múltiples frameworks (Gradio + FastAPI)

## Solución Implementada

### 1. Limpieza del Backend
```python
# Eliminación de código innecesario
- Removido Gradio y sus dependencias
- Simplificación de la estructura de la API
```

### 2. Corrección de Rutas
```python
# Estructura correcta de rutas
backend/
├── app.py             # Configuración principal
├── pdf_routes.py      # Rutas específicas para PDFs
└── uploads/           # Directorio para archivos
```

### 3. Configuración de Archivos Estáticos
```python
# En app.py
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
```

### 4. Manejo de CORS
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Plan de Acción para Futuros Desarrollos

### 1. Verificación Inicial
- [ ] Confirmar que el directorio `uploads` existe y tiene permisos correctos
- [ ] Verificar que las rutas no tienen prefijos duplicados
- [ ] Comprobar la configuración CORS
- [ ] Validar las URLs en el frontend

### 2. Estructura del Proyecto
```
proyecto/
├── backend/
│   ├── app.py
│   ├── pdf_routes.py
│   └── uploads/
├── fronted/
│   └── src/
│       └── routes/
│           └── pdf/
└── docs/
```

### 3. Endpoints API
- `GET /api/health` - Verificación del estado del servidor
- `POST /api/upload-pdf` - Subida de PDFs
- `GET /uploads/{filename}` - Acceso a archivos estáticos

### 4. Manejo de Errores
```typescript
try {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
    },
    body: formData
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Error: ${response.status} - ${errorText}`);
  }
} catch (error) {
  console.error('Error:', error);
}
```

## Mejores Prácticas

### Backend
1. Usar logging detallado
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

2. Separar rutas por funcionalidad
```python
app.include_router(pdf_router, prefix="/api")
```

3. Manejar archivos estáticos correctamente
```python
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR))
```

### Frontend
1. Usar rutas relativas
```typescript
const endpoint = '/api/upload-pdf';
```

2. Manejar respuestas del servidor
```typescript
const data = await response.json();
pdfUrl = `http://localhost:8000${data.url}`;
```

3. Implementar manejo de errores robusto
```typescript
if (!response.ok) {
  const errorText = await response.text();
  throw new Error(`Error: ${response.status} - ${errorText}`);
}
```

## Checklist de Verificación
- [ ] Backend corriendo en puerto correcto
- [ ] Rutas API configuradas correctamente
- [ ] CORS configurado para desarrollo
- [ ] Directorio de uploads existente y con permisos
- [ ] Frontend usando rutas correctas
- [ ] Manejo de errores implementado
- [ ] Logs activados para debugging

## Notas Adicionales
- Mantener separación clara entre servicios
- Implementar logging extensivo
- Usar tipos TypeScript en el frontend
- Mantener documentación actualizada
- Realizar pruebas de integración

## Referencias
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SvelteKit Documentation](https://kit.svelte.dev/)
- [CORS Configuration](https://fastapi.tiangolo.com/tutorial/cors/)
- [Static Files in FastAPI](https://fastapi.tiangolo.com/tutorial/static-files/) 