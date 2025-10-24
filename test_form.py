import streamlit as st
import sys
import os

# Agregar el directorio app al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from validators.patterns import (
    validate_email, validate_phone, validate_date, 
    validate_dni, validate_postal_code, validate_url,
    validate_all_fields, extract_numbers, clean_text
)

# Configuración de la página
st.set_page_config(
    page_title="Validador de Patrones",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🔍 Validador de Patrones de Formulario")
st.markdown("---")

# Crear dos columnas
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Formulario de Validación")
    
    # Formulario
    with st.form("validation_form"):
        email = st.text_input(
            "📧 Correo Electrónico",
            placeholder="usuario@ejemplo.com",
            help="Patrón complejo con caracteres especiales permitidos"
        )
        
        phone = st.text_input(
            "📱 Número Telefónico",
            placeholder="+1234567890",
            help="Formato: + seguido de 8 a 15 dígitos"
        )
        
        date = st.text_input(
            "📅 Fecha",
            placeholder="15/12/2023",
            help="Formato: DD/MM/YYYY o DD/MM/-YYYY"
        )
        
        dni = st.text_input(
            "🆔 DNI",
            placeholder="12345678A",
            help="4 a 18 caracteres alfanuméricos en mayúsculas"
        )
        
        postal_code = st.text_input(
            "📮 Código Postal",
            placeholder="28001",
            help="3 a 9 dígitos"
        )
        
        url = st.text_input(
            "🔗 URL",
            placeholder="https://www.ejemplo.com/path?param=valor",
            help="Patrón completo con esquema, usuario, host, etc."
        )
        
        submitted = st.form_submit_button("🔍 Validar Campos", use_container_width=True)

with col2:
    st.header("📊 Resultados de Validación")
    
    if submitted:
        # Validar todos los campos
        data = {
            'email': email,
            'phone': phone,
            'date': date,
            'dni': dni,
            'postal_code': postal_code,
            'url': url
        }
        
        results = validate_all_fields(data)
        
        # Mostrar resultados
        for field, result in results.items():
            if result['value']:  # Solo mostrar campos con valor
                field_names = {
                    'email': '📧 Email',
                    'phone': '📱 Teléfono',
                    'date': '📅 Fecha',
                    'dni': '🆔 DNI',
                    'postal_code': '📮 Código Postal',
                    'url': '🔗 URL'
                }
                
                field_name = field_names.get(field, field)
                value = result['value']
                is_valid = result['valid']
                
                if is_valid is True:
                    st.success(f"{field_name}: ✅ **VÁLIDO** - `{value}`")
                elif is_valid is False:
                    st.error(f"{field_name}: ❌ **INVÁLIDO** - `{value}`")
                else:
                    st.warning(f"{field_name}: ⚠️ **DESCONOCIDO** - `{value}`")
        
        # Resumen general
        st.markdown("---")
        valid_count = sum(1 for r in results.values() if r['valid'] is True)
        invalid_count = sum(1 for r in results.values() if r['valid'] is False)
        total_filled = sum(1 for r in results.values() if r['value'])
        
        if total_filled > 0:
            st.metric("Campos Válidos", f"{valid_count}/{total_filled}")
            if invalid_count > 0:
                st.metric("Campos Inválidos", invalid_count)

# Sección de herramientas adicionales
st.markdown("---")
st.header("🛠️ Herramientas Adicionales")

col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("🔢 Extraer Números")
    text_input = st.text_area(
        "Texto para extraer números:",
        placeholder="Mi teléfono es 123-456-7890 y mi código postal es 28001",
        height=100
    )
    
    if st.button("Extraer Números"):
        if text_input:
            numbers = extract_numbers(text_input)
            if numbers:
                st.success(f"Números encontrados: {', '.join(numbers)}")
            else:
                st.info("No se encontraron números en el texto")
        else:
            st.warning("Por favor, ingresa algún texto")

with col4:
    st.subheader("🧹 Limpiar Texto")
    clean_input = st.text_area(
        "Texto para limpiar:",
        placeholder="¡Hola! Este es un texto con caracteres especiales @#$%",
        height=100
    )
    
    if st.button("Limpiar Texto"):
        if clean_input:
            cleaned = clean_text(clean_input)
            st.success(f"Texto limpio: `{cleaned}`")
        else:
            st.warning("Por favor, ingresa algún texto")

# Casos de prueba predefinidos
st.markdown("---")
st.header("🧪 Casos de Prueba Predefinidos")

test_cases = {
    "✅ Casos Válidos": {
        "email": "usuario@ejemplo.com",
        "phone": "+1234567890",
        "date": "15/12/2023",
        "dni": "12345678A",
        "postal_code": "28001",
        "url": "https://www.ejemplo.com/path?param=valor"
    },
    "❌ Casos Inválidos": {
        "email": "email-invalido",
        "phone": "1234567890",  # Sin +
        "date": "2023/12/15",   # Formato incorrecto
        "dni": "123",           # Muy corto
        "postal_code": "12",    # Muy corto
        "url": "ejemplo.com"    # Sin esquema
    }
}

for case_type, test_data in test_cases.items():
    st.subheader(case_type)
    
    # Crear botones para cada caso de prueba
    cols = st.columns(len(test_data))
    for i, (field, value) in enumerate(test_data.items()):
        with cols[i]:
            field_names = {
                'email': '📧 Email',
                'phone': '📱 Teléfono',
                'date': '📅 Fecha',
                'dni': '🆔 DNI',
                'postal_code': '📮 Código Postal',
                'url': '🔗 URL'
            }
            
            if st.button(f"{field_names[field]}\n`{value}`", key=f"{case_type}_{field}"):
                # Validar el campo específico
                validators = {
                    'email': validate_email,
                    'phone': validate_phone,
                    'date': validate_date,
                    'dni': validate_dni,
                    'postal_code': validate_postal_code,
                    'url': validate_url
                }
                
                is_valid = validators[field](value)
                if is_valid:
                    st.success(f"✅ {field_names[field]} es VÁLIDO")
                else:
                    st.error(f"❌ {field_names[field]} es INVÁLIDO")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔍 Validador de Patrones - Implementado con Python y Streamlit</p>
</div>
""", unsafe_allow_html=True)
