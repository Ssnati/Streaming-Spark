# 🏠 Análisis de Propiedades Inmobiliarias con Spark

Proyecto de análisis de datos inmobiliarios que combina web scraping con procesamiento en tiempo real utilizando Apache Spark 3.4.1. El sistema está diseñado para monitorear un directorio y analizar datos de archivos CSV a medida que llegan, ofreciendo dos modos de análisis distintos.

## 🚀 Características Principales

### 🔍 Web Scraping
- **`web_scraper.py`**: Script para extraer propiedades de portales inmobiliarios.
- Soporta paginación automática para obtener un gran volumen de datos.
- Extrae y limpia información clave como precio, área, barrio y publicador.
- Guarda los resultados en archivos CSV individuales dentro de la carpeta `files/csv`.

### 📊 Procesamiento de Datos con Spark Streaming
El proyecto ofrece dos enfoques para el análisis de datos en tiempo real:

1.  **Análisis Uno por Uno (`streaming_analysis_one_by_one.py`)**:
    - Procesa cada nuevo archivo CSV de forma individual e independiente.
    - Ideal para ver el impacto y las características de cada lote de datos nuevo.

2.  **Análisis Acumulativo (`streaming_analysis_acumulative.py`)**:
    - Cada vez que se añade un nuevo archivo, vuelve a analizar el **conjunto completo** de datos en la carpeta.
    - Proporciona una visión global y actualizada del mercado con toda la información disponible.

3.  **Análisis "Todo en Uno" (`all_in_one_streaming.py`)**:
    - Un script avanzado que combina múltiples técnicas de streaming en una sola ejecución:
    - **Conteo por Ventanas de Tiempo**: Analiza la frecuencia de palabras en los títulos de las propiedades en ventanas de tiempo deslizantes.
    - **Extracción de Palabras con Números**: Identifica y extrae palabras que contienen dígitos en cualquier campo de texto.
    - **Unión de Múltiples Flujos**: Combina y procesa datos de dos directorios de entrada (`files/csv` y `files/csv2`) simultáneamente.

#### Métricas Generadas en Cada Análisis:
- **Métricas por Barrio**: Conteo de propiedades, precio promedio y precio por m².
- **Estadísticas Generales**: Resumen total de propiedades y promedios generales.
- **Tendencias de Precios**: Rango de precios (mínimo y máximo).
- **Top 5 Barrios Más Caros**: Clasificación basada en el precio promedio.
- **Propiedades Destacadas**: Una tabla detallada con la propiedad más cara y la más barata del conjunto de datos analizado.

## 🛠️ Instalación

### Requisitos
- Python 3.7+
- Java 8 o 11 (Requerido)
- Mínimo 4GB de RAM
- Sistema Operativo: Linux o macOS

### Pasos de Instalación
```bash
# 1. Clonar el repositorio
git clone https://github.com/Ssnati/Streaming-Spark.git
cd Streaming-Spark

# 2. Verificar la version de Java
java -version
# En caso de no ser la requerida, instalar la 11 y cambiarla en el sistema operativo
sudo apt-get install openjdk-11-jdk
sudo update-alternatives --config java

# 3. Crear y activar un entorno virtual
# En Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# 4. Instalar las dependencias
pip install -r requirements.txt
```

## 🚀 Uso

### Paso 1: Extraer Datos (Opcional)
> **Recuerda que, de ahora en adelante, debes ejecutar los comandos con `sudo` para evitar problemas de permisos y para que los archivos se guarden correctamente.**

Si no tienes archivos CSV, puedes generarlos con el scraper. Los archivos se guardarán en `files/csv/`.

```bash
# Extraer datos de las primeras 3 páginas
python web_scraper.py --pages 3

# O solo de la primera página
python web_scraper.py --single
```

### Paso 2: Ejecutar un Análisis en Tiempo Real
Elige uno de los dos modos de análisis. El script comenzará a monitorear la carpeta `files/csv`. Puedes añadir, mover o eliminar archivos CSV en esa carpeta para ver cómo se actualiza el análisis.

**Opción A: Análisis Uno por Uno**
```bash
python streaming_analysis_one_by_one.py
```

**Opción B: Análisis Acumulativo**
```bash
python streaming_analysis_acumulative.py
```

**Opción C: Análisis "Todo en Uno"**
```bash
python all_in_one_streaming.py
```

> **Tips:** Para ver como se actualiza el stream y la consola, ejecuta en otra terminal el script para scrapear datos con una página más. De esta forma, el análisis en tiempo real detectará los nuevos archivos CSV y mostrará los resultados actualizados.

*Presiona `Ctrl+C` en la terminal para detener el script de análisis.*

## 📁 Estructura del Proyecto
```
.
├── checkpoints/              # Directorios para los puntos de control de Spark
├── files/
│   └── csv/                # Carpeta monitoreada para archivos CSV de entrada
├── .venv/                    # Entorno virtual de Python
├── web_scraper.py            # Script de web scraping
├── streaming_analysis_one_by_one.py # Análisis de streaming (archivo por archivo)
├── streaming_analysis_acumulative.py  # Análisis de streaming (acumulativo)
├── all_in_one_streaming.py        # Script con múltiples análisis de streaming
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

## 🛠️ Solución de Problemas

- **Error de `pyspark` no encontrado**: Asegúrate de haber activado el entorno virtual (`source .venv/bin/activate` o `.venv\Scripts\activate`) antes de ejecutar los scripts.
- **Error de Java**: Verifica que Java 8 o 11 esté instalado y que la variable de entorno `JAVA_HOME` esté configurada correctamente.
- **Permisos en Linux/macOS**: Si encuentras errores de permisos, asegúrate de que los scripts tengan permisos de ejecución (`chmod +x *.py`).
- **Error de update de linux**: Si encuentras errores de update de linux, ejecuta el siguiente comando:
```bash
sudo apt update
```
- **Java no encontrado o version incorrecta**: La version de Java debe ser 8 o 11. Si encuentras errores de Java, ejecuta el siguiente comando:
```bash
sudo apt install openjdk-11-jdk
sudo update-alternatives --config java
```

## 👥 Créditos
<center>
Hecho por Santiago Orjuela, Sebastián Rueda y Zarith Gomez
</center>