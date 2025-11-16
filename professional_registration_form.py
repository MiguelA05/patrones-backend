"""
Formulario de Registro Profesional - LaboraUQ

Este módulo contiene la aplicación Streamlit para el registro de profesionales
en la plataforma LaboraUQ. Incluye validación en tiempo real de campos,
interfaz adaptada a los colores del logo y gestión de campos dinámicos.

CAMPOS CON VALIDACIÓN DE PATRÓN (Expresiones Regulares):
Los siguientes campos tienen validación mediante patrones definidos en 
app/validators/patterns.py (líneas 9-40):

1. Email (PATTERN_EMAIL) - Obligatorio
2. Teléfono (PATTERN_PHONE) - Obligatorio  
3. Fecha de Nacimiento (PATTERN_DATE) - Obligatorio
4. DNI/Pasaporte (PATTERN_DNI) - Obligatorio
5. Código Postal (PATTERN_POSTAL_CODE) - Obligatorio
6. URLs de Portafolio (PATTERN_URL) - Obligatorio (al menos una URL)

Los demás campos (nombre, profesión, experiencia, etc.) solo tienen
validación de requerido, sin validación de patrón.

Autor: LaboraUQ Development Team
Fecha: 2024
"""

import streamlit as st
import sys
import os
import base64

# Agregar el directorio raíz al path para importar los módulos
sys.path.insert(0, os.path.dirname(__file__))

from app.validators.patterns import (
    validate_email, validate_phone, validate_date, 
    validate_dni, validate_postal_code, validate_url
)

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="LaboraUQ",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# ESTILOS CSS PERSONALIZADOS
# =============================================================================
# Los estilos están adaptados a la paleta de colores del logo LaboraUQ:
# - Azul oscuro (#1a365d, #2c5282): Colores principales
# - Verde (#10b981, #059669): Acentos y elementos interactivos
# - Fondo oscuro (#0f172a, #1e293b): Para mejor contraste y legibilidad
st.markdown("""
<style>
    /* Fondo oscuro para mejor contraste */
    .stApp {
        background-color: #0f172a;
    }
    
    .main .block-container {
        background-color: #1e293b;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Estilo adaptado a los colores del logo LaboraUQ */
    .main-header {
        background: linear-gradient(135deg, #1a365d 0%, #2c5282 50%, #1a365d 100%);
        padding: 3rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 4px 20px rgba(26, 54, 93, 0.4);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        margin-bottom: 0;
    }
    
    .logo-img {
        height: 220px;
        width: auto;
        max-width: 500px;
        object-fit: contain;
        filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.4));
        background: transparent;
        mix-blend-mode: normal;
    }
    
    @media (max-width: 768px) {
        .logo-img {
            height: 140px;
            max-width: 350px;
        }
        .main-header {
            padding: 2rem 0;
        }
    }
    
    @media (max-width: 480px) {
        .logo-img {
            height: 120px;
            max-width: 300px;
        }
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 300;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 1.1rem;
        font-weight: bold;
        margin: 0.2rem 0 0 0;
    }
    
    .section-title {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #10b981;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        letter-spacing: 0.5px;
    }
    
    .add-url-btn {
        background: #10b981;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 1.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .add-url-btn:hover {
        background: #059669;
        transform: scale(1.1);
    }
    
    .remove-url-btn {
        background: #dc3545;
        color: white;
        border: none;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .remove-url-btn:hover {
        background: #c82333;
        transform: scale(1.1);
    }
    
    .validation-success {
        color: #10b981;
        font-size: 0.9rem;
    }
    
    .validation-error {
        color: #dc3545;
        font-size: 0.9rem;
    }
    
    .validation-warning {
        color: #ffc107;
        font-size: 0.9rem;
    }
    
    .validation-summary {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1a365d;
        margin: 1rem 0;
    }
    
    .validation-summary h4 {
        color: #1a365d;
        margin: 0 0 0.5rem 0;
    }
    
    .validation-stats {
        display: flex;
        gap: 1rem;
        margin-top: 0.5rem;
    }
    
    .stat-item {
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: 600;
    }
    
    .stat-valid {
        background: #d1fae5;
        color: #065f46;
    }
    
    .stat-invalid {
        background: #f8d7da;
        color: #721c24;
    }
    
    .stat-missing {
        background: #fff3cd;
        color: #856404;
    }
    
    /* Botones de Streamlit con colores del logo */
    .stButton > button {
        background: linear-gradient(135deg, #1a365d 0%, #2c5282 50%, #10b981 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2c5282 0%, #1a365d 50%, #059669 100%);
        box-shadow: 0 4px 12px rgba(26, 54, 93, 0.4);
    }
    
    /* Checkbox con colores del logo */
    .stCheckbox > label {
        color: #1a365d;
    }
    
    .stCheckbox > div[data-baseweb="checkbox"] {
        background-color: #10b981;
    }
    
    /* Estilos para campos de entrada - Sin borde rojo por defecto */
    /* Usar selectores muy específicos para sobrescribir estilos de Streamlit */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    div[data-baseweb="base-input"] > div > input,
    div[data-baseweb="base-input"] > div > textarea,
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        border: 1px solid #4a5568 !important;
        border-color: #4a5568 !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    /* Sobrescribir cualquier estilo de error por defecto de Streamlit */
    .stTextInput > div > div > input[aria-invalid="false"],
    .stTextArea > div > div > textarea[aria-invalid="false"],
    .stSelectbox > div > div > select[aria-invalid="false"],
    .stTextInput > div > div > input:not([aria-invalid="true"]),
    .stTextArea > div > div > textarea:not([aria-invalid="true"]),
    .stSelectbox > div > div > select:not([aria-invalid="true"]),
    div[data-baseweb="base-input"] > div > input:not([aria-invalid="true"]),
    div[data-baseweb="base-input"] > div > textarea:not([aria-invalid="true"]) {
        border-color: #4a5568 !important;
    }
    
    /* Forzar que los campos sin clase de validación no tengan borde rojo */
    .stTextInput:not(.field-error) > div > div > input,
    .stTextArea:not(.field-error) > div > div > textarea,
    .stSelectbox:not(.field-error) > div > div > select,
    .stTextInput:not(.field-error) input,
    .stTextArea:not(.field-error) textarea,
    .stSelectbox:not(.field-error) select,
    .stTextInput:not(.field-error) > div[data-baseweb="base-input"] > div > input,
    .stTextArea:not(.field-error) > div[data-baseweb="base-input"] > div > textarea {
        border-color: #4a5568 !important;
    }
    
    /* Cuando el campo está enfocado pero sin validar aún - borde azul */
    .stTextInput:not(.field-valid):not(.field-error) > div > div > input:focus,
    .stTextArea:not(.field-valid):not(.field-error) > div > div > textarea:focus,
    .stSelectbox:not(.field-valid):not(.field-error) > div > div > select:focus,
    .stTextInput:not(.field-valid):not(.field-error) input:focus,
    .stTextArea:not(.field-valid):not(.field-error) textarea:focus,
    .stSelectbox:not(.field-valid):not(.field-error) select:focus,
    .stTextInput:not(.field-error):not(.field-valid) > div[data-baseweb="base-input"] > div > input:focus,
    .stTextArea:not(.field-error):not(.field-valid) > div[data-baseweb="base-input"] > div > textarea:focus {
        border-color: #2c5282 !important;
        box-shadow: 0 0 0 2px rgba(44, 82, 130, 0.2) !important;
        outline: none !important;
    }
    
    /* Campo válido - borde verde (tiene prioridad sobre focus) */
    .stTextInput.field-valid > div > div > input,
    .stTextArea.field-valid > div > div > textarea,
    .stSelectbox.field-valid > div > div > select,
    .stTextInput.field-valid > div > div > input:focus,
    .stTextArea.field-valid > div > div > textarea:focus,
    .stSelectbox.field-valid > div > div > select:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2) !important;
        outline: none !important;
    }
    
    /* Campo con error - borde rojo (solo cuando hay error real) */
    .stTextInput.field-error > div > div > input,
    .stTextArea.field-error > div > div > textarea,
    .stSelectbox.field-error > div > div > select,
    .stTextInput.field-error > div > div > input:focus,
    .stTextArea.field-error > div > div > textarea:focus,
    .stSelectbox.field-error > div > div > select:focus {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.2) !important;
        outline: none !important;
    }
    
    /* Campo con advertencia - borde amarillo */
    .stTextInput.field-warning > div > div > input,
    .stTextArea.field-warning > div > div > textarea,
    .stSelectbox.field-warning > div > div > select,
    .stTextInput.field-warning > div > div > input:focus,
    .stTextArea.field-warning > div > div > textarea:focus,
    .stSelectbox.field-warning > div > div > select:focus {
        border-color: #ffc107 !important;
        box-shadow: 0 0 0 2px rgba(255, 193, 7, 0.2) !important;
        outline: none !important;
    }
</style>
""", unsafe_allow_html=True)

