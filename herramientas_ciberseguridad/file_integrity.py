#!/usr/bin/env python3
"""
File Integrity Checker - Verificador de Integridad de Archivos
Monitorea cambios en archivos y directorios
"""

import hashlib
import os
import sys
import json
from datetime import datetime

def calculate_file_hash(filepath, algorithm='sha256'):
    """Calcula el hash de un archivo"""
    # Validar algoritmo contra una lista permitida
    allowed_algorithms = ['md5', 'sha1', 'sha256', 'sha512']
    if algorithm.lower() not in allowed_algorithms:
        print(f"Error: Algoritmo no permitido '{algorithm}'. Usar: {', '.join(allowed_algorithms)}")
        return None
    
    hash_obj = hashlib.new(algorithm)
    
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Error al leer {filepath}: {e}")
        return None

def scan_directory(directory, algorithm='sha256'):
    """Escanea un directorio y genera un registro de hashes"""
    file_hashes = {}
    
    print(f"[*] Escaneando directorio: {directory}")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, directory)
            
            file_hash = calculate_file_hash(filepath, algorithm)
            if file_hash:
                file_stat = os.stat(filepath)
                file_hashes[relative_path] = {
                    'hash': file_hash,
                    'size': file_stat.st_size,
                    'modified': file_stat.st_mtime,
                    'algorithm': algorithm
                }
                print(f"    ✓ {relative_path}")
    
    return file_hashes

def create_baseline(directory, output_file='baseline.json', algorithm='sha256'):
    """Crea una línea base de integridad"""
    print(f"\n{'='*60}")
    print(f"CREANDO LÍNEA BASE DE INTEGRIDAD")
    print(f"{'='*60}\n")
    
    baseline = {
        'timestamp': datetime.now().isoformat(),
        'directory': os.path.abspath(directory),
        'algorithm': algorithm,
        'files': scan_directory(directory, algorithm)
    }
    
    with open(output_file, 'w') as f:
        json.dump(baseline, f, indent=2)
    
    print(f"\n[+] Línea base creada: {output_file}")
    print(f"[+] Archivos escaneados: {len(baseline['files'])}")
    print(f"{'='*60}\n")

def verify_integrity(directory, baseline_file='baseline.json'):
    """Verifica la integridad contra una línea base"""
    print(f"\n{'='*60}")
    print(f"VERIFICANDO INTEGRIDAD DE ARCHIVOS")
    print(f"{'='*60}\n")
    
    if not os.path.exists(baseline_file):
        print(f"Error: No se encuentra el archivo de línea base: {baseline_file}")
        return
    
    with open(baseline_file, 'r') as f:
        baseline = json.load(f)
    
    print(f"[*] Línea base creada: {baseline['timestamp']}")
    print(f"[*] Directorio base: {baseline['directory']}")
    print(f"[*] Algoritmo: {baseline['algorithm']}")
    
    current_files = scan_directory(directory, baseline['algorithm'])
    
    # Análisis de cambios
    modified = []
    added = []
    deleted = []
    unchanged = []
    
    # Verificar archivos en la línea base
    for filepath, baseline_info in baseline['files'].items():
        if filepath in current_files:
            current_info = current_files[filepath]
            if current_info['hash'] != baseline_info['hash']:
                modified.append(filepath)
            else:
                unchanged.append(filepath)
        else:
            deleted.append(filepath)
    
    # Verificar archivos nuevos
    for filepath in current_files:
        if filepath not in baseline['files']:
            added.append(filepath)
    
    # Mostrar resultados
    print(f"\n{'='*60}")
    print(f"RESULTADOS DE LA VERIFICACIÓN")
    print(f"{'='*60}\n")
    
    if not modified and not added and not deleted:
        print("✓ INTEGRIDAD VERIFICADA: No se detectaron cambios")
    else:
        print("⚠️  SE DETECTARON CAMBIOS:\n")
        
        if modified:
            print(f"[!] Archivos Modificados ({len(modified)}):")
            for f in modified:
                print(f"    - {f}")
        
        if added:
            print(f"\n[+] Archivos Agregados ({len(added)}):")
            for f in added:
                print(f"    + {f}")
        
        if deleted:
            print(f"\n[-] Archivos Eliminados ({len(deleted)}):")
            for f in deleted:
                print(f"    - {f}")
    
    print(f"\n[*] Resumen:")
    print(f"    Total en línea base: {len(baseline['files'])}")
    print(f"    Total actual: {len(current_files)}")
    print(f"    Sin cambios: {len(unchanged)}")
    print(f"    Modificados: {len(modified)}")
    print(f"    Agregados: {len(added)}")
    print(f"    Eliminados: {len(deleted)}")
    print(f"\n{'='*60}\n")

def print_usage():
    """Imprime instrucciones de uso"""
    print("""
USO:
    python3 file_integrity.py [opciones]

OPCIONES:
    -c, --create <dir>          Crea línea base de integridad
    -v, --verify <dir>          Verifica integridad contra línea base
    -b, --baseline <archivo>    Especifica archivo de línea base
                                (por defecto: baseline.json)
    -a, --algorithm <algo>      Algoritmo hash (sha256, sha512, md5)
                                (por defecto: sha256)
    -h, --help                  Muestra esta ayuda

EJEMPLOS:
    # Crear línea base
    python3 file_integrity.py -c /ruta/a/directorio
    
    # Verificar integridad
    python3 file_integrity.py -v /ruta/a/directorio
    
    # Con archivo de línea base personalizado
    python3 file_integrity.py -c /ruta -b mi_baseline.json
    python3 file_integrity.py -v /ruta -b mi_baseline.json
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    baseline_file = 'baseline.json'
    algorithm = 'sha256'
    mode = None
    directory = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ['-h', '--help']:
            print_usage()
            sys.exit(0)
        elif arg in ['-c', '--create']:
            if i + 1 < len(sys.argv):
                mode = 'create'
                directory = sys.argv[i + 1]
                i += 2
            else:
                print("Error: Falta el directorio")
                sys.exit(1)
        elif arg in ['-v', '--verify']:
            if i + 1 < len(sys.argv):
                mode = 'verify'
                directory = sys.argv[i + 1]
                i += 2
            else:
                print("Error: Falta el directorio")
                sys.exit(1)
        elif arg in ['-b', '--baseline']:
            if i + 1 < len(sys.argv):
                baseline_file = sys.argv[i + 1]
                i += 2
            else:
                print("Error: Falta el archivo de línea base")
                sys.exit(1)
        elif arg in ['-a', '--algorithm']:
            if i + 1 < len(sys.argv):
                algorithm = sys.argv[i + 1].lower()
                i += 2
            else:
                print("Error: Falta el algoritmo")
                sys.exit(1)
        else:
            print(f"Opción desconocida: {arg}")
            print_usage()
            sys.exit(1)
    
    if mode is None or directory is None:
        print("Error: Debe especificar un modo (-c o -v) y un directorio")
        print_usage()
        sys.exit(1)
    
    if not os.path.exists(directory):
        print(f"Error: El directorio '{directory}' no existe")
        sys.exit(1)
    
    if mode == 'create':
        create_baseline(directory, baseline_file, algorithm)
    elif mode == 'verify':
        verify_integrity(directory, baseline_file)

if __name__ == "__main__":
    main()
