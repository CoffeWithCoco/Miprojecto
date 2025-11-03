#!/usr/bin/env python3
"""
Network Analyzer - Analizador de Red
Proporciona información sobre la configuración de red y conexiones
"""

import socket
import sys
import subprocess
import platform

def get_hostname():
    """Obtiene el nombre del host"""
    return socket.gethostname()

def get_local_ip():
    """Obtiene la dirección IP local"""
    try:
        # Crear un socket temporal para obtener la IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "No disponible"

def get_public_ip():
    """Intenta obtener la IP pública (requiere conexión a internet)"""
    try:
        import urllib.request
        response = urllib.request.urlopen('https://api.ipify.org', timeout=5)
        return response.read().decode('utf-8')
    except Exception:
        return "No disponible (sin conexión a internet)"

def resolve_hostname(hostname):
    """Resuelve un hostname a dirección IP"""
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        return None

def reverse_dns(ip):
    """Realiza búsqueda DNS inversa"""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except (socket.herror, socket.gaierror):
        return "No se pudo resolver"

def get_network_interfaces():
    """Obtiene información de interfaces de red"""
    system = platform.system()
    
    try:
        if system == "Linux":
            result = subprocess.run(['ip', 'addr'], capture_output=True, text=True, timeout=5)
            return result.stdout
        elif system == "Darwin":  # macOS
            result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=5)
            return result.stdout
        elif system == "Windows":
            result = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=5)
            return result.stdout
        else:
            return "Sistema operativo no soportado"
    except Exception as e:
        return f"Error al obtener interfaces: {e}"

def check_port_open(host, port):
    """Verifica si un puerto está abierto en un host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def print_network_info():
    """Imprime información completa de red"""
    print(f"\n{'='*60}")
    print(f"ANALIZADOR DE RED")
    print(f"{'='*60}\n")
    
    print(f"[*] Información del Host:")
    print(f"    Hostname: {get_hostname()}")
    print(f"    IP Local: {get_local_ip()}")
    print(f"    IP Pública: {get_public_ip()}")
    print(f"    Sistema: {platform.system()} {platform.release()}")
    
    print(f"\n[*] Puertos Comunes (localhost):")
    common_ports = {
        22: 'SSH',
        80: 'HTTP',
        443: 'HTTPS',
        3306: 'MySQL',
        5432: 'PostgreSQL',
        6379: 'Redis',
        8080: 'HTTP-Alt',
        27017: 'MongoDB'
    }
    
    for port, service in common_ports.items():
        status = "ABIERTO" if check_port_open('localhost', port) else "CERRADO"
        print(f"    Puerto {port} ({service}): {status}")
    
    print(f"\n{'='*60}\n")

def print_usage():
    """Imprime instrucciones de uso"""
    print("""
USO:
    python3 network_analyzer.py [opciones]

OPCIONES:
    -i, --info              Muestra información de red completa
    -r, --resolve <host>    Resuelve hostname a IP
    -d, --dns <ip>          Búsqueda DNS inversa
    -p, --port <host> <p>   Verifica si un puerto está abierto
    -if, --interfaces       Muestra interfaces de red
    -h, --help              Muestra esta ayuda

EJEMPLOS:
    python3 network_analyzer.py -i
    python3 network_analyzer.py -r google.com
    python3 network_analyzer.py -d 8.8.8.8
    python3 network_analyzer.py -p localhost 80
    python3 network_analyzer.py -if
    """)

def main():
    if len(sys.argv) < 2:
        print_network_info()
        sys.exit(0)
    
    arg = sys.argv[1]
    
    if arg in ['-h', '--help']:
        print_usage()
    elif arg in ['-i', '--info']:
        print_network_info()
    elif arg in ['-r', '--resolve']:
        if len(sys.argv) < 3:
            print("Error: Falta el hostname")
            sys.exit(1)
        hostname = sys.argv[2]
        print(f"\n[*] Resolviendo: {hostname}")
        ip = resolve_hostname(hostname)
        if ip:
            print(f"    IP: {ip}")
        else:
            print(f"    No se pudo resolver el hostname")
    elif arg in ['-d', '--dns']:
        if len(sys.argv) < 3:
            print("Error: Falta la dirección IP")
            sys.exit(1)
        ip = sys.argv[2]
        print(f"\n[*] Búsqueda DNS inversa: {ip}")
        hostname = reverse_dns(ip)
        print(f"    Hostname: {hostname}")
    elif arg in ['-p', '--port']:
        if len(sys.argv) < 4:
            print("Error: Faltan argumentos (host y puerto)")
            sys.exit(1)
        host = sys.argv[2]
        port = int(sys.argv[3])
        print(f"\n[*] Verificando puerto {port} en {host}")
        if check_port_open(host, port):
            print(f"    Estado: ABIERTO")
        else:
            print(f"    Estado: CERRADO")
    elif arg in ['-if', '--interfaces']:
        print(f"\n{'='*60}")
        print(f"INTERFACES DE RED")
        print(f"{'='*60}\n")
        print(get_network_interfaces())
    else:
        print(f"Opción desconocida: {arg}")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
