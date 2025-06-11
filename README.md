# Web Scraper + Spark Streaming - Fincaraíz

Proyecto completo que demuestra web scraping y procesamiento en tiempo real con Spark Streaming para propiedades inmobiliarias.

## 🚀 Características

### 1. Web Scraping Básico
- Extracción de propiedades desde Fincaraíz Colombia
- Paginación automática (5 páginas por defecto)
- Extracción inteligente de barrios conservando artículos (ej: "La Calleja")
- Datos guardados en CSV con timestamps

### 2. Spark Streaming
- Procesamiento de datos en tiempo real con Spark 3.4.1
- Análisis por lotes (batch) y en tiempo real (streaming)
- Cálculo de métricas de precios por barrio
- Visualización de tendencias de precios

## 🐧 Instalación en Linux

### 1. Requisitos previos

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y \
    python3-pip \
    python3-venv \
    openjdk-11-jdk \
    git \
    libxml2-dev \
    libxslt1-dev \
    python3-lxml

# Verificar instalación de Java (requerido para Spark)
java -version  # Debe mostrar versión 11 o superior
```

### 2. Configuración del entorno virtual

```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Actualzar pip
pip install --upgrade pip
```

### 3. Instalación de dependencias

#### Opción 1: Dependencias mínimas (recomendado para producción)
```bash
pip install -r requirements-min.txt
```

#### Opción 2: Todas las dependencias (desarrollo)
```bash
pip install -r requirements.txt
```

### 4. Configuración de variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```bash
# Configuración de Spark
SPARK_HOME=venv/lib/python3.10/site-packages/pyspark
PYSPARK_PYTHON=python3
PYSPARK_DRIVER_PYTHON=python3

# Configuración de la aplicación
LOG_LEVEL=INFO
DATA_DIR=./data
```

## 🚀 Uso

### 1. Web Scraping

```bash
# Scraping básico (5 páginas)
python web_scraper.py

# Especificar número de páginas
python web_scraper.py --pages 3

# Solo primera página
python web_scraper.py --single

# Usar URL personalizada
python web_scraper.py --url "https://www.fincaraiz.com.co/venta/casas/otra-ciudad/otro-departamento"
```

### 2. Análisis por lotes (Batch)

```bash
# Procesar datos estáticos
python spark_streaming_analysis.py
```

### 3. Análisis en tiempo real (Streaming)

```bash
# Iniciar el procesamiento en tiempo real
python streaming_analysis.py
```

## 📊 Estructura de archivos

```
.
├── files/
│   └── csv/                    # Archivos CSV de entrada/salida
│       └── propiedades_*.csv   # Datos de propiedades
├── output/                     # Resultados de análisis
├── scrapped_data/              # HTMLs descargados (debug)
├── venv/                      # Entorno virtual
├── .env                       # Variables de entorno
├── requirements.txt           # Dependencias completas
├── requirements-min.txt       # Dependencias mínimas
├── web_scraper.py             # Script de scraping
├── spark_streaming_analysis.py # Análisis por lotes
└── streaming_analysis.py      # Análisis en tiempo real
```

## 📝 Notas

- Los datos se guardan automáticamente en `files/csv/` con timestamps
- Los análisis generan informes en la carpeta `output/`
- Se recomienda revisar los logs para depuración

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

#### Sistema Completo
```bash
cd spark
python streaming_coordinator.py
```

## 📊 Análisis de Spark Streaming

El sistema ejecuta 5 análisis en tiempo real:

1. **📋 Todas las propiedades** (cada 10s)
   - Muestra propiedades procesadas en tiempo real

2. **📍 Estadísticas por ubicación** (cada 15s)
   - Precio promedio, máximo, mínimo por zona
   - Número total de propiedades

3. **🏠 Análisis por tipo** (cada 20s)
   - Casa vs Apartamento vs Duplex
   - Precio y área promedio por tipo

4. **💰 Mejor relación calidad-precio** (cada 25s)
   - Propiedades ordenadas por precio/m²
   - Detecta las mejores ofertas

5. **⭐ Alertas propiedades premium** (cada 30s)
   - Propiedades > $500M COP
   - Características de lujo

## 📁 Estructura del Proyecto

```
├── Spark.py                 # Script principal de scraping
├── requirements.txt         # Todas las dependencias del entorno
├── requirements-min.txt     # Dependencias mínimas del proyecto
├── .gitignore              # Archivos a ignorar en Git
├── README.md               # Este archivo
├── propiedades.csv         # Datos extraídos (generado)
├── barrios_tunja_completo.csv # Datos de barrios convertidos desde KML
├── kml_to_csv_simple.py    # Conversor de KML a CSV
└── data/                   # Carpeta de archivos de datos
    └── html_response_*.html # Respuestas HTML (generadas)
```

## 🎮 Guía Rápida

### Para probar todo el sistema (2 minutos):
```bash
# 1. Instalar dependencias
pip install -r requirements-min.txt

# 2. Ejecutar menú principal
python main.py

