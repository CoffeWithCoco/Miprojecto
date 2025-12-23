#!/bin/bash
# Ejemplos de uso de las herramientas de ciberseguridad

echo "============================================================"
echo "EJEMPLOS DE HERRAMIENTAS DE CIBERSEGURIDAD"
echo "============================================================"
echo ""

# 1. Password Checker
echo "[1] Verificador de Contraseñas"
echo "Probando contraseña débil..."
python3 herramientas_ciberseguridad/password_checker.py "abc123"
echo ""
read -p "Presione Enter para continuar..."
echo ""

# 2. Hash Generator
echo "[2] Generador de Hashes"
echo "Generando hash SHA256 de 'Hola Mundo'..."
python3 herramientas_ciberseguridad/hash_generator.py -t "Hola Mundo"
echo ""
read -p "Presione Enter para continuar..."
echo ""

# 3. Network Analyzer
echo "[3] Analizador de Red"
echo "Resolviendo google.com..."
python3 herramientas_ciberseguridad/network_analyzer.py -r google.com
echo ""
read -p "Presione Enter para continuar..."
echo ""

# 4. Port Scanner (ejemplo pequeño)
echo "[4] Escáner de Puertos"
echo "Escaneando puertos 1-10 en localhost..."
python3 herramientas_ciberseguridad/port_scanner.py localhost 1 10
echo ""
read -p "Presione Enter para continuar..."
echo ""

# 5. File Integrity
echo "[5] Verificador de Integridad de Archivos"
echo "Creando directorio de prueba..."
mkdir -p /tmp/demo_integrity
echo "Archivo de prueba" > /tmp/demo_integrity/test.txt
echo "Creando línea base..."
python3 herramientas_ciberseguridad/file_integrity.py -c /tmp/demo_integrity -b /tmp/demo_baseline.json
echo ""
echo "Verificando integridad..."
python3 herramientas_ciberseguridad/file_integrity.py -v /tmp/demo_integrity -b /tmp/demo_baseline.json
echo ""
read -p "Presione Enter para continuar..."
echo ""

# 6. Vulnerability Scanner (ayuda)
echo "[6] Escáner de Vulnerabilidades"
python3 herramientas_ciberseguridad/vulnerability_scanner.py --help
echo ""

echo "============================================================"
echo "DEMOSTRACIÓN COMPLETADA"
echo "============================================================"
echo ""
echo "Para más información, consulte el README.md"
echo ""
