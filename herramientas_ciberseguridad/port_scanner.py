#!/usr/bin/env python3
"""
Port Scanner - Herramienta de Escaneo de Puertos
Escanea puertos abiertos en un host específico
"""

import socket
import sys
from datetime import datetime

def scan_port(host, port, timeout=1):
    """Escanea un puerto específico en un host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.gaierror:
        print(f"Error: No se pudo resolver el hostname {host}")
        return False
    except socket.error:
        print(f"Error: No se pudo conectar al host {host}")
        return False

def scan_ports(host, start_port=1, end_port=1024):
    """Escanea un rango de puertos en un host"""
    print(f"\n{'='*60}")
    print(f"ESCÁNER DE PUERTOS")
    print(f"{'='*60}")
    print(f"Host: {host}")
    print(f"Rango de puertos: {start_port}-{end_port}")
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    open_ports = []
    
    try:
        for port in range(start_port, end_port + 1):
            if scan_port(host, port):
                print(f"[+] Puerto {port}: ABIERTO")
                open_ports.append(port)
            else:
                print(f"[-] Puerto {port}: CERRADO", end='\r')
        
        print(f"\n\n{'='*60}")
        print(f"RESUMEN DEL ESCANEO")
        print(f"{'='*60}")
        print(f"Total de puertos abiertos: {len(open_ports)}")
        if open_ports:
            print(f"Puertos abiertos: {', '.join(map(str, open_ports))}")
        print(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
    except KeyboardInterrupt:
        print("\n\n[!] Escaneo interrumpido por el usuario")
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 port_scanner.py <host> [puerto_inicio] [puerto_fin]")
        print("Ejemplo: python3 port_scanner.py localhost 1 100")
        sys.exit(1)
    
    host = sys.argv[1]
    start_port = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end_port = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    
    scan_ports(host, start_port, end_port)