def load_logo():
    """
    Carga el logo de LaboraUQ desde el directorio de assets.
    
    Busca el logo en diferentes formatos (PNG, SVG) y ubicaciones.
    Si encuentra el logo, lo convierte a base64 para mostrarlo en el header.
    
    Returns:
        tuple: (logo_data, mime_type) si se encuentra el logo, (None, None) en caso contrario
    """
    logo_formats = ["laborauq_logo.png", "laborauq_logo.svg", "logo.png", "logo.svg"]
    assets_dir = os.path.join(os.path.dirname(__file__), "assets", "images")
    
    for logo_file in logo_formats:
        potential_path = os.path.join(assets_dir, logo_file)
        if os.path.exists(potential_path):
            try:
                with open(potential_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode()
                
                if logo_file.endswith(".svg"):
                    mime_type = "image/svg+xml"
                else:
                    mime_type = "image/png"
                
                return img_data, mime_type
            except Exception:
                continue
    
    return None, None


def render_header():
    """
    Renderiza el header principal de la aplicación con el logo de LaboraUQ.
    
    Si el logo está disponible, lo muestra junto con el subtítulo.
    Si no está disponible, muestra solo el texto del título y subtítulo.
    """
    logo_data, logo_mime_type = load_logo()
    
    if logo_data and logo_mime_type:
        st.markdown(f"""
        <div class="main-header">
            <div class="logo-container">
                <img src="data:{logo_mime_type};base64,{logo_data}" class="logo-img" alt="LaboraUQ Logo" />
            </div>
            <p>Únete a nuestra comunidad profesional y conecta con oportunidades</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="main-header">
            <h1>LaboraUQ</h1>
            <p>Únete a nuestra comunidad profesional y conecta con oportunidades</p>
        </div>
        """, unsafe_allow_html=True)


# Renderizar header principal
render_header()

# =============================================================================
# INICIALIZACIÓN DEL ESTADO DE LA SESIÓN
# =============================================================================

def initialize_session_state():
    """
    Inicializa las variables de estado de la sesión de Streamlit.
    
    Variables inicializadas:
    - portfolio_urls: Lista de URLs de portafolio (inicia con un campo vacío)
    - fields_interacted: Conjunto de nombres de campos que han sido interactuados
    """
    if 'portfolio_urls' not in st.session_state:
        st.session_state.portfolio_urls = [""]
    
    if 'fields_interacted' not in st.session_state:
        st.session_state.fields_interacted = set()


initialize_session_state()


# =============================================================================
# FUNCIONES DE GESTIÓN DE URLs DE PORTAFOLIO
# =============================================================================

def add_portfolio_url():
    """
    Agrega un nuevo campo de URL de portafolio a la lista dinámica.
    
    La función agrega una cadena vacía a la lista de URLs en el estado
    de la sesión, permitiendo que el usuario agregue múltiples URLs.
    """
    st.session_state.portfolio_urls.append("")


def remove_portfolio_url(index: int):
    """
    Elimina un campo de URL de portafolio de la lista.
    
    Args:
        index (int): Índice del campo a eliminar
        
    Nota:
        No permite eliminar el último campo (siempre debe haber al menos uno)
    """
    if len(st.session_state.portfolio_urls) > 1:
        st.session_state.portfolio_urls.pop(index)


# =============================================================================
# FUNCIONES DE VALIDACIÓN Y FEEDBACK VISUAL
# =============================================================================

def validate_field(value: str, validator_func, field_name: str, is_required: bool = False) -> tuple:
    """
    Valida un campo individual y retorna el resultado de la validación.
    
    Args:
        value (str): Valor del campo a validar
        validator_func: Función de validación a aplicar (ej: validate_email)
        field_name (str): Nombre del campo para mensajes de error
        is_required (bool): Indica si el campo es obligatorio
        
    Returns:
        tuple: (icono, mensaje, estado) donde:
            - icono: Emoji o símbolo representativo (✅, ❌, ⚠️)
            - mensaje: Mensaje descriptivo del estado
            - estado: "success", "error", "warning" o "neutral"
    """
    if not value:
        if is_required:
            return "⚠️", f"{field_name} es obligatorio", "warning"
        else:
            return "", "", "neutral"
    
    is_valid = validator_func(value)
    if is_valid:
        return "✅", f"{field_name} válido", "success"
    else:
        return "❌", f"{field_name} inválido", "error"


def show_validation_feedback_conditional(icon: str, message: str, status: str, show_empty: bool = False):
    """
    Muestra feedback visual de validación con estilos personalizados.
    
    Args:
        icon (str): Icono o emoji a mostrar
        message (str): Mensaje de validación
        status (str): Estado de validación ("success", "error", "warning", "neutral")
        show_empty (bool): Si es True, muestra espacio en blanco para estado neutral
    """
    if status == "success":
        st.markdown(f'<div class="validation-success">{icon} {message}</div>', unsafe_allow_html=True)
    elif status == "error":
        st.markdown(f'<div class="validation-error">{icon} {message}</div>', unsafe_allow_html=True)
    elif status == "warning":
        st.markdown(f'<div class="validation-warning">{icon} {message}</div>', unsafe_allow_html=True)
    elif show_empty and status == "neutral":
        st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)