# 3. Seleccionar opción 2 (Demo Spark Streaming)
# 4. ¡Ver la magia! 🎉
```

### Para scraping real de Fincaraíz:
```bash
# Desde el menú principal
python main.py
# Seleccionar opción 1 (Web Scraping básico)
```

## 🔧 Requisitos del Sistema

- **Python**: 3.7 o superior
- **Java**: 8 o 11 (para PySpark)
- **RAM**: Mínimo 4GB recomendado
- **SO**: Windows/Linux/macOS

## 📈 Datos Generados

### CSV Básico (`data/propiedades.csv`)
- title, price, location, rooms, bathrooms, area_m2, publisher, url

### Streaming JSON (formato enriquecido)
- Todos los campos anteriores +
- timestamp, property_type, amenities, condition, construction_year
- price_per_m2, floors, parking, description

## 🎯 Casos de Uso Demostrados

1. **ETL en Tiempo Real**: Extracción, transformación y carga continua
2. **Análisis de Mercado**: Estadísticas de precios en vivo
3. **Alertas Automáticas**: Detección de propiedades premium
4. **Calidad de Datos**: Limpieza y validación en streaming
5. **Agregaciones Complejas**: Múltiples métricas simultáneas

## 🚨 Troubleshooting

### Error: "Java not found"
```bash
# Instalar Java 11
# Windows: Descargar desde Oracle/OpenJDK
# Linux: sudo apt install openjdk-11-jdk
# macOS: brew install openjdk@11
```

### Error: "No module named pyspark"
```bash
pip install pyspark==3.4.1
```

### Sin datos en streaming
```bash
# Desde el menú principal, seleccionar opción 4
python main.py
```

## 📝 Notas Importantes

- **Streaming Data**: Los archivos JSON se generan en `data/streaming_data/`
- **Rate Limiting**: 2 segundos entre requests para respetar el servidor
- **Memory**: Spark usa ~2GB RAM por defecto
- **Performance**: Mejor rendimiento con SSD
- **Estructura Modular**: Código organizado en módulos específicos

## 🎓 Conceptos Demostrados

### Web Scraping
- **Beautiful Soup**: Parsing de HTML
- **Requests**: Manejo de HTTP
- **Rate Limiting**: Respeto al servidor
- **Error Handling**: Manejo de errores robusto

### Spark Streaming
- **Structured Streaming**: API moderna de Spark
- **Micro-batch Processing**: Procesamiento por lotes pequeños
- **Window Functions**: Análisis temporal
- **Multiple Sinks**: Múltiples outputs simultáneos
- **Schema Evolution**: Manejo de cambios de estructura

### Arquitectura de Software
- **Modularidad**: Separación clara de responsabilidades
- **Escalabilidad**: Fácil agregar nuevas fuentes
- **Mantenibilidad**: Código organizado y documentado

---

## 🏆 ¿Por qué este proyecto es ideal para demostrar Spark Streaming?

1. **✅ Datos Realistas**: Propiedades inmobiliarias reales
2. **✅ Flujo Continuo**: Datos llegan gradualmente
3. **✅ Análisis Variados**: 5 tipos diferentes de consultas
4. **✅ Escalabilidad**: Fácil agregar más fuentes de datos
5. **✅ Visualización**: Resultados claros en consola
6. **✅ Práctica Real**: Caso de uso empresarial típico
7. **✅ Código Organizado**: Estructura profesional modular

¡Perfecto para demostrar las capacidades de Spark Streaming en un contexto real! 🚀

## 🔧 Requisitos del Sistema

- **Python**: 3.7 o superior
- **Java**: 8 o 11 (para PySpark)
- **RAM**: Mínimo 4GB recomendado
- **SO**: Windows/Linux/macOS

## 📈 Datos Generados

### CSV Básico (`propiedades.csv`)
- title, price, location, rooms, bathrooms, area_m2, publisher, url

### Streaming JSON (formato enriquecido)
- Todos los campos anteriores +
- timestamp, property_type, amenities, condition, construction_year
- price_per_m2, floors, parking, description

## 🎯 Casos de Uso Demostrados

1. **ETL en Tiempo Real**: Extracción, transformación y carga continua
2. **Análisis de Mercado**: Estadísticas de precios en vivo
3. **Alertas Automáticas**: Detección de propiedades premium
4. **Calidad de Datos**: Limpieza y validación en streaming
5. **Agregaciones Complejas**: Múltiples métricas simultáneas

## 🚨 Troubleshooting

### Error: "Java not found"
```bash
# Instalar Java 11
# Windows: Descargar desde Oracle/OpenJDK
# Linux: sudo apt install openjdk-11-jdk
# macOS: brew install openjdk@11
```

### Error: "No module named pyspark"
```bash
pip install pyspark==3.4.1
```

### Sin datos en streaming
```bash
# Verificar directorio
ls streaming_data/

# Regenerar datos
python synthetic_data_generator.py
```

## 📝 Notas Importantes

- **Streaming Data**: Los archivos JSON se generan en `streaming_data/`
- **Rate Limiting**: 2 segundos entre requests para respetar el servidor
- **Memory**: Spark usa ~2GB RAM por defecto
- **Performance**: Mejor rendimiento con SSD

## 🎓 Conceptos Demostrados

- **Spark Streaming**: Procesamiento micro-batch
- **Structured Streaming**: API moderna de Spark
- **Window Functions**: Análisis temporal
- **Watermarking**: Manejo de datos tardíos
- **Multiple Sinks**: Múltiples outputs simultáneos
- **Schema Evolution**: Manejo de cambios de estructura

---

## 🏆 ¿Por qué este proyecto es ideal para mostrar Spark Streaming?

1. **✅ Datos Realistas**: Propiedades inmobiliarias reales
2. **✅ Flujo Continuo**: Datos llegan gradualmente
3. **✅ Análisis Variados**: 5 tipos diferentes de consultas
4. **✅ Escalabilidad**: Fácil agregar más fuentes de datos
5. **✅ Visualización**: Resultados claros en consola
6. **✅ Práctica Real**: Caso de uso empresarial típico

¡Perfecto para demostrar las capacidades de Spark Streaming! 🚀
