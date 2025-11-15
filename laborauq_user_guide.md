# Guía de Uso - LaboraUQ
## Sistema de Validación de Formularios con Expresiones Regulares

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Modos de Uso](#modos-de-uso)
6. [Patrones de Validación](#patrones-de-validación)
7. [Guía de Usuario](#guía-de-usuario)
8. [Guía para Desarrolladores](#guía-para-desarrolladores)
9. [Casos de Prueba](#casos-de-prueba)
10. [Solución de Problemas](#solución-de-problemas)

---

## Descripción General

**LaboraUQ** es una aplicación web desarrollada en Python que implementa un sistema robusto de validación de formularios de registro profesional utilizando expresiones regulares. El sistema está diseñado para plataformas de networking laboral y garantiza la integridad, estructura y formato correcto de los datos personales y profesionales ingresados por los usuarios.

### Características Principales

- Validación en tiempo real de campos del formulario
- Analizador léxico basado en expresiones regulares
- Resumen estadístico de validación
- Interfaz profesional estilo LinkedIn
- Campos dinámicos para URLs de portafolio
- Diseño responsivo y accesible

### Tecnologías Utilizadas

- **Backend**: Python 3.x, FastAPI
- **Frontend**: Streamlit
- **Validación**: Módulo `re` (expresiones regulares)
- **Despliegue**: Streamlit Cloud

---

## Requisitos del Sistema

### Requisitos de Software

- **Python**: 3.8 o superior
- **pip**: Gestor de paquetes de Python
- **Navegador web**: Chrome, Firefox, Safari o Edge (versión actualizada)

### Dependencias de Python

```
streamlit>=1.28.0
fastapi>=0.104.0
pydantic>=2.4.0
uvicorn>=0.24.0
```

---

## Instalación

### Opción 1: Instalación Local

1. **Clonar o descargar el repositorio**:
```bash
git clone <URL_DEL_REPOSITORIO>
cd LaboraUQ
```

2. **Crear un entorno virtual (recomendado)**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install streamlit fastapi pydantic uvicorn
```

4. **Verificar la instalación**:
```bash
python -c "import streamlit; print(streamlit.__version__)"
```

### Opción 2: Uso en Línea

Acceda directamente a la aplicación desplegada en:
**https://laborauq.streamlit.app/**

---

## Estructura del Proyecto

```
LaboraUQ/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints.py          # Endpoints de la API
│   ├── services/
│   │   └── extractor.py              # Servicios de extracción
│   ├── validators/
│   │   └── patterns.py               # Patrones regex y funciones de validación
│   ├── schemas/
│   │   └── request_response.py       # Esquemas de datos
│   └── main.py                       # Configuración principal de FastAPI
│
├── professional_registration_form.py # Formulario principal de Streamlit
├── test_form.py                      # Interfaz de pruebas de validación
├── run_enhanced_form.py              # Script de ejecución del formulario
├── Dockerfile                        # Configuración de Docker
├── .gitignore                        # Archivos ignorados por Git
└── README.md                         # Documentación del proyecto
```

### Descripción de Componentes Clave

#### `app/validators/patterns.py`
Contiene todas las expresiones regulares y funciones de validación:
- Patrones para email, teléfono, fecha, DNI, código postal y URL
- Funciones de validación individuales
- Funciones auxiliares de extracción y limpieza de texto

#### `professional_registration_form.py`
Interfaz principal del formulario con:
- Diseño profesional personalizado con CSS
- Validación interactiva en tiempo real
- Gestión de campos dinámicos (URLs de portafolio)
- Resumen estadístico de validación

#### `test_form.py`
Entorno de pruebas que incluye:
- Validador individual de campos
- Herramientas de extracción de números
- Limpieza de texto
- Casos de prueba predefinidos

---

## Modos de Uso

### Modo 1: Formulario de Registro Completo

**Propósito**: Simular el proceso de registro en una plataforma de networking laboral.

**Cómo ejecutar**:
```bash
streamlit run professional_registration_form.py
```

O utilizar el script de ejecución:
```bash
python run_enhanced_form.py
```

**Acceso**: Abrir navegador en `http://localhost:8501`

**Funcionalidades**:
- Registro completo de información personal y profesional
- Validación automática de todos los campos
- Resumen de estado de validación
- Gestión dinámica de URLs de portafolio
- Confirmación de registro exitoso

### Modo 2: Interfaz de Pruebas

**Propósito**: Probar patrones de validación individuales y herramientas auxiliares.

**Cómo ejecutar**:
```bash
streamlit run test_form.py
```

**Acceso**: Abrir navegador en `http://localhost:8501`

**Funcionalidades**:
- Validación individual de campos
- Extracción de números de texto
- Limpieza de caracteres especiales
- Casos de prueba predefinidos (válidos e inválidos)
- Resultados visuales inmediatos

### Modo 3: API REST (FastAPI)

**Propósito**: Integración con otros sistemas mediante endpoints HTTP.

**Cómo ejecutar**:
```bash
uvicorn app.main:app --reload --port 8000
```

**Acceso**: 
- API: `http://localhost:8000`
- Documentación interactiva: `http://localhost:8000/docs`

**Endpoints disponibles**:
- `GET /`: Mensaje de bienvenida
- `POST /api/v1/extract`: Extracción de patrones de texto

---

## Patrones de Validación

### 1. Correo Electrónico

**Estándares**: RFC 5321, RFC 5322

**Patrón**: Complejo con soporte para caracteres especiales en comillas

**Formato válido**:
- `usuario@dominio.com`
- `nombre.apellido@empresa.co`
- `"usuario+especial"@ejemplo.com`

**Restricciones**:
- Longitud máxima: 254 caracteres
- Debe contener exactamente un símbolo `@`
- Dominio debe tener al menos un punto y extensión de 2+ caracteres
- Cada nivel del dominio: 1-63 caracteres

**Ejemplo de uso**:
```python
from app.validators.patterns import validate_email

email = "usuario@ejemplo.com"
is_valid = validate_email(email)  # True

email_invalido = "usuario@@ejemplo"
is_valid = validate_email(email_invalido)  # False
```

### 2. Número Telefónico

**Estándar**: ITU-T E.164

**Formato válido**:
- `+573001234567` (Colombia)
- `+34912345678` (España)
- `+12025551234` (Estados Unidos)

**Restricciones**:
- Debe iniciar con `+`
- Seguido de 8 a 15 dígitos numéricos
- Sin espacios, guiones ni paréntesis

**Ejemplo de uso**:
```python
from app.validators.patterns import validate_phone

phone = "+573001234567"
is_valid = validate_phone(phone)  # True

phone_invalido = "3001234567"  # Falta el +
is_valid = validate_phone(phone_invalido)  # False
```

### 3. Fecha de Nacimiento

**Formato válido**:
- `DD/MM/YYYY`: `15/08/2000`
- `DD/MM/-YYYY`: `01/01/-500` (fechas antes de Cristo)

**Restricciones**:
- Día: 2 dígitos (01-31)
- Mes: 2 dígitos (01-12)
- Año: 1 o más dígitos, opcionalmente precedido por `-`
- Separador obligatorio: `/`

**Nota**: Esta validación es **sintáctica**, no semántica. No verifica días válidos por mes (ej: acepta `31/02/2024`).

**Ejemplo de uso**:
```python
from app.validators.patterns import validate_date

fecha = "15/08/2000"
is_valid = validate_date(fecha)  # True

fecha_invalida = "2000-08-15"  # Formato incorrecto
is_valid = validate_date(fecha_invalida)  # False
```

### 4. DNI/Identificación Personal

**Formato válido**:
- Alfanumérico en mayúsculas
- Longitud: 4 a 18 caracteres

**Ejemplos válidos**:
- `12345678A` (España)
- `AB123456` (Pasaporte)
- `1095550864` (Colombia)

**Restricciones**:
- Solo letras mayúsculas (A-Z) y números (0-9)
- Sin espacios ni caracteres especiales

**Ejemplo de uso**:
```python
from app.validators.patterns import validate_dni

dni = "12345678A"
is_valid = validate_dni(dni)  # True

dni_invalido = "123"  # Muy corto
is_valid = validate_dni(dni_invalido)  # False
```

### 5. Código Postal

**Formato válido**:
- Solo dígitos numéricos
- Longitud: 3 a 9 dígitos

**Ejemplos válidos**:
- `630001` (Colombia)
- `28001` (España)
- `10001` (Estados Unidos)

**Restricciones**:
- Solo números
- Sin letras ni caracteres especiales

**Ejemplo de uso**:
```python
from app.validators.patterns import validate_postal_code

codigo = "630001"
is_valid = validate_postal_code(codigo)  # True

codigo_invalido = "12"  # Muy corto
is_valid = validate_postal_code(codigo_invalido)  # False
```

### 6. URL (Enlace Web)

**Estándar**: RFC 3986, RFC 1035

**Formato válido**:
- `https://www.ejemplo.com`
- `http://github.com/usuario/proyecto`
- `https://portfolio.dev/proyectos?categoria=web`

**Componentes validados**:
- **Esquema**: `http://` o `https://` (obligatorio)
- **Usuario** (opcional): `usuario@`
- **Host**: Dominio válido con estructura jerárquica
- **Puerto** (opcional): `:8080`
- **Ruta** (opcional): `/path/to/resource`
- **Parámetros** (opcional): `?param=valor`

**Restricciones**:
- Host no puede exceder 255 caracteres
- Cada nivel del dominio: máximo 61 caracteres
- El esquema es obligatorio

**Ejemplo de uso**:
```python
from app.validators.patterns import validate_url

url = "https://github.com/usuario/proyecto"
is_valid = validate_url(url)  # True

url_invalida = "github.com/proyecto"  # Falta esquema
is_valid = validate_url(url_invalida)  # False
```

---

## Guía de Usuario

### Paso 1: Acceder al Formulario

1. **Opción A - En línea**: Visite https://laborauq.streamlit.app/
2. **Opción B - Local**: Ejecute `streamlit run professional_registration_form.py`

### Paso 2: Completar Información Personal

#### Campos Obligatorios (marcados con *)

1. **Nombre Completo**: Su nombre y apellidos
2. **Correo Electrónico**: Dirección de email válida
   - VÁLIDO: `usuario@empresa.com`
   - INVÁLIDO: `usuario@empresa` (falta extensión)
3. **Teléfono**: Número con código de país
   - VÁLIDO: `+573001234567`
   - INVÁLIDO: `3001234567` (falta el `+`)

#### Campos Opcionales

4. **Fecha de Nacimiento**: Formato DD/MM/YYYY
   - Ejemplo: `15/08/2000`

### Paso 3: Completar Información Profesional

5. **Profesión** *: Su título profesional
   - Ejemplo: `Desarrollador Full Stack`
6. **Empresa Actual**: Lugar de trabajo actual
7. **Años de Experiencia** *: Seleccionar del menú desplegable
8. **Ubicación**: Ciudad y país

### Paso 4: Documentos

9. **DNI/Pasaporte**: Documento de identidad
   - VÁLIDO: `12345678A`, `AB123456`
   - INVÁLIDO: `123` (muy corto)
10. **Código Postal**: Código de su ubicación
    - VÁLIDO: `630001`, `28001`
    - INVÁLIDO: `12` (muy corto)

### Paso 5: Enlaces de Portafolio

11. **URLs de Proyectos**: Agregue enlaces a sus proyectos
    - VÁLIDO: `https://github.com/usuario/proyecto`
    - INVÁLIDO: `github.com/proyecto` (falta `https://`)
    - Use el botón **Agregar URL** para más enlaces
    - Use el botón de eliminar para quitar URLs

### Paso 6: Información Adicional

12. **Biografía Profesional**: Descripción de su perfil
13. **Habilidades Principales**: Lista de habilidades separadas por comas

### Paso 7: Revisar Estado de Validación

Antes de enviar, revise el **Resumen de Validación**:
- **Válidos**: Campos correctos
- **Inválidos**: Campos con errores de formato
- **Obligatorios faltantes**: Campos requeridos sin completar

### Paso 8: Aceptar Términos y Enviar

14. Marque: "Acepto los términos y condiciones" (obligatorio)
15. Opcionalmente: "Deseo recibir notificaciones"
16. Haga clic en **Completar Registro**

### Interpretación de Mensajes

- **Verde con marca**: Campo válido
- **Rojo con X**: Campo inválido, revise el formato
- **Amarillo con advertencia**: Campo obligatorio faltante

---

## Guía para Desarrolladores

### Agregar Nuevos Patrones de Validación

1. **Definir el patrón regex** en `app/validators/patterns.py`:

```python
# Ejemplo: Validar código de estudiante (formato: EST-NNNN)
PATTERN_STUDENT_CODE = r"^EST-[0-9]{4}$"
```

2. **Crear función de validación**:

```python
def validate_student_code(code: str) -> bool:
    """
    Valida si un código de estudiante tiene formato correcto.
    Formato esperado: EST-NNNN (ej: EST-1234)
    
    Args:
        code (str): Código a validar
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    if not code:
        return False
    return bool(re.match(PATTERN_STUDENT_CODE, code))
```

3. **Integrar en el formulario** (`professional_registration_form.py`):

```python
# Importar la función
from validators.patterns import validate_student_code

# Agregar campo al formulario
codigo_estudiante = st.text_input(
    "Código de Estudiante",
    placeholder="EST-1234",
    help="Formato: EST-NNNN"
)

# Agregar validación
show_smart_validation(
    "codigo_estudiante", 
    codigo_estudiante, 
    validate_student_code, 
    is_required=True,
    display_name="Código"
)
```

### Modificar Estilos CSS

Edite la sección de CSS en `professional_registration_form.py`:

```python
st.markdown("""
<style>
    /* Sus estilos personalizados aquí */
    .custom-class {
        color: #your-color;
    }
</style>
""", unsafe_allow_html=True)
```

### Extender la API FastAPI

Agregue nuevos endpoints en `app/api/v1/endpoints.py`:

```python
@router.post("/validate")
def validate_field(field: str, value: str):
    validators = {
        'email': validate_email,
        'phone': validate_phone,
        # Agregar más validadores
    }
    
    validator = validators.get(field)
    if not validator:
        return {"error": "Validator not found"}
    
    return {
        "field": field,
        "value": value,
        "valid": validator(value)
    }
```

### Pruebas Unitarias

Ejemplo de pruebas para sus patrones:

```python
import unittest
from app.validators.patterns import validate_email

class TestEmailValidation(unittest.TestCase):
    def test_valid_emails(self):
        valid_emails = [
            "usuario@ejemplo.com",
            "nombre.apellido@empresa.co",
            "test@test.com"
        ]
        for email in valid_emails:
            self.assertTrue(validate_email(email))
    
    def test_invalid_emails(self):
        invalid_emails = [
            "usuario@@ejemplo.com",
            "@ejemplo.com",
            "usuario@"
        ]
        for email in invalid_emails:
            self.assertFalse(validate_email(email))

if __name__ == '__main__':
    unittest.main()
```

---

## Casos de Prueba

### Conjunto de Pruebas Válidas

| Campo | Entrada | Resultado Esperado |
|-------|---------|-------------------|
| Email | `usuario@ejemplo.com` | VÁLIDO |
| Teléfono | `+573001234567` | VÁLIDO |
| Fecha | `15/08/2000` | VÁLIDO |
| DNI | `12345678A` | VÁLIDO |
| Código Postal | `630001` | VÁLIDO |
| URL | `https://github.com/user/repo` | VÁLIDO |

### Conjunto de Pruebas Inválidas

| Campo | Entrada | Resultado Esperado | Razón |
|-------|---------|-------------------|-------|
| Email | `usuario@@ejemplo.com` | INVÁLIDO | Doble `@` |
| Teléfono | `3001234567` | INVÁLIDO | Falta `+` |
| Fecha | `2000-08-15` | INVÁLIDO | Formato incorrecto |
| DNI | `123` | INVÁLIDO | Muy corto (<4 caracteres) |
| Código Postal | `12` | INVÁLIDO | Muy corto (<3 dígitos) |
| URL | `github.com/repo` | INVÁLIDO | Falta esquema (`https://`) |

### Casos Especiales

| Campo | Entrada | Resultado | Observación |
|-------|---------|-----------|-------------|
| Email | `a@b.co` | VÁLIDO | Formato mínimo válido |
| Fecha | `31/02/2024` | VÁLIDO | Validación sintáctica, no semántica |
| DNI | `ABCD1234EFGH5678AB` | VÁLIDO | Longitud máxima (18 caracteres) |
| URL | `https://a.b` | VÁLIDO | URL mínima válida |

---

## Solución de Problemas

### Problema 1: Streamlit no se ejecuta

**Síntoma**: Error al ejecutar `streamlit run`

**Solución**:
```bash
# Verificar instalación
pip install --upgrade streamlit

# Verificar versión de Python (debe ser 3.8+)
python --version

# Ejecutar con Python explícito
python -m streamlit run professional_registration_form.py
```

### Problema 2: Módulo no encontrado

**Síntoma**: `ModuleNotFoundError: No module named 'app'`

**Solución**:
```bash
# Asegurarse de estar en el directorio raíz del proyecto
cd LaboraUQ

# Verificar que existe el directorio app/
ls app/validators/

# Ejecutar desde el directorio correcto
streamlit run professional_registration_form.py
```

### Problema 3: Puerto ya en uso

**Síntoma**: `Address already in use`

**Solución**:
```bash
# Usar un puerto diferente
streamlit run professional_registration_form.py --server.port 8502

# O detener procesos que usen el puerto 8501
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8501 | xargs kill -9
```

### Problema 4: Validación no funciona correctamente

**Posibles causas y soluciones**:

1. **Espacios en blanco extras**:
   - Asegúrese de no incluir espacios antes o después del valor
   - Ejemplo: `+573001234567` (correcto) vs ` +573001234567` (incorrecto)

2. **Formato de fecha incorrecto**:
   - Use barras `/` no guiones `-`
   - Formato: `DD/MM/YYYY` no `YYYY-MM-DD`

3. **URL sin esquema**:
   - Siempre incluya `http://` o `https://`
   - `https://ejemplo.com` (correcto) vs `ejemplo.com` (incorrecto)

### Problema 5: Campos dinámicos de URL no se actualizan

**Solución**:
```python
# Limpiar caché de Streamlit
streamlit cache clear

# O reiniciar la aplicación presionando 'R' en el navegador
```

---

## Referencias Técnicas

### Estándares Implementados

- **RFC 5321**: Simple Mail Transfer Protocol (SMTP)
- **RFC 5322**: Internet Message Format
- **RFC 1035**: Domain Names Implementation and Specification
- **RFC 3986**: Uniform Resource Identifier (URI) Generic Syntax
- **ITU-T E.164**: International Public Telecommunication Numbering Plan

### Documentación Adicional

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Python re module](https://docs.python.org/3/library/re.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

---

## Soporte

Para reportar problemas, sugerencias o contribuciones, por favor:

1. Revise esta guía de uso completa
2. Consulte la sección de solución de problemas
3. Verifique los casos de prueba predefinidos
4. Contacte al equipo de desarrollo con información detallada del problema

---

## Notas Importantes

### Limitaciones Conocidas

1. **Validación sintáctica vs semántica**: 
   - Las fechas se validan por formato, no por validez (acepta `31/02/2024`)
   - Los dominios de email se validan por estructura, no por existencia real

2. **Seguridad**:
   - La validación client-side NO reemplaza la validación server-side
   - Implemente validación adicional en backend para producción

3. **Rendimiento**:
   - Evite patrones regex que causen ReDoS (Regular Expression Denial of Service)
   - Los patrones actuales están optimizados para complejidad lineal

### Mejores Prácticas

- Siempre combine validación de formato con validación de negocio
- Implemente límites de longitud en todos los campos
- Use mensajes de error descriptivos y útiles
- Proporcione ejemplos de formato válido
- Mantenga la experiencia de usuario fluida con validación no intrusiva

---

**Versión de la Guía**: 1.0  
**Última Actualización**: 2025  
**Autores**: Miguel Angel Mira Ortega, Juan Manuel Isaza Vergara, Santiago Quintero Uribe  
**Universidad del Quindío - Ingeniería de Sistemas y Computación**