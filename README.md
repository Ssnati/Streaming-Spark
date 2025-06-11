# Web Scraper + Spark Streaming - Fincaraíz

Proyecto completo que demuestra web scraping y procesamiento en tiempo real con Spark Streaming para propiedades inmobiliarias.

## 🚀 Características

### 1. Web Scraping Básico
- Extracción de propiedades desde Fincaraíz Colombia
- Paginación automática (5 páginas)
- Datos guardados en CSV

### 2. Spark Streaming (⭐ NUEVO)
- Procesamiento de datos en tiempo real
- Múltiples análisis simultáneos
- Generación de datos sintéticos para demo

## 📦 Instalación

### Opción 1: Dependencias completas
```bash
pip install -r requirements.txt
```

### Opción 2: Solo dependencias esenciales
```bash
pip install -r requirements-min.txt
```

### Opción 3: Solo para Spark Streaming
```bash
pip install pyspark pandas
```

## 🎯 Uso

### 🚀 PUNTO DE ENTRADA PRINCIPAL (RECOMENDADO)
```bash
python main.py
```

### Opciones Individuales

#### Web Scraping Básico
```bash
python scraping/Spark.py
```

#### 🔥 Demo Spark Streaming
```bash
cd spark
python spark_streaming_demo.py
```

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
📁 Electiva-4/
├── 📄 main.py                    # 🎯 PUNTO DE ENTRADA PRINCIPAL
├── 📄 README.md                  # Documentación completa
├── 📄 requirements-min.txt       # Dependencias esenciales
├── 📄 requirements.txt           # Todas las dependencias
├── 📄 .gitignore                 # Configuración Git
│
├── 📁 scraping/                  # Módulos de web scraping
│   ├── 📄 __init__.py           # Inicialización del módulo
│   ├── 📄 Spark.py              # Scraper básico de Fincaraíz
│   └── 📄 detailed_scraper.py   # Scraper detallado individual
│
├── 📁 spark/                     # Módulos de Spark Streaming
│   ├── 📄 __init__.py           # Inicialización del módulo
│   ├── 📄 spark_streaming_app.py      # Motor de Spark Streaming
│   ├── 📄 spark_streaming_demo.py     # 🎯 Demo completo
│   ├── 📄 synthetic_data_generator.py # Generador de datos
│   └── 📄 streaming_coordinator.py    # Coordinador del sistema
│
└── 📁 data/                      # Datos y archivos generados
    ├── 📄 __init__.py           # Inicialización del módulo
    ├── 📄 propiedades.csv       # Datos de propiedades
    ├── 📄 html_response_*.html  # Respuestas HTML guardadas
    └── 📁 streaming_data/       # Datos para Spark (se crea automáticamente)
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
