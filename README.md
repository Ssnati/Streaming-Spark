# 🏠 Análisis de Propiedades Inmobiliarias con Spark

Proyecto de análisis de datos inmobiliarios que combina web scraping con procesamiento por lotes y en tiempo real usando Apache Spark 3.4.1.

## 🚀 Características Principales

### 🔍 Web Scraping
- Extracción de propiedades desde portales inmobiliarios
- Paginación automática
- Extracción inteligente de barrios
- Guardado en CSV con timestamps

### 📊 Procesamiento de Datos
- Análisis por lotes (Batch)
- Procesamiento en tiempo real (Streaming)
- Métricas por barrio
- Limpieza y validación de datos

## 🛠️ Instalación

### Requisitos
- Python 3.7+
- Java 8/11
- 4GB RAM mínimo
- Linux/macOS

### Pasos de instalación
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/streaming-spark.git
cd streaming-spark

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 🚀 Uso

### 1. Extraer datos
```bash
# Extraer 3 páginas
python web_scraper.py --pages 3

# Solo primera página
python web_scraper.py --single
```

### 2. Análisis por lotes
```bash
python spark_streaming_analysis.py
```

### 3. Procesamiento en tiempo real
```bash
python streaming_analysis.py
```

## 📁 Estructura del Proyecto

```
.
├── files/
│   └── csv/                    # Archivos CSV
├── output/                     # Resultados
├── web_scraper.py             # Script de scraping
├── spark_streaming_analysis.py # Análisis batch
└── streaming_analysis.py       # Análisis en tiempo real
```

## 🛠️ Solución de Problemas

### Java no encontrado
```bash
# Linux
sudo apt install openjdk-11-jdk
```

### Error de PySpark
```bash
pip install pyspark==3.4.1
```

### Datos faltantes
- Verifica que los archivos CSV estén en `files/csv/`
- Revisa los logs para mensajes de error