def apply_validation_styles():
    """
    Inyecta un script JavaScript global que aplica clases CSS a los campos
    basándose en los mensajes de validación cercanos.
    """
    st.markdown("""
    <script>
    (function() {
        // Interceptar y sobrescribir estilos de Streamlit de forma agresiva
        function forceCorrectBorderColors() {
            document.querySelectorAll('input, textarea, select').forEach(function(input) {
                const container = input.closest('.stTextInput, .stTextArea, .stSelectbox');
                if (!container) return;
                
                const computedStyle = window.getComputedStyle(input);
                const borderColor = computedStyle.borderColor;
                const isFocused = document.activeElement === input;
                
                // Detectar si Streamlit aplicó un borde rojo
                const isRedBorder = borderColor.includes('220') || borderColor.includes('rgb(220') || 
                                   borderColor.includes('#dc') || borderColor.toLowerCase().includes('red');
                
                // Si no hay validación y no está enfocado, forzar borde gris
                if (!container.classList.contains('field-valid') && 
                    !container.classList.contains('field-error') && 
                    !container.classList.contains('field-warning')) {
                    if (!isFocused && isRedBorder) {
                        // Forzar borde gris
                        input.style.setProperty('border-color', '#4a5568', 'important');
                        input.style.setProperty('box-shadow', '', 'important');
                    } else if (isFocused && !isRedBorder) {
                        // Si está enfocado y no es rojo, aplicar azul
                        input.style.setProperty('border-color', '#2c5282', 'important');
                        input.style.setProperty('box-shadow', '0 0 0 2px rgba(44, 82, 130, 0.2)', 'important');
                    } else if (!isFocused && !isRedBorder) {
                        // Si no está enfocado y no es rojo, aplicar gris
                        input.style.setProperty('border-color', '#4a5568', 'important');
                        input.style.setProperty('box-shadow', '', 'important');
                    }
                }
            });
        }
        
        function applyFieldValidationStyles() {
            // Buscar todos los campos de entrada
            const fieldContainers = document.querySelectorAll('.stTextInput, .stTextArea, .stSelectbox');
            
            fieldContainers.forEach(function(container) {
                // Primero, remover todas las clases de validación
                container.classList.remove('field-valid', 'field-error', 'field-warning');
                
                // Buscar el mensaje de validación más cercano después del campo
                // En Streamlit, los mensajes suelen estar en el siguiente elemento hermano
                let found = false;
                let current = container;
                let validationStatus = null;
                
                // Buscar en el siguiente elemento hermano directo
                let next = current.nextElementSibling;
                let maxSearch = 5; // Limitar la búsqueda a los siguientes 5 elementos
                let searchCount = 0;
                
                while (next && !found && searchCount < maxSearch) {
                    // Buscar mensajes de validación directamente en el elemento
                    const directMsg = next.querySelector && next.querySelector('.validation-success, .validation-error, .validation-warning');
                    if (directMsg) {
                        found = true;
                        if (directMsg.classList.contains('validation-success')) {
                            validationStatus = 'valid';
                            container.classList.add('field-valid');
                        } else if (directMsg.classList.contains('validation-error')) {
                            validationStatus = 'error';
                            container.classList.add('field-error');
                        } else if (directMsg.classList.contains('validation-warning')) {
                            validationStatus = 'warning';
                            container.classList.add('field-warning');
                        }
                        break;
                    }
                    
                    // También verificar si el elemento mismo es un mensaje de validación
                    if (next.classList && (
                        next.classList.contains('validation-success') ||
                        next.classList.contains('validation-error') ||
                        next.classList.contains('validation-warning')
                    )) {
                        found = true;
                        if (next.classList.contains('validation-success')) {
                            validationStatus = 'valid';
                            container.classList.add('field-valid');
                        } else if (next.classList.contains('validation-error')) {
                            validationStatus = 'error';
                            container.classList.add('field-error');
                        } else if (next.classList.contains('validation-warning')) {
                            validationStatus = 'warning';
                            container.classList.add('field-warning');
                        }
                        break;
                    }
                    
                    next = next.nextElementSibling;
                    searchCount++;
                }
                
                // Aplicar estilos directamente a los inputs para sobrescribir estilos inline
                const inputs = container.querySelectorAll('input, textarea, select');
                inputs.forEach(function(input) {
                    // Remover cualquier estilo inline de borde que Streamlit pueda haber aplicado
                    if (input.style.borderColor && !validationStatus) {
                        input.style.borderColor = '';
                    }
                    
                    // Aplicar estilos según el estado de validación
                    if (validationStatus === 'valid') {
                        input.style.borderColor = '#10b981';
                        input.style.boxShadow = '0 0 0 2px rgba(16, 185, 129, 0.2)';
                    } else if (validationStatus === 'error') {
                        input.style.borderColor = '#dc3545';
                        input.style.boxShadow = '0 0 0 2px rgba(220, 53, 69, 0.2)';
                    } else if (validationStatus === 'warning') {
                        input.style.borderColor = '#ffc107';
                        input.style.boxShadow = '0 0 0 2px rgba(255, 193, 7, 0.2)';
                    } else {
                        // Sin validación: borde gris por defecto
                        input.style.borderColor = '#4a5568';
                        input.style.boxShadow = '';
                    }
                });
            });
        }
        
        // Función para manejar el focus de los campos
        function handleFieldFocus() {
            document.querySelectorAll('.stTextInput input, .stTextArea textarea, .stSelectbox select').forEach(function(input) {
                const container = input.closest('.stTextInput, .stTextArea, .stSelectbox');
                if (container) {
                    // Solo aplicar borde azul si no tiene clase de validación
                    if (!container.classList.contains('field-valid') && 
                        !container.classList.contains('field-error') && 
                        !container.classList.contains('field-warning')) {
                        input.addEventListener('focus', function() {
                            this.style.borderColor = '#2c5282';
                            this.style.boxShadow = '0 0 0 2px rgba(44, 82, 130, 0.2)';
                        });
                        input.addEventListener('blur', function() {
                            // Restaurar el color según el estado de validación
                            setTimeout(function() {
                                applyFieldValidationStyles();
                            }, 50);
                        });
                    }
                }
            });
        }
        
        // Función para aplicar estilos cuando cambia el input
        function setupInputListeners() {
            document.querySelectorAll('.stTextInput input, .stTextArea textarea, .stSelectbox select').forEach(function(input) {
                // Solo agregar listeners si no los tiene ya
                if (!input.hasAttribute('data-validation-listener')) {
                    input.setAttribute('data-validation-listener', 'true');
                    
                    // Agregar listener para cuando el usuario escribe
                    input.addEventListener('input', function() {
                        setTimeout(applyFieldValidationStyles, 50);
                    });
                    
                    // Agregar listener para cuando el campo pierde el foco
                    input.addEventListener('blur', function() {
                        setTimeout(applyFieldValidationStyles, 50);
                    });
                    
                    // Listener para focus - aplicar borde azul si no hay validación
                    input.addEventListener('focus', function() {
                        const container = this.closest('.stTextInput, .stTextArea, .stSelectbox');
                        if (container && !container.classList.contains('field-valid') && 
                            !container.classList.contains('field-error') && 
                            !container.classList.contains('field-warning')) {
                            this.style.borderColor = '#2c5282';
                            this.style.boxShadow = '0 0 0 2px rgba(44, 82, 130, 0.2)';
                        }
                    });
                }
            });
        }
        
        // Ejecutar cuando el DOM esté listo
        function init() {
            applyFieldValidationStyles();
            setupInputListeners();
            handleFieldFocus();
            observeInputStyles();
            forceCorrectBorderColors();
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
        
        // Ejecutar después de delays para asegurar que Streamlit haya renderizado
        setTimeout(init, 100);
        setTimeout(init, 300);
        setTimeout(init, 600);
        setTimeout(init, 1000);
        
        // Ejecutar periódicamente para forzar estilos y sobrescribir cambios de Streamlit
        setInterval(function() {
            applyFieldValidationStyles();
            forceCorrectBorderColors();
        }, 100); // Ejecutar cada 100ms para ser más agresivo
        
        // Observar cambios en atributos de estilo para interceptar cambios de Streamlit
        const styleObserver = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                    const target = mutation.target;
                    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.tagName === 'SELECT') {
                        setTimeout(forceCorrectBorderColors, 10);
                    }
                }
            });
        });
        
        // Observar todos los inputs para cambios de estilo
        function observeInputStyles() {
            document.querySelectorAll('input, textarea, select').forEach(function(input) {
                styleObserver.observe(input, {
                    attributes: true,
                    attributeFilter: ['style']
                });
            });
        }
        
        // Observar cambios en el DOM para aplicar estilos cuando se agreguen nuevos elementos
        const observer = new MutationObserver(function(mutations) {
            let shouldApply = false;
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) {
                            // Verificar si se agregó un mensaje de validación
                            if (node.classList && (
                                node.classList.contains('validation-success') ||
                                node.classList.contains('validation-error') ||
                                node.classList.contains('validation-warning')
                            )) {
                                shouldApply = true;
                            }
                            // Verificar si se agregó un campo de entrada
                            if (node.classList && (
                                node.classList.contains('stTextInput') ||
                                node.classList.contains('stTextArea') ||
                                node.classList.contains('stSelectbox')
                            )) {
                                shouldApply = true;
                            }
                            // Verificar si contiene mensajes de validación
                            if (node.querySelector && node.querySelector('.validation-success, .validation-error, .validation-warning')) {
                                shouldApply = true;
                            }
                            
                            // Si se agregaron nuevos inputs, observarlos también
                            const newInputs = node.querySelectorAll ? node.querySelectorAll('input, textarea, select') : [];
                            newInputs.forEach(function(input) {
                                styleObserver.observe(input, {
                                    attributes: true,
                                    attributeFilter: ['style']
                                });
                            });
                            // Si el nodo mismo es un input
                            if (node.tagName === 'INPUT' || node.tagName === 'TEXTAREA' || node.tagName === 'SELECT') {
                                styleObserver.observe(node, {
                                    attributes: true,
                                    attributeFilter: ['style']
                                });
                            }
                        }
                    });
                }
            });
            if (shouldApply) {
                setTimeout(function() {
                    applyFieldValidationStyles();
                    setupInputListeners();
                    observeInputStyles();
                    forceCorrectBorderColors();
                }, 100);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    })();
    </script>
    """, unsafe_allow_html=True)


