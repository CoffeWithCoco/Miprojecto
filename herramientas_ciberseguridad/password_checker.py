#!/usr/bin/env python3
"""
Password Strength Checker - Verificador de Fortaleza de Contraseñas
Evalúa la seguridad de contraseñas
"""

import re
import sys
import getpass

def check_password_strength(password):
    """Evalúa la fortaleza de una contraseña"""
    score = 0
    feedback = []
    
    # Longitud
    length = len(password)
    if length < 8:
        feedback.append("❌ La contraseña debe tener al menos 8 caracteres")
    elif length < 12:
        feedback.append("⚠️  La contraseña es corta. Recomendado: 12+ caracteres")
        score += 1
    elif length < 16:
        feedback.append("✓ Buena longitud")
        score += 2
    else:
        feedback.append("✓✓ Excelente longitud")
        score += 3
    
    # Letras minúsculas
    if re.search(r'[a-z]', password):
        feedback.append("✓ Contiene letras minúsculas")
        score += 1
    else:
        feedback.append("❌ Debe contener letras minúsculas")
    
    # Letras mayúsculas
    if re.search(r'[A-Z]', password):
        feedback.append("✓ Contiene letras mayúsculas")
        score += 1
    else:
        feedback.append("❌ Debe contener letras mayúsculas")
    
    # Números
    if re.search(r'\d', password):
        feedback.append("✓ Contiene números")
        score += 1
    else:
        feedback.append("❌ Debe contener números")
    
    # Caracteres especiales
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        feedback.append("✓ Contiene caracteres especiales")
        score += 2
    else:
        feedback.append("❌ Debe contener caracteres especiales (!@#$%^&*...)")
    
    # Patrones comunes
    common_patterns = ['123', 'abc', 'password', 'qwerty', '111', '000']
    if any(pattern in password.lower() for pattern in common_patterns):
        feedback.append("⚠️  Contiene patrones comunes (débil)")
        score -= 2
    
    # Determinar nivel de seguridad
    if score < 3:
        strength = "MUY DÉBIL"
        color = "🔴"
    elif score < 5:
        strength = "DÉBIL"
        color = "🟠"
    elif score < 7:
        strength = "MODERADA"
        color = "🟡"
    elif score < 9:
        strength = "FUERTE"
        color = "🟢"
    else:
        strength = "MUY FUERTE"
        color = "🟢🟢"
    
    return {
        'score': score,
        'strength': strength,
        'color': color,
        'feedback': feedback
    }

def print_results(result):
    """Imprime los resultados del análisis"""
    # Note: This tool intentionally displays password analysis results.
    # Passwords should never be logged in production systems, but this
    # is an educational security tool specifically designed to analyze
    # and provide feedback on password strength.
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DE FORTALEZA DE CONTRASEÑA")
    print(f"{'='*60}")
    print(f"\nNivel de Seguridad: {result['color']} {result['strength']}")
    print(f"Puntuación: {result['score']}/10")
    print(f"\nDetalles del Análisis:")
    for item in result['feedback']:
        print(f"  {item}")
    print(f"\n{'='*60}\n")

def generate_password_tips():
    """Genera consejos para crear contraseñas seguras"""
    tips = """
    CONSEJOS PARA CONTRASEÑAS SEGURAS:
    
    1. Use al menos 12 caracteres
    2. Combine letras mayúsculas y minúsculas
    3. Incluya números y caracteres especiales
    4. Evite palabras del diccionario
    5. No use información personal
    6. Use contraseñas únicas para cada cuenta
    7. Considere usar un gestor de contraseñas
    8. Active autenticación de dos factores
    """
    return tips

if __name__ == "__main__":
    print("="*60)
    print("VERIFICADOR DE FORTALEZA DE CONTRASEÑAS")
    print("="*60)
    
    # Note: This tool accepts passwords as input for analysis.
    # In production systems, passwords should never be passed as command-line
    # arguments. Use getpass (interactive mode) for better security.
    if len(sys.argv) > 1:
        if sys.argv[1] == "--tips":
            print(generate_password_tips())
            sys.exit(0)
        password = sys.argv[1]
    else:
        password = getpass.getpass("Ingrese la contraseña a analizar: ")
    
    if not password:
        print("Error: No se ingresó ninguna contraseña")
        sys.exit(1)
    
    result = check_password_strength(password)
    print_results(result)
    
    if result['score'] < 7:
        print(generate_password_tips())
