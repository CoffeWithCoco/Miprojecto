# Miprojecto - Herramientas de Ciberseguridad

Colección de herramientas de ciberseguridad escritas en Python para análisis de seguridad, auditorías y pruebas de penetración.

## 🛠️ Herramientas Incluidas

### 1. **Port Scanner** (Escáner de Puertos)
Escanea puertos abiertos en un host específico para identificar servicios disponibles.

**Uso:**
```bash
python3 herramientas_ciberseguridad/port_scanner.py <host> [puerto_inicio] [puerto_fin]
```

**Ejemplos:**
```bash
# Escanear puertos comunes (1-1024)
python3 herramientas_ciberseguridad/port_scanner.py localhost

# Escanear rango específico
python3 herramientas_ciberseguridad/port_scanner.py 192.168.1.1 1 100

# Escanear puerto específico
python3 herramientas_ciberseguridad/port_scanner.py example.com 80 80
```

### 2. **Password Checker** (Verificador de Contraseñas)
Evalúa la fortaleza de contraseñas y proporciona recomendaciones de seguridad.

**Uso:**
```bash
python3 herramientas_ciberseguridad/password_checker.py [contraseña]
```

**Ejemplos:**
```bash
# Análisis interactivo (oculta la contraseña)
python3 herramientas_ciberseguridad/password_checker.py

# Análisis directo
python3 herramientas_ciberseguridad/password_checker.py "MiContraseña123!"

# Mostrar consejos
python3 herramientas_ciberseguridad/password_checker.py --tips
```

**Criterios de evaluación:**
- Longitud de la contraseña
- Uso de mayúsculas y minúsculas
- Inclusión de números
- Caracteres especiales
- Patrones comunes

### 3. **Hash Generator** (Generador de Hashes)
Genera y verifica hashes criptográficos de textos y archivos.

**Uso:**
```bash
python3 herramientas_ciberseguridad/hash_generator.py [opciones]
```

**Ejemplos:**
```bash
# Generar hash de texto
python3 herramientas_ciberseguridad/hash_generator.py -t "Hola Mundo"

# Generar hash de archivo
python3 herramientas_ciberseguridad/hash_generator.py -f documento.txt

# Usar algoritmo específico
python3 herramientas_ciberseguridad/hash_generator.py -t "secreto" -a sha512

# Verificar hash
python3 herramientas_ciberseguridad/hash_generator.py -t "texto" -v abc123def456
```

**Algoritmos soportados:** MD5, SHA1, SHA256, SHA512

### 4. **Network Analyzer** (Analizador de Red)
Proporciona información sobre la configuración de red y conexiones.

**Uso:**
```bash
python3 herramientas_ciberseguridad/network_analyzer.py [opciones]
```

**Ejemplos:**
```bash
# Información completa de red
python3 herramientas_ciberseguridad/network_analyzer.py -i

# Resolver hostname a IP
python3 herramientas_ciberseguridad/network_analyzer.py -r google.com

# Búsqueda DNS inversa
python3 herramientas_ciberseguridad/network_analyzer.py -d 8.8.8.8

# Verificar puerto
python3 herramientas_ciberseguridad/network_analyzer.py -p localhost 80

# Ver interfaces de red
python3 herramientas_ciberseguridad/network_analyzer.py -if
```

### 5. **File Integrity Checker** (Verificador de Integridad)
Monitorea cambios en archivos y directorios mediante hashes.

**Uso:**
```bash
python3 herramientas_ciberseguridad/file_integrity.py [opciones]
```

**Ejemplos:**
```bash
# Crear línea base de integridad
python3 herramientas_ciberseguridad/file_integrity.py -c /ruta/a/directorio

# Verificar integridad
python3 herramientas_ciberseguridad/file_integrity.py -v /ruta/a/directorio

# Usar archivo de línea base personalizado
python3 herramientas_ciberseguridad/file_integrity.py -c /ruta -b mi_baseline.json
python3 herramientas_ciberseguridad/file_integrity.py -v /ruta -b mi_baseline.json

# Usar algoritmo específico
python3 herramientas_ciberseguridad/file_integrity.py -c /ruta -a sha512
```

**Funcionalidades:**
- Detección de archivos modificados
- Detección de archivos nuevos
- Detección de archivos eliminados
- Almacenamiento de línea base en JSON

### 6. **Vulnerability Scanner** (Escáner de Vulnerabilidades)
Escanea sistemas en busca de vulnerabilidades comunes.

**Uso:**
```bash
python3 herramientas_ciberseguridad/vulnerability_scanner.py [opciones] <objetivo>
```

**Ejemplos:**
```bash
# Escaneo básico
python3 herramientas_ciberseguridad/vulnerability_scanner.py example.com

# Escaneo completo
python3 herramientas_ciberseguridad/vulnerability_scanner.py -f example.com
```

**Verificaciones:**
- Certificados SSL/TLS
- Protocolos débiles (SSLv3, TLSv1)
- Puertos vulnerables abiertos
- Headers de seguridad HTTP (en modo completo)

## 📋 Requisitos

- Python 3.6 o superior
- No requiere dependencias externas (solo bibliotecas estándar de Python)

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/CoffeWithCoco/Miprojecto.git
cd Miprojecto
```

2. Dar permisos de ejecución (opcional):
```bash
chmod +x herramientas_ciberseguridad/*.py
```

## ⚠️ Consideraciones de Seguridad

- **Uso Ético**: Estas herramientas deben usarse únicamente en sistemas propios o con permiso explícito.
- **Legalidad**: El uso no autorizado de estas herramientas puede ser ilegal.
- **Propósito Educativo**: Diseñadas para aprendizaje y auditorías legítimas.
- **Limitaciones**: Estas son herramientas básicas. Para auditorías profesionales, use herramientas especializadas.

## 🔒 Mejores Prácticas

1. **Siempre obtenga permiso** antes de escanear sistemas que no sean suyos
2. **Documente sus hallazgos** de manera responsable
3. **Reporte vulnerabilidades** a los propietarios del sistema de manera ética
4. **Mantenga las herramientas actualizadas**
5. **Use en entornos de prueba** antes de producción

## 📖 Documentación Adicional

Para más información sobre cada herramienta, ejecute:
```bash
python3 herramientas_ciberseguridad/<herramienta>.py --help
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abra un issue o pull request para sugerencias.

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## ⚡ Inicio Rápido

```bash
# Ejemplo rápido: Escanear localhost
python3 herramientas_ciberseguridad/port_scanner.py localhost 1 100

# Verificar contraseña
python3 herramientas_ciberseguridad/password_checker.py

# Generar hash
python3 herramientas_ciberseguridad/hash_generator.py -t "Mi texto secreto"

# Información de red
python3 herramientas_ciberseguridad/network_analyzer.py -i
```

## 🛡️ Herramientas de Seguridad Profesionales Recomendadas

Para auditorías de seguridad profesionales, considere:
- **Nmap**: Escaneo de puertos avanzado
- **Wireshark**: Análisis de tráfico de red
- **OWASP ZAP**: Pruebas de seguridad web
- **Metasploit**: Framework de pruebas de penetración
- **Burp Suite**: Pruebas de seguridad de aplicaciones web

---

**Nota**: Este es un proyecto educativo. Úselo de manera responsable y ética.