def show_smart_validation(field_name: str, value: str, validator_func, is_required: bool = False, display_name: str = None):
    """
    Muestra validación inteligente que solo aparece cuando es necesario.
    
    Esta función evita mostrar mensajes de validación hasta que el usuario
    haya interactuado con el campo o haya ingresado un valor. Esto mejora
    la experiencia de usuario al no mostrar errores prematuramente.
    
    NOTA: Solo debe usarse con campos que tienen validación de patrón definida
    en app/validators/patterns.py (email, phone, date, dni, postal_code, url).
    
    Args:
        field_name (str): Nombre interno del campo (usado para tracking)
        value (str): Valor actual del campo
        validator_func: Función de validación de patrón a aplicar 
                       (validate_email, validate_phone, validate_date, etc.)
        is_required (bool): Indica si el campo es obligatorio
        display_name (str, optional): Nombre a mostrar en mensajes. 
                                     Si es None, usa field_name
    """
    display_field_name = display_name if display_name else field_name
    
    # Solo mostrar mensajes si el campo ha sido interactuado o tiene valor
    if value or field_name in st.session_state.fields_interacted:
        icon, message, status = validate_field(value, validator_func, display_field_name, is_required)
        show_validation_feedback_conditional(icon, message, status)
        
        # Marcar el campo como interactuado si tiene valor
        if value:
            st.session_state.fields_interacted.add(field_name)
    
    # Para campos obligatorios vacíos, solo mostrar advertencia si ya fueron interactuados
    elif is_required and field_name in st.session_state.fields_interacted:
        icon, message, status = validate_field(value, validator_func, display_field_name, is_required)
        show_validation_feedback_conditional(icon, message, status)

