#!/usr/bin/env python3
"""
Script para ejecutar el formulario profesional de registro mejorado
"""

import subprocess
import sys
import os

def main():
    """Ejecuta el formulario profesional de registro con validación mejorada"""
    print("🚀 Iniciando formulario profesional de registro mejorado...")
    print("💼 Professional Network - Plataforma de Networking Laboral")
    print()
    
    # Verificar que streamlit esté instalado
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} encontrado")
    except ImportError:
        print("❌ Streamlit no está instalado. Instálalo con:")
        print("   pip install streamlit")
        sys.exit(1)
    
    # Ejecutar la aplicación
    try:
        print("🌐 Abriendo formulario profesional en el navegador...")
        print("📱 El formulario estará disponible en: http://localhost:8501")
        print("⏹️  Presiona Ctrl+C para detener la aplicación")
        print()
        print("🎯 Nuevas características del formulario:")
        print("   • ✅ Validación en tiempo real mejorada")
        print("   • ⚠️ Notificaciones de campos obligatorios")
        print("   • 📊 Resumen de validación en tiempo real")
        print("   • 🔗 Campos dinámicos para URLs de portafolio")
        print("   • 🎨 Diseño profesional estilo LinkedIn")
        print("   • 🔍 Validación completa con patrones regex")
        print()
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "professional_registration_form.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--theme.base", "light",
            "--theme.primaryColor", "#0077b5",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f8f9fa"
        ])
    except KeyboardInterrupt:
        print("\n👋 Formulario detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar el formulario: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
