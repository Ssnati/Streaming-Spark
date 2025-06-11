from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.utils import AnalysisException
from pyspark.sql import functions as F
import time
import os

def format_currency(col_name):
    """Formatea una columna numérica como moneda colombiana."""
    return F.format_string("$%,.0f", F.col(col_name)).alias(col_name)

def format_float(col_name, decimals=2):
    """Formatea una columna numérica con separadores de miles y decimales opcionales."""
    return F.format_string("%,.{}f".format(decimals), F.col(col_name)).alias(col_name)

def create_spark_session():
    """Crea y retorna una sesión de Spark configurada para streaming."""
    return SparkSession.builder \
        .appName("RealEstateStreamingAnalysis") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()

def run_full_analysis(batch_df, epoch_id, spark, input_path, schema):
    """
    Esta función se activa cada vez que se detectan archivos nuevos en el stream.
    Lee TODOS los archivos CSV del directorio de entrada y realiza un análisis completo.
    """
    print(f"\n{'='*50}")
    print(f"Lote {epoch_id} detectado a las {time.strftime('%Y-%m-%d %H:%M:%S')}")

    if batch_df.rdd.isEmpty():
        print("No hay datos nuevos en este lote. Esperando...")
        return

    print("Nuevos archivos detectados. Realizando análisis completo del conjunto de datos acumulado...")

    try:
        # Lee todos los archivos del directorio en un DataFrame estático
        full_df = spark.read \
            .schema(schema) \
            .option("header", "true") \
            .csv(input_path)
        
        if full_df.rdd.isEmpty():
            print("El directorio de entrada no contiene datos válidos para analizar.")
            return

    except Exception as e:
        print(f"Error al leer el conjunto de datos completo: {e}")
        return

    # Procesar los datos (lógica de la función process_batch original)
    processed_df = full_df.select(
        col("title"),
        col("price").cast("float").alias("price"),
        lower(col("neighborhood")).alias("neighborhood"),
        when(col("area_m2").rlike(r'^\d+$'), col("area_m2").cast("float"))
            .otherwise(None)
            .alias("area_m2"),
        col("publisher")
    ).filter(
        (col("neighborhood").isNotNull()) &
        (col("neighborhood") != "n/a") &
        (col("neighborhood") != "") &
        (col("price") > 0) &
        (col("area_m2").isNotNull()) &
        (col("area_m2") > 0)
    ).withColumn(
        "price_per_m2",
        col("price") / col("area_m2")
    )

    # Cache el DataFrame procesado para mejorar el rendimiento de los cálculos siguientes
    processed_df.cache()
    
    # Calcular métricas por barrio
    if not processed_df.rdd.isEmpty():
        print("\n=== ANÁLISIS COMPLETO ACUMULADO ===")
        
        metrics_df = processed_df.groupBy("neighborhood").agg(
            count("*").alias("property_count"),
            avg("price").alias("avg_price"),
            avg("price_per_m2").alias("avg_price_per_m2")
        ).orderBy(desc("property_count"))
        
        # Mostrar métricas por barrio
        print("\n--- Métricas por Barrio ---")
        metrics_formatted = metrics_df.select(
            "neighborhood",
            "property_count",
            format_currency("avg_price"),
            format_currency("avg_price_per_m2")
        )
        metrics_formatted.show(truncate=False)
        
        # Estadísticas generales
        stats = processed_df.agg(
            count("*").alias("total_properties"),
            avg("price").alias("avg_price"),
            avg("area_m2").alias("avg_area_m2"),
            avg("price_per_m2").alias("avg_price_per_m2")
        )
        
        print("\n--- Estadísticas Generales ---")
        stats_formatted = stats.select(
            "total_properties",
            format_currency("avg_price"),
            format_float("avg_area_m2", 1),
            format_currency("avg_price_per_m2")
        )
        stats_formatted.show(truncate=False)
        
        # Mostrar tendencias de precios
        print("\n--- Tendencias de Precios ---")
        price_trends = processed_df.agg(
            min("price").alias("precio_minimo"),
            max("price").alias("precio_maximo"),
            (max("price") - min("price")).alias("rango_precios")
        )
        price_trends_formatted = price_trends.select(
            format_currency("precio_minimo"),
            format_currency("precio_maximo"),
            format_currency("rango_precios")
        )
        price_trends_formatted.show(truncate=False)
        
        # Top 5 barrios más caros
        print("\n--- Top 5 Barrios más Caros (por precio promedio) ---")
        top_neighborhoods = metrics_df.orderBy(desc("avg_price")).limit(5)
        top_neighborhoods_formatted = top_neighborhoods.select(
            "neighborhood",
            "property_count",
            format_currency("avg_price"),
            format_currency("avg_price_per_m2")
        )
        top_neighborhoods_formatted.show(truncate=False)
    
    # Liberar el cache
    processed_df.unpersist()
    
    print(f"\n{'='*50}")
    print("Análisis completo finalizado. Esperando nuevos archivos...")

