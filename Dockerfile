# Usar la imagen base de Spark con Python
FROM bitnami/spark:3.5

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=nonrandom \
    PYSPARK_PYTHON=python3 \
    PYSPARK_DRIVER_PYTHON=python3

# Instalar dependencias del sistema
RUN apt-get update --allow-releaseinfo-change && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
COPY spark_streaming_analysis.py .
COPY web_scraper.py .
COPY files/ ./files/

# Instalar dependencias de Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Puerto predeterminado para Spark UI
EXPOSE 4040 8080 7077

# Comando por defecto: iniciar el script de Spark Streaming
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", "spark_streaming_analysis.py"]