def validate_all_form_fields(email: str, telefono: str, fecha_nacimiento: str, 
                             dni: str, codigo_postal: str, portfolio_urls: list) -> dict:
    """
    Valida únicamente los campos que tienen validación de patrón definida.
    
    Esta función valida SOLO los 6 campos con patrones definidos en 
    app/validators/patterns.py (líneas 9-40). TODOS estos campos son obligatorios:
    
    1. Email (PATTERN_EMAIL) - obligatorio
    2. Teléfono (PATTERN_PHONE) - obligatorio
    3. Fecha de Nacimiento (PATTERN_DATE) - obligatorio
    4. DNI/Pasaporte (PATTERN_DNI) - obligatorio
    5. Código Postal (PATTERN_POSTAL_CODE) - obligatorio
    6. URLs de Portafolio (PATTERN_URL) - obligatorio (al menos una URL)
    
    Args:
        email (str): Correo electrónico
        telefono (str): Número de teléfono
        fecha_nacimiento (str): Fecha de nacimiento
        dni (str): DNI o pasaporte
        codigo_postal (str): Código postal
        portfolio_urls (list): Lista de URLs de portafolio
        
    Returns:
        dict: Diccionario con el resumen de validación conteniendo:
            - valid (int): Cantidad de campos válidos
            - invalid (int): Cantidad de campos inválidos
            - required_missing (int): Cantidad de campos obligatorios faltantes
            - total (int): Total de campos con patrones validados
            - fields_detail (dict): Detalle de cada campo con su estado
    """
    validation_summary = {
        'valid': 0,
        'invalid': 0,
        'required_missing': 0,
        'total': 0,
        'fields_detail': {}
    }
    
    # Campos con validación de patrón (definidos en patterns.py líneas 9-40)
    # 1. Email (obligatorio)
    validation_summary['total'] += 1
    if not email or email.strip() == '':
        validation_summary['required_missing'] += 1
        validation_summary['fields_detail']['email'] = {
            'status': 'missing',
            'display_name': 'Correo Electrónico',
            'message': 'Correo Electrónico es obligatorio'
        }
    else:
        if validate_email(email):
            validation_summary['valid'] += 1
            validation_summary['fields_detail']['email'] = {
                'status': 'valid',
                'display_name': 'Correo Electrónico',
                'message': 'Correo Electrónico es válido'
            }
        else:
            validation_summary['invalid'] += 1
            validation_summary['fields_detail']['email'] = {
                'status': 'invalid',
                'display_name': 'Correo Electrónico',
                'message': 'Correo Electrónico tiene formato inválido'
            }
    
    # 2. Teléfono (obligatorio)
    validation_summary['total'] += 1
    if not telefono or telefono.strip() == '':
        validation_summary['required_missing'] += 1
        validation_summary['fields_detail']['telefono'] = {
            'status': 'missing',
            'display_name': 'Teléfono',
            'message': 'Teléfono es obligatorio'
        }
    else:
        if validate_phone(telefono):
            validation_summary['valid'] += 1
            validation_summary['fields_detail']['telefono'] = {
                'status': 'valid',
                'display_name': 'Teléfono',
                'message': 'Teléfono es válido'
            }
        else:
            validation_summary['invalid'] += 1
            validation_summary['fields_detail']['telefono'] = {
                'status': 'invalid',
                'display_name': 'Teléfono',
                'message': 'Teléfono tiene formato inválido'
            }
    
    # 3. Fecha de Nacimiento (obligatorio)
    validation_summary['total'] += 1
    if not fecha_nacimiento or fecha_nacimiento.strip() == '':
        validation_summary['required_missing'] += 1
        validation_summary['fields_detail']['fecha_nacimiento'] = {
            'status': 'missing',
            'display_name': 'Fecha de Nacimiento',
            'message': 'Fecha de Nacimiento es obligatoria'
        }
    else:
        if validate_date(fecha_nacimiento):
            validation_summary['valid'] += 1
            validation_summary['fields_detail']['fecha_nacimiento'] = {
                'status': 'valid',
                'display_name': 'Fecha de Nacimiento',
                'message': 'Fecha de Nacimiento es válida'
            }
        else:
            validation_summary['invalid'] += 1
            validation_summary['fields_detail']['fecha_nacimiento'] = {
                'status': 'invalid',
                'display_name': 'Fecha de Nacimiento',
                'message': 'Fecha de Nacimiento tiene formato inválido'
            }
    
    # 4. DNI/Pasaporte (obligatorio)
    validation_summary['total'] += 1
    if not dni or dni.strip() == '':
        validation_summary['required_missing'] += 1
        validation_summary['fields_detail']['dni'] = {
            'status': 'missing',
            'display_name': 'DNI/Pasaporte',
            'message': 'DNI/Pasaporte es obligatorio'
        }
    else:
        if validate_dni(dni):
            validation_summary['valid'] += 1
            validation_summary['fields_detail']['dni'] = {
                'status': 'valid',
                'display_name': 'DNI/Pasaporte',
                'message': 'DNI/Pasaporte es válido'
            }
        else:
            validation_summary['invalid'] += 1
            validation_summary['fields_detail']['dni'] = {
                'status': 'invalid',
                'display_name': 'DNI/Pasaporte',
                'message': 'DNI/Pasaporte tiene formato inválido'
            }
    
    # 5. Código Postal (obligatorio)
    validation_summary['total'] += 1
    if not codigo_postal or codigo_postal.strip() == '':
        validation_summary['required_missing'] += 1
        validation_summary['fields_detail']['codigo_postal'] = {
            'status': 'missing',
            'display_name': 'Código Postal',
            'message': 'Código Postal es obligatorio'
        }
    else:
        if validate_postal_code(codigo_postal):
            validation_summary['valid'] += 1
            validation_summary['fields_detail']['codigo_postal'] = {
                'status': 'valid',
                'display_name': 'Código Postal',
                'message': 'Código Postal es válido'
            }
        else:
            validation_summary['invalid'] += 1
            validation_summary['fields_detail']['codigo_postal'] = {
                'status': 'invalid',
                'display_name': 'Código Postal',
                'message': 'Código Postal tiene formato inválido'
            }
    
    # 6. URLs de Portafolio (obligatorio - al menos una URL)
    urls_con_valor = [url for url in portfolio_urls if url and url.strip()]
    if len(urls_con_valor) == 0:
        validation_summary['total'] += 1
        validation_summary['required_missing'] += 1
        validation_summary['fields_detail']['urls_portfolio'] = {
            'status': 'missing',
            'display_name': 'URLs de Portafolio',
            'message': 'Al menos una URL de Portafolio es obligatoria'
        }
    else:
        urls_validas = 0
        urls_invalidas = 0
        for url in urls_con_valor:
            validation_summary['total'] += 1
            if validate_url(url):
                urls_validas += 1
            else:
                urls_invalidas += 1
        
        if urls_invalidas == 0:
            validation_summary['valid'] += urls_validas
            validation_summary['fields_detail']['urls_portfolio'] = {
                'status': 'valid',
                'display_name': 'URLs de Portafolio',
                'message': f'Todas las URLs ({urls_validas}) son válidas'
            }
        else:
            validation_summary['invalid'] += urls_invalidas
            validation_summary['valid'] += urls_validas
            validation_summary['fields_detail']['urls_portfolio'] = {
                'status': 'invalid',
                'display_name': 'URLs de Portafolio',
                'message': f'{urls_invalidas} URL(s) inválida(s) de {urls_validas + urls_invalidas} total'
            }
    
    return validation_summary

