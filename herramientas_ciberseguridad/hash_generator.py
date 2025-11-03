#!/usr/bin/env python3
"""
Hash Generator - Generador y Verificador de Hashes
Genera y verifica hashes criptográficos
"""

import hashlib
import sys
import os

def generate_hash(data, algorithm='sha256'):
    """Genera un hash del texto dado"""
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    
    if algorithm not in algorithms:
        return None
    
    hash_obj = algorithms[algorithm]()
    hash_obj.update(data.encode('utf-8'))
    return hash_obj.hexdigest()

def hash_file(filepath, algorithm='sha256'):
    """Genera un hash de un archivo"""
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    
    if algorithm not in algorithms:
        return None
    
    if not os.path.exists(filepath):
        print(f"Error: El archivo '{filepath}' no existe")
        return None
    
    hash_obj = algorithms[algorithm]()
    
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def verify_hash(data, expected_hash, algorithm='sha256'):
    """Verifica si un hash coincide con el esperado"""
    actual_hash = generate_hash(data, algorithm)
    return actual_hash == expected_hash.lower()

def print_usage():
    """Imprime instrucciones de uso"""
    print("""
USO:
    python3 hash_generator.py [opciones]

OPCIONES:
    -t, --text <texto>          Genera hash de texto
    -f, --file <archivo>        Genera hash de archivo
    -v, --verify <hash>         Verifica hash contra texto
    -a, --algorithm <algo>      Algoritmo (md5, sha1, sha256, sha512)
                                Por defecto: sha256
    -h, --help                  Muestra esta ayuda

EJEMPLOS:
    python3 hash_generator.py -t "Hola Mundo"
    python3 hash_generator.py -f documento.txt
    python3 hash_generator.py -t "secreto" -a md5
    python3 hash_generator.py -f archivo.pdf -a sha512
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    algorithm = 'sha256'
    mode = None
    target = None
    verify_hash_value = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ['-h', '--help']:
            print_usage()
            sys.exit(0)
        elif arg in ['-a', '--algorithm']:
            if i + 1 < len(sys.argv):
                algorithm = sys.argv[i + 1].lower()
                i += 2
            else:
                print("Error: Falta el algoritmo")
                sys.exit(1)
        elif arg in ['-t', '--text']:
            if i + 1 < len(sys.argv):
                mode = 'text'
                target = sys.argv[i + 1]
                i += 2
            else:
                print("Error: Falta el texto")
                sys.exit(1)
        elif arg in ['-f', '--file']:
            if i + 1 < len(sys.argv):
                mode = 'file'
                target = sys.argv[i + 1]
                i += 2
            else:
                print("Error: Falta el archivo")
                sys.exit(1)
        elif arg in ['-v', '--verify']:
            if i + 1 < len(sys.argv):
                verify_hash_value = sys.argv[i + 1]
                i += 2
            else:
                print("Error: Falta el hash a verificar")
                sys.exit(1)
        else:
            print(f"Opción desconocida: {arg}")
            print_usage()
            sys.exit(1)
    
    if mode is None:
        print("Error: Debe especificar -t o -f")
        print_usage()
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"GENERADOR DE HASHES CRIPTOGRÁFICOS")
    print(f"{'='*60}")
    print(f"Algoritmo: {algorithm.upper()}")
    
    if mode == 'text':
        print(f"Texto: {target}")
        hash_result = generate_hash(target, algorithm)
    else:
        print(f"Archivo: {target}")
        hash_result = hash_file(target, algorithm)
    
    if hash_result:
        print(f"Hash: {hash_result}")
        
        if verify_hash_value:
            if hash_result == verify_hash_value.lower():
                print(f"\n✓ VERIFICACIÓN EXITOSA: Los hashes coinciden")
            else:
                print(f"\n✗ VERIFICACIÓN FALLIDA: Los hashes NO coinciden")
                print(f"  Esperado: {verify_hash_value}")
                print(f"  Obtenido: {hash_result}")
    else:
        print(f"Error: No se pudo generar el hash")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
