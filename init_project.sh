#!/bin/bash

# Script de inicialización del proyecto LectorPDF

echo "Iniciando configuración del proyecto LectorPDF..."

# Crear directorios necesarios
echo "Creando directorios..."
mkdir -p backend/uploads
mkdir -p backend/vector_db
mkdir -p fronted/public

# Verificar y configurar permisos
echo "Configurando permisos..."
chmod 755 backend/uploads
chmod 755 backend/vector_db

# Verificar variables de entorno
echo "Verificando variables de entorno..."
if [ ! -f "backend/.env" ]; then
    echo "Creando archivo .env para backend..."
    cat > backend/.env << EOL
OPENAI_API_KEY=your_api_key_here
UPLOAD_DIR=uploads
VECTOR_DIR=vector_db
EOL
fi

if [ ! -f "fronted/.env" ]; then
    echo "Creando archivo .env para fronted..."
    cat > fronted/.env << EOL
VITE_API_URL=http://localhost:8000
EOL
fi

# Verificar dependencias del backend
echo "Verificando dependencias del backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Verificar dependencias del frontend
echo "Verificando dependencias del frontend..."
cd ../fronted
npm install

echo "Configuración completada. Para iniciar el proyecto:"
echo "1. Backend: cd backend && source venv/bin/activate && uvicorn app:app --reload --port 8000 --host 0.0.0.0"
echo "   NOTA: Siempre usar app.py como punto de entrada del backend"
echo "2. Frontend: cd fronted && npm run dev" 