def infer_schema(spark, input_path):
    """Infers schema from the first CSV file in the input directory."""
    try:
        # Read a sample of the first CSV file
        sample_df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(input_path) \
            .limit(1)
            
        if sample_df.rdd.isEmpty():
            raise ValueError(f"No se encontraron archivos CSV en {os.path.abspath(input_path)}")
            
        return sample_df.schema
        
    except AnalysisException as e:
        raise ValueError(f"Error al inferir el esquema: {str(e)}")

def main():
    # Configuración de rutas
    input_path = "files/csv"
    checkpoint_path = "checkpoints/streaming_analysis_full"
    
    # Asegurarse de que existan los directorios necesarios
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    os.makedirs(input_path, exist_ok=True)
    
    # Iniciar sesión de Spark
    spark = create_spark_session()
    
    try:
        # Inferir el esquema del primer archivo CSV
        print("Inferiendo esquema del primer archivo CSV...")
        schema = infer_schema(spark, input_path)
        
        # Mostrar el esquema inferido
        print("\nEsquema inferido:")
        for field in schema.fields:
            print(f"- {field.name}: {field.dataType}")
        
        # Configurar el stream
        print("\nIniciando el análisis en tiempo real...")
        print(f"Monitoreando la carpeta: {os.path.abspath(input_path)}")
        print("Presiona Ctrl+C para detener\n")
        
        # Crear el streaming DataFrame. Se usará como disparador.
        streaming_df = spark.readStream \
            .schema(schema) \
            .option("header", "true") \
            .csv(input_path)
        
        # Iniciar el procesamiento del stream
        # Usamos foreachBatch para ejecutar nuestro análisis completo cada vez que llegan datos nuevos.
        query = streaming_df.writeStream \
            .foreachBatch(lambda df, epoch_id: run_full_analysis(df, epoch_id, spark, input_path, schema)) \
            .outputMode("append") \
            .option("checkpointLocation", checkpoint_path) \
            .start()
        
        query.awaitTermination()
        
    except KeyboardInterrupt:
        print("\nDeteniendo el análisis...")
        if 'query' in locals():
            query.stop()
    except Exception as e:
        print(f"\nError durante la ejecución: {str(e)}")
        print("Asegúrate de que hay archivos CSV en el directorio y que tienen el formato correcto.")
        print(f"Directorio actual: {os.path.abspath(input_path)}")
        print("\nPosibles soluciones:")
        print("1. Verifica que el directorio 'files/csv' existe y contiene archivos CSV")
        print("2. Asegúrate de que los archivos CSV tienen encabezados en la primera fila")
        print("3. Comprueba que tienes permisos de lectura en el directorio")
        raise
    finally:
        if 'spark' in locals():
            spark.stop()
            print("Análisis detenido.")

if __name__ == "__main__":
    main()