# =============================================================================
# FORMULARIO PRINCIPAL
# =============================================================================

# Aplicar estilos de validación a los campos (debe llamarse después de definir la función)
apply_validation_styles()

# Contenedor del formulario
with st.container():
    st.markdown('<div>', unsafe_allow_html=True)
    
    # -------------------------------------------------------------------------
    # SECCIÓN: Información Personal
    # Campos básicos del usuario: nombre, email, teléfono y fecha de nacimiento
    # 
    # Campos con validación de patrón (definidos en patterns.py líneas 9-40):
    # - Email: PATTERN_EMAIL (obligatorio)
    # - Teléfono: PATTERN_PHONE (obligatorio)
    # - Fecha de Nacimiento: PATTERN_DATE (obligatorio)
    # -------------------------------------------------------------------------
    st.markdown('<div class="section-title">Información Personal</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input(
            "Nombre Completo *",
            placeholder="Ej: Juan Pérez García",
            help="Ingresa tu nombre completo"
        )
        
        email = st.text_input(
            "Correo Electrónico *",
            placeholder="ejemplo@empresa.com",
            help="Tu email profesional"
        )
        
        show_smart_validation("email", email, validate_email, is_required=True, display_name="Email")
    
    with col2:
        telefono = st.text_input(
            "Teléfono *",
            placeholder="+1234567890",
            help="Número con código de país"
        )
        
        show_smart_validation("telefono", telefono, validate_phone, is_required=True, display_name="Teléfono")
        
        fecha_nacimiento = st.text_input(
            "Fecha de Nacimiento *",
            placeholder="DD/MM/YYYY",
            help="Formato: DD/MM/YYYY"
        )
        
        show_smart_validation("fecha_nacimiento", fecha_nacimiento, validate_date, is_required=True, display_name="Fecha")
    
    # -------------------------------------------------------------------------
    # SECCIÓN: Información Profesional
    # Datos relacionados con la carrera profesional del usuario
    # -------------------------------------------------------------------------
    st.markdown('<div class="section-title">Información Profesional</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        profesion = st.text_input(
            "Profesión *",
            placeholder="Ej: Desarrollador Full Stack",
            help="Tu título profesional"
        )
        
        empresa_actual = st.text_input(
            "Empresa Actual",
            placeholder="Ej: Tech Solutions Inc.",
            help="Empresa donde trabajas actualmente"
        )
    
    with col4:
        experiencia = st.selectbox(
            "Años de Experiencia *",
            ["", "0-1 años", "2-3 años", "4-5 años", "6-10 años", "11-15 años", "16+ años"]
        )
        
        ubicacion = st.text_input(
            "Ubicación",
            placeholder="Ciudad, País",
            help="Tu ubicación actual"
        )
    
    # -------------------------------------------------------------------------
    # SECCIÓN: Documentos
    # Documentos de identificación y códigos postales
    # 
    # Campos con validación de patrón (definidos en patterns.py líneas 9-40):
    # - DNI/Pasaporte: PATTERN_DNI (obligatorio)
    # - Código Postal: PATTERN_POSTAL_CODE (obligatorio)
    # -------------------------------------------------------------------------
    st.markdown('<div class="section-title">Documentos</div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        dni = st.text_input(
            "DNI/Pasaporte *",
            placeholder="12345678A",
            help="Documento de identidad"
        )
        
        show_smart_validation("dni", dni, validate_dni, is_required=True, display_name="DNI")
    
    with col6:
        codigo_postal = st.text_input(
            "Código Postal *",
            placeholder="28001",
            help="Código postal de tu ubicación"
        )
        
        show_smart_validation("codigo_postal", codigo_postal, validate_postal_code, is_required=True, display_name="Código Postal")
    
    # -------------------------------------------------------------------------
    # SECCIÓN: Enlaces de Portafolio (Campos Dinámicos)
    # Permite agregar múltiples URLs de proyectos, GitHub, LinkedIn, etc.
    # Los campos son dinámicos: el usuario puede agregar o eliminar URLs
    # 
    # Campo con validación de patrón (definido en patterns.py líneas 9-40):
    # - URLs: PATTERN_URL (obligatorio, al menos una URL)
    # -------------------------------------------------------------------------
    st.markdown('<div class="section-title">Enlaces de Portafolio o Proyectos Personales</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div>
        <p style="color: #6c757d; margin-bottom: 1rem;">
            <strong>Comparte tus proyectos (al menos una URL es obligatoria):</strong> GitHub, LinkedIn, sitio web personal, proyectos destacados, etc.
        </p>
    """, unsafe_allow_html=True)
    
    # Campos dinámicos para URLs
    for i, url in enumerate(st.session_state.portfolio_urls):
        col_url, col_btn = st.columns([5, 1])
        
        with col_url:
            label_url = f"URL {i+1} *" if i == 0 else f"URL {i+1}"
            st.session_state.portfolio_urls[i] = st.text_input(
                label_url,
                value=url,
                placeholder="https://github.com/usuario/proyecto",
                key=f"url_{i}",
                help="Enlace a tu proyecto o portafolio" + (" (obligatorio al menos una)" if i == 0 else "")
            )
            
            is_required = (i == 0)
            if st.session_state.portfolio_urls[i] or is_required:
                show_smart_validation(f"url_{i}", st.session_state.portfolio_urls[i], validate_url, is_required=is_required, display_name="URL")
        
        with col_btn:
            if len(st.session_state.portfolio_urls) > 1:
                st.markdown('<div style="height: 2.5rem; display: flex; align-items: center;">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"remove_{i}", help="Eliminar URL"):
                    remove_portfolio_url(i)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="height: 2.5rem;"></div>', unsafe_allow_html=True)
    
    # Botón para agregar nueva URL
    col_add, col_empty = st.columns([2, 8])
    with col_add:
        if st.button("➕ Agregar URL", help="Agregar otro enlace"):
            add_portfolio_url()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # -------------------------------------------------------------------------
    # SECCIÓN: Información Adicional
    # Campos opcionales para biografía y habilidades del usuario
    # -------------------------------------------------------------------------
    st.markdown('<div class="section-title">Información Adicional</div>', unsafe_allow_html=True)
    
    biografia = st.text_area(
        "Biografía Profesional",
        placeholder="Cuéntanos sobre tu experiencia, habilidades y objetivos profesionales...",
        height=100,
        help="Una breve descripción de tu perfil profesional"
    )
    
    habilidades = st.text_input(
        "Habilidades Principales",
        placeholder="Python, JavaScript, React, Node.js, SQL...",
        help="Separa las habilidades con comas"
    )
    
    # -------------------------------------------------------------------------
    # SECCIÓN: Términos y Condiciones
    # Checkboxes para aceptar términos y recibir notificaciones
    # -------------------------------------------------------------------------
    st.markdown('<div class="section-title">📋 Términos y Condiciones</div>', unsafe_allow_html=True)
    
    acepto_terminos = st.checkbox(
        "Acepto los términos y condiciones y la política de privacidad *",
        help="Debes aceptar los términos para continuar"
    )
    
    recibir_notificaciones = st.checkbox(
        "Deseo recibir notificaciones sobre oportunidades laborales",
        help="Te enviaremos ofertas de trabajo relevantes"
    )
    
    # -------------------------------------------------------------------------
    # SECCIÓN: Estado de Validación
    # Muestra un resumen visual del estado de validación de todos los campos obligatorios
    # -------------------------------------------------------------------------
    st.markdown('<div class="section-title">Estado de Validación</div>', unsafe_allow_html=True)
    
    validation_summary = validate_all_form_fields(
        email, telefono, fecha_nacimiento, dni, codigo_postal, st.session_state.portfolio_urls
    )
    
    # Construir lista de todos los campos con su estado
    fields_list_html = '<ul style="list-style: none; padding: 0; margin: 1rem 0;">'
    
    # Orden de campos para mostrar
    field_order = ['email', 'telefono', 'fecha_nacimiento', 'dni', 'codigo_postal', 'urls_portfolio']
    
    for field_name in field_order:
        if field_name in validation_summary['fields_detail']:
            field_detail = validation_summary['fields_detail'][field_name]
            status = field_detail['status']
            display_name = field_detail['display_name']
            
            if status == 'valid':
                icon = '✅'
                color = '#065f46'
                text = f'{display_name} - Válido'
            elif status == 'invalid':
                icon = '❌'
                color = '#721c24'
                text = f'{display_name} - Inválido'
            else:  # missing
                icon = '⚠️'
                color = '#856404'
                text = f'{display_name} - Faltante'
            
            fields_list_html += f'<li style="padding: 0.5rem 0; border-bottom: 1px solid #e5e7eb;"><span style="color: {color}; font-weight: 600;">{icon} {text}</span></li>'
    
    fields_list_html += '</ul>'
    
    st.markdown(f"""
    <div class="validation-summary">
        <h4>Resumen de Validación</h4>
        <p style="margin-bottom: 0.5rem; color: #6c757d; font-size: 0.9rem;">Estado de los campos con validación de patrón:</p>
        {fields_list_html}
    </div>
    """, unsafe_allow_html=True)
    
    # -------------------------------------------------------------------------
    # BOTÓN DE ENVÍO Y PROCESAMIENTO DEL FORMULARIO
    # Valida todos los campos y procesa el registro si es exitoso
    # -------------------------------------------------------------------------
    if st.button("🚀 Completar Registro", key="submit_btn"):
        campos_obligatorios = {
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'profesion': profesion,
            'experiencia': experiencia,
            'fecha_nacimiento': fecha_nacimiento,
            'dni': dni,
            'codigo_postal': codigo_postal
        }
        
        campos_faltantes = [campo for campo, valor in campos_obligatorios.items() if not valor]
        
        if not st.session_state.portfolio_urls or not any(url.strip() for url in st.session_state.portfolio_urls):
            campos_faltantes.append('urls_portfolio')
        
        if campos_faltantes:
            st.error(f"Por favor completa los campos obligatorios: {', '.join(campos_faltantes)}")
        elif not acepto_terminos:
            st.error("Debes aceptar los términos y condiciones para continuar")
        elif validation_summary['invalid'] > 0 or validation_summary['required_missing'] > 0:
            st.error("Por favor corrige los errores de validación antes de continuar")
        else:
            st.success("¡Registro completado exitosamente!")
            
            st.markdown("### Resumen del Registro")
            
            col_summary1, col_summary2 = st.columns(2)
            
            with col_summary1:
                st.write("**Información Personal:**")
                st.write(f"• Nombre: {nombre}")
                st.write(f"• Email: {email}")
                st.write(f"• Teléfono: {telefono}")
                if fecha_nacimiento:
                    st.write(f"• Fecha de Nacimiento: {fecha_nacimiento}")
            
            with col_summary2:
                st.write("**Información Profesional:**")
                st.write(f"• Profesión: {profesion}")
                if empresa_actual:
                    st.write(f"• Empresa: {empresa_actual}")
                st.write(f"• Experiencia: {experiencia}")
                if ubicacion:
                    st.write(f"• Ubicación: {ubicacion}")
            
            st.write("**Enlaces de Portafolio:**")
            for i, url in enumerate(st.session_state.portfolio_urls, 1):
                if url:
                    st.write(f"• URL {i}: {url}")
            
            if biografia:
                st.write("**Biografía:**")
                st.write(biografia)
            
            if habilidades:
                st.write("**Habilidades:**")
                st.write(habilidades)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div style="text-align: center; color: #6c757d; margin-top: 3rem; padding: 2rem;">
    <p>Professional Network - Conectando talentos con oportunidades</p>
    <p style="font-size: 0.9rem;">© 2024 Professional Network. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
