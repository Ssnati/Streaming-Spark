# Web Scraper - Fincaraíz

Proyecto de web scraping para extraer información de propiedades inmobiliarias desde Fincaraíz Colombia.

## Instalación

### Opción 1: Instalar todas las dependencias
```bash
pip install -r requirements.txt
```

### Opción 2: Instalar solo dependencias mínimas
```bash
pip install -r requirements-min.txt
```

## Uso

Ejecutar el scraper:
```bash
python Spark.py
```

El script extraerá información de las primeras 5 páginas de casas en venta en Tunja, Boyacá y guardará los datos en `propiedades.csv`.

## Datos extraídos

- Título de la propiedad
- Precio
- Ubicación
- Número de habitaciones
- Número de baños
- Área en m²
- Inmobiliaria/Publisher
- URL de la propiedad

## Archivos generados

- `propiedades.csv`: Datos de las propiedades en formato CSV
- `data/html_response_paginaX.html`: Respuestas HTML guardadas de cada página (para debugging)
- `barrios_tunja_completo.csv`: Datos de barrios de Tunja convertidos desde KML

## Estructura del proyecto

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
