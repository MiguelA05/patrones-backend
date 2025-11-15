#!/bin/bash

# Script para ejecutar la aplicación Streamlit
# Asegúrate de tener el entorno virtual activado

echo "🚀 Iniciando aplicación LaboraUQ..."
echo ""

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "✅ Activando entorno virtual..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "✅ Activando entorno virtual..."
    source venv/bin/activate
fi

# Verificar que streamlit esté instalado
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit no está instalado. Instalando..."
    pip install streamlit
fi

echo "📱 La aplicación se abrirá en http://localhost:8501"
echo "⏹️  Presiona Ctrl+C para detener la aplicación"
echo ""

# Ejecutar la aplicación
streamlit run professional_registration_form.py --server.port 8501

