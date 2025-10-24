import streamlit as st
import sys
import os
from datetime import datetime

# Agregar el directorio app al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from validators.patterns import (
    validate_email, validate_phone, validate_date, 
    validate_dni, validate_postal_code, validate_url,
    validate_all_fields
)

# Configuración de la página
st.set_page_config(
    page_title="LaboraUQ",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para estilo profesional
st.markdown("""
<style>
    /* Estilo profesional tipo LinkedIn */
    .main-header {
        background: linear-gradient(135deg, #0077b5 0%, #005885 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 4px 20px rgba(0, 119, 181, 0.3);
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
        margin: 0.5rem 0 0 0;
    }
    
    .section-title {
        color: #0077b5;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e1e5e9;
    }
    
    .url-input-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    
    .add-url-btn {
        background: #0077b5;
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
        background: #005885;
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
        color: #28a745;
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
        border-left: 4px solid #0077b5;
        margin: 1rem 0;
    }
    
    .validation-summary h4 {
        color: #0077b5;
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
        background: #d4edda;
        color: #155724;
    }
    
    .stat-invalid {
        background: #f8d7da;
        color: #721c24;
    }
    
    .stat-missing {
        background: #fff3cd;
        color: #856404;
    }
    
    .submit-btn {
        background: linear-gradient(135deg, #0077b5 0%, #005885 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 2rem;
    }
    
    .submit-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 119, 181, 0.4);
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>LaboraUQ</h1>
    <p>Únete a nuestra comunidad profesional y conecta con oportunidades</p>
</div>
""", unsafe_allow_html=True)

# Inicializar el estado de la sesión para URLs dinámicas
if 'portfolio_urls' not in st.session_state:
    st.session_state.portfolio_urls = [""]

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Inicializar estado para campos interactuados
if 'fields_interacted' not in st.session_state:
    st.session_state.fields_interacted = set()

# Función para agregar nueva URL
def add_portfolio_url():
    st.session_state.portfolio_urls.append("")

# Función para remover URL
def remove_portfolio_url(index):
    if len(st.session_state.portfolio_urls) > 1:
        st.session_state.portfolio_urls.pop(index)

# Función mejorada para validar campo en tiempo real
def validate_field(value, validator_func, field_name, is_required=False):
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

# Función para mostrar feedback visual solo cuando hay cambios
def show_validation_feedback_conditional(icon, message, status, show_empty=False):
    if status == "success":
        st.markdown(f'<div class="validation-success">{icon} {message}</div>', unsafe_allow_html=True)
    elif status == "error":
        st.markdown(f'<div class="validation-error">{icon} {message}</div>', unsafe_allow_html=True)
    elif status == "warning":
        st.markdown(f'<div class="validation-warning">{icon} {message}</div>', unsafe_allow_html=True)
    elif show_empty and status == "neutral":
        st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

# Función inteligente para mostrar validación solo cuando es necesario
def show_smart_validation(field_name, value, validator_func, is_required=False, display_name=None):
    # Usar display_name si se proporciona, sino usar field_name
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

# Función para mostrar feedback visual mejorado
def show_validation_feedback(icon, message, status):
    if status == "success":
        st.markdown(f'<div class="validation-success">{icon} {message}</div>', unsafe_allow_html=True)
    elif status == "error":
        st.markdown(f'<div class="validation-error">{icon} {message}</div>', unsafe_allow_html=True)
    elif status == "warning":
        st.markdown(f'<div class="validation-warning">{icon} {message}</div>', unsafe_allow_html=True)

# Función para validar todos los campos y mostrar resumen
def validate_all_form_fields():
    validation_summary = {
        'valid': 0,
        'invalid': 0,
        'required_missing': 0,
        'total': 0
    }
    
    # Campos obligatorios
    required_fields = {
        'nombre': nombre,
        'email': email,
        'telefono': telefono,
        'profesion': profesion,
        'experiencia': experiencia
    }
    
    # Validar campos obligatorios
    for field_name, value in required_fields.items():
        validation_summary['total'] += 1
        if not value:
            validation_summary['required_missing'] += 1
        elif field_name == 'email' and value:
            if validate_email(value):
                validation_summary['valid'] += 1
            else:
                validation_summary['invalid'] += 1
        elif field_name == 'telefono' and value:
            if validate_phone(value):
                validation_summary['valid'] += 1
            else:
                validation_summary['invalid'] += 1
        else:
            validation_summary['valid'] += 1
    
    # Validar campos opcionales
    optional_fields = {
        'fecha_nacimiento': fecha_nacimiento,
        'dni': dni,
        'codigo_postal': codigo_postal
    }
    
    for field_name, value in optional_fields.items():
        if value:
            validation_summary['total'] += 1
            if field_name == 'fecha_nacimiento':
                if validate_date(value):
                    validation_summary['valid'] += 1
                else:
                    validation_summary['invalid'] += 1
            elif field_name == 'dni':
                if validate_dni(value):
                    validation_summary['valid'] += 1
                else:
                    validation_summary['invalid'] += 1
            elif field_name == 'codigo_postal':
                if validate_postal_code(value):
                    validation_summary['valid'] += 1
                else:
                    validation_summary['invalid'] += 1
    
    # Validar URLs de portafolio
    for url in st.session_state.portfolio_urls:
        if url:
            validation_summary['total'] += 1
            if validate_url(url):
                validation_summary['valid'] += 1
            else:
                validation_summary['invalid'] += 1
    
    return validation_summary

# Contenedor del formulario
with st.container():
    st.markdown('<div>', unsafe_allow_html=True)
    
    # Información Personal
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
        
        # Validación inteligente del email (solo muestra mensajes cuando es necesario)
        show_smart_validation("email", email, validate_email, is_required=True, display_name="Email")
    
    with col2:
        telefono = st.text_input(
            "Teléfono *",
            placeholder="+1234567890",
            help="Número con código de país"
        )
        
        # Validación inteligente del teléfono (solo muestra mensajes cuando es necesario)
        show_smart_validation("telefono", telefono, validate_phone, is_required=True, display_name="Teléfono")
        
        fecha_nacimiento = st.text_input(
            "Fecha de Nacimiento",
            placeholder="DD/MM/YYYY",
            help="Formato: DD/MM/YYYY"
        )
        
        # Validación inteligente de la fecha (solo muestra mensajes cuando es necesario)
        show_smart_validation("fecha_nacimiento", fecha_nacimiento, validate_date, display_name="Fecha")
    
    # Información Profesional
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
    
    # Información de Documentos
    st.markdown('<div class="section-title">Documentos</div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        dni = st.text_input(
            "DNI/Pasaporte",
            placeholder="12345678A",
            help="Documento de identidad"
        )
        
        # Validación inteligente del DNI (solo muestra mensajes cuando es necesario)
        show_smart_validation("dni", dni, validate_dni, display_name="DNI")
    
    with col6:
        codigo_postal = st.text_input(
            "Código Postal",
            placeholder="28001",
            help="Código postal de tu ubicación"
        )
        
        # Validación inteligente del código postal (solo muestra mensajes cuando es necesario)
        show_smart_validation("codigo_postal", codigo_postal, validate_postal_code, display_name="Código Postal")
    
    # Enlaces de Portafolio (Campo Dinámico)
    st.markdown('<div class="section-title">Enlaces de Portafolio o Proyectos Personales</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div>
        <p style="color: #6c757d; margin-bottom: 1rem;">
            <strong>Comparte tus proyectos:</strong> GitHub, LinkedIn, sitio web personal, proyectos destacados, etc.
        </p>
    """, unsafe_allow_html=True)
    
    # Campos dinámicos para URLs
    for i, url in enumerate(st.session_state.portfolio_urls):
        col_url, col_btn = st.columns([5, 1])
        
        with col_url:
            st.session_state.portfolio_urls[i] = st.text_input(
                f"URL {i+1}",
                value=url,
                placeholder="https://github.com/usuario/proyecto",
                key=f"url_{i}",
                help="Enlace a tu proyecto o portafolio"
            )
            
            # Validación inteligente de la URL (solo muestra mensajes cuando es necesario)
            if st.session_state.portfolio_urls[i]:
                show_smart_validation(f"url_{i}", st.session_state.portfolio_urls[i], validate_url, display_name="URL")
        
        with col_btn:
            if len(st.session_state.portfolio_urls) > 1:
                # Usar st.empty() para crear espacio y luego el botón
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
    
    # Información Adicional
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
    
    # Resumen de Validación
    st.markdown('<div class="section-title">Estado de Validación</div>', unsafe_allow_html=True)
    
    validation_summary = validate_all_form_fields()
    
    st.markdown(f"""
    <div class="validation-summary">
        <h4>Resumen de Validación</h4>
        <p>Estado actual de todos los campos del formulario:</p>
        <div class="validation-stats">
            <div class="stat-item stat-valid">Válidos: {validation_summary['valid']}</div>
            <div class="stat-item stat-invalid">Inválidos: {validation_summary['invalid']}</div>
            <div class="stat-item stat-missing">Obligatorios faltantes: {validation_summary['required_missing']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Términos y Condiciones
    st.markdown('<div class="section-title">📋 Términos y Condiciones</div>', unsafe_allow_html=True)
    
    acepto_terminos = st.checkbox(
        "Acepto los términos y condiciones y la política de privacidad *",
        help="Debes aceptar los términos para continuar"
    )
    
    recibir_notificaciones = st.checkbox(
        "Deseo recibir notificaciones sobre oportunidades laborales",
        help="Te enviaremos ofertas de trabajo relevantes"
    )
    
    # Botón de envío
    if st.button("🚀 Completar Registro", key="submit_btn"):
        # Validar campos obligatorios
        campos_obligatorios = {
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'profesion': profesion,
            'experiencia': experiencia
        }
        
        campos_faltantes = [campo for campo, valor in campos_obligatorios.items() if not valor]
        
        if campos_faltantes:
            st.error(f"Por favor completa los campos obligatorios: {', '.join(campos_faltantes)}")
        elif not acepto_terminos:
            st.error("Debes aceptar los términos y condiciones para continuar")
        else:
            # Validar todos los campos con patrones
            data_to_validate = {
                'email': email,
                'phone': telefono,
                'date': fecha_nacimiento,
                'dni': dni,
                'postal_code': codigo_postal
            }
            
            # Filtrar campos vacíos
            data_to_validate = {k: v for k, v in data_to_validate.items() if v}
            
            validation_results = validate_all_fields(data_to_validate)
            
            # Validar URLs de portafolio
            portfolio_validation = []
            for url in st.session_state.portfolio_urls:
                if url:
                    portfolio_validation.append(validate_url(url))
            
            # Verificar si hay errores de validación
            validation_errors = []
            for field, result in validation_results.items():
                if not result['valid']:
                    validation_errors.append(f"{field}: {result['value']}")
            
            if portfolio_validation and not all(portfolio_validation):
                validation_errors.append("URLs de portafolio: Algunas URLs son inválidas")
            
            if validation_errors:
                st.error("Errores de validación encontrados:")
                for error in validation_errors:
                    st.error(f"• {error}")
            else:
                # Registro exitoso
                st.session_state.form_submitted = True
                st.success("¡Registro completado exitosamente!")
                
                # Mostrar resumen
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

# Footer
st.markdown("""
<div style="text-align: center; color: #6c757d; margin-top: 3rem; padding: 2rem;">
    <p>Professional Network - Conectando talentos con oportunidades</p>
    <p style="font-size: 0.9rem;">© 2024 Professional Network. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
