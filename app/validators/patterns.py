import re
from typing import List, Dict, Any


# =============================================================================
# PATRONES DE VALIDACIÓN DEFINIDOS
# =============================================================================

# Patrón complejo para correo electrónico
SIMBOLOS_COMILLAS = r"!#\$%&'\*\+-\/=\?\^_`{\|}~\.,:;<>\(\)\[ \]@(\\\")"
PARTE_NOMBRE = rf"([A-Za-z0-9_\-+]+)|(\"[A-Za-z0-9{SIMBOLOS_COMILLAS}]*\")"
NOMBRE_CORREO = rf"{PARTE_NOMBRE}(\.{PARTE_NOMBRE})*"
DOMINIO = r"((?:[a-z0-9](?:[a-z0-9_-]{0,61}[a-z0-9])?)(?:\.(?:[a-z0-9](?:[a-z0-9_-]{0,61}[a-z0-9])?))*\.[a-z]{2,})"
PATTERN_EMAIL = rf"^({NOMBRE_CORREO})@({DOMINIO})$"

# Patrón para números telefónicos
PATTERN_PHONE = r"^\+[0-9]{8,15}$"

# Patrón para fechas
PATTERN_DATE = r"^[0-9]{2}/[0-9]{2}/(-)?[0-9]+$"

# Patrón para DNIs
PATTERN_DNI = r"^[A-Z0-9]{4,18}$"

# Patrón para códigos postales
PATTERN_POSTAL_CODE = r"^[0-9]{3,9}$"

# Patrones complejos para URLs
ESQUEMA = r"[A-Za-z][A-Za-z0-9\+\.-]+"
HEX = r"[0-9ABCDEF]"
ESP = rf"%({HEX}){{2}}"
USUARIO = rf"([A-Za-z]|({ESP}))[!\$&\(,\)\*\+;]*@([A-Za-z]|({ESP}))[!\$&\(,\)\*\+;]*"
IP = r"[0-9]{{1,3}}:[0-9]{{1,3}}:[0-9]{{1,3}}"
MAC = rf"{HEX}{{2}}:{HEX}{{2}}:{HEX}{{2}}:{HEX}{{2}}:{HEX}{{2}}"
PUERTO = r"(:[0-9]{1,5})?"
HOST = r"(?![A-Za-z0-9.-]{256,})((?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)(?:\.(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?))*)(?![A-Za-z0-9.-])"
RUTA = r"(/[A-Za-z0-9\-._~:/?#[\]@!$&'()*+,;=]*)?"
PARAMETROS = r"(\?[A-Za-z0-9\-._~:/?#[\]@!$&'()*+,;=]*)?"
PATTERN_URL = rf"{ESQUEMA}://({USUARIO})?{HOST}{PUERTO}{RUTA}{PARAMETROS}"


# =============================================================================
# FUNCIONES DE VALIDACIÓN
# =============================================================================

def validate_email(email: str) -> bool:
    """
    Valida si un email tiene formato correcto usando el patrón complejo definido.
    
    Args:
        email (str): Email a validar
        
    Returns:
        bool: True si el email es válido, False en caso contrario
    """
    if not email or len(email) > 254:
        return False
    return bool(re.match(PATTERN_EMAIL, email))


def validate_phone(phone: str) -> bool:
    """
    Valida si un número telefónico tiene formato correcto.
    Formato esperado: + seguido de 8 a 15 dígitos
    
    Args:
        phone (str): Número telefónico a validar
        
    Returns:
        bool: True si el teléfono es válido, False en caso contrario
    """
    if not phone:
        return False
    return bool(re.match(PATTERN_PHONE, phone))


def validate_date(date: str) -> bool:
    """
    Valida si una fecha tiene formato correcto.
    Formato esperado: DD/MM/YYYY o DD/MM/-YYYY
    
    Args:
        date (str): Fecha a validar
        
    Returns:
        bool: True si la fecha es válida, False en caso contrario
    """
    if not date:
        return False
    return bool(re.match(PATTERN_DATE, date))


def validate_dni(dni: str) -> bool:
    """
    Valida si un DNI tiene formato correcto.
    Formato esperado: 4 a 18 caracteres alfanuméricos en mayúsculas
    
    Args:
        dni (str): DNI a validar
        
    Returns:
        bool: True si el DNI es válido, False en caso contrario
    """
    if not dni:
        return False
    return bool(re.match(PATTERN_DNI, dni))


def validate_postal_code(postal_code: str) -> bool:
    """
    Valida si un código postal tiene formato correcto.
    Formato esperado: 3 a 9 dígitos
    
    Args:
        postal_code (str): Código postal a validar
        
    Returns:
        bool: True si el código postal es válido, False en caso contrario
    """
    if not postal_code:
        return False
    return bool(re.match(PATTERN_POSTAL_CODE, postal_code))


def validate_url(url: str) -> bool:
    """
    Valida si una URL tiene formato correcto usando el patrón complejo definido.
    
    Args:
        url (str): URL a validar
        
    Returns:
        bool: True si la URL es válida, False en caso contrario
    """
    if not url:
        return False
    return bool(re.match(PATTERN_URL, url))


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def extract_numbers(text: str) -> List[str]:
    """
    Extrae todos los números de un texto.
    
    Args:
        text (str): Texto del cual extraer números
        
    Returns:
        List[str]: Lista de números encontrados
    """
    if not text:
        return []
    pattern = r'\d+'
    return re.findall(pattern, text)


def clean_text(text: str) -> str:
    """
    Limpia texto removiendo caracteres especiales.
    Mantiene solo letras, números y espacios.
    
    Args:
        text (str): Texto a limpiar
        
    Returns:
        str: Texto limpio
    """
    if not text:
        return ""
    pattern = r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, '', text)


def find_patterns(text: str, pattern: str) -> Dict[str, Any]:
    """
    Busca patrones en texto y retorna información detallada.
    
    Args:
        text (str): Texto en el cual buscar
        pattern (str): Patrón regex a buscar
        
    Returns:
        Dict[str, Any]: Diccionario con información de las coincidencias
    """
    if not text or not pattern:
        return {"matches": [], "count": 0, "text_length": 0}
    
    matches = re.findall(pattern, text)
    return {
        "matches": matches,
        "count": len(matches),
        "text_length": len(text)
    }


def validate_all_fields(data: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    """
    Valida múltiples campos usando los patrones definidos.
    
    Args:
        data (Dict[str, str]): Diccionario con los campos a validar
        
    Returns:
        Dict[str, Dict[str, Any]]: Resultados de validación para cada campo
    """
    results = {}
    
    # Mapeo de campos a funciones de validación
    validators = {
        'email': validate_email,
        'phone': validate_phone,
        'date': validate_date,
        'dni': validate_dni,
        'postal_code': validate_postal_code,
        'url': validate_url
    }
    
    for field, value in data.items():
        if field in validators:
            results[field] = {
                'value': value,
                'valid': validators[field](value),
                'validator': field
            }
        else:
            results[field] = {
                'value': value,
                'valid': None,
                'validator': 'unknown'
            }
    
    return results
