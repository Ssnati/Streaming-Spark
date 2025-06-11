from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.utils import AnalysisException
import time
import os

def create_spark_session():
    """Crea y retorna una sesión de Spark configurada para streaming."""
    return SparkSession.builder \
        .appName("RealEstateStreamingAnalysis") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()

def process_batch(df, epoch_id):
    """Procesa cada lote de datos del stream."""
    if df.rdd.isEmpty():
        print("No hay datos nuevos para procesar")
        return
    
    # Mostrar información del lote actual
    print(f"\n{'='*50}")
    print(f"Procesando lote {epoch_id} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Número de registros en este lote: {df.count()}")
    
    # Procesar los datos
    processed_df = df.select(
        col("title"),
        col("price").cast("float").alias("price"),
        lower(col("neighborhood")).alias("neighborhood"),
        when(col("area_m2").rlike(r'^\d+$'), col("area_m2").cast("float")).otherwise(None).alias("area_m2"),
        col("publisher")
    ).filter(
        (col("neighborhood").isNotNull()) &
        (col("neighborhood") != "n/a") &
        (col("price") > 0) &
        (col("area_m2") > 0)
    )
    
    # Calcular métricas por barrio
    if not processed_df.rdd.isEmpty():
        metrics_df = processed_df.groupBy("neighborhood").agg(
            count("*").alias("property_count"),
            avg("price").alias("avg_price"),
            avg("price" / col("area_m2")).alias("avg_price_per_m2")
        ).orderBy(desc("property_count"))
        
        print("\n=== Métricas por Barrio ===")
        metrics_df.show(truncate=False)
        
        # Estadísticas generales
        stats = processed_df.agg(
            count("*").alias("total_properties"),
            avg("price").alias("avg_price"),
            avg("area_m2").alias("avg_area_m2"),
            avg("price" / col("area_m2")).alias("avg_price_per_m2")
        )
        
        print("\n=== Estadísticas Generales ===")
        stats.show(truncate=False)
        
        # Mostrar tendencias de precios
        print("\n=== Tendencias de Precios ===")
        price_trends = processed_df.agg(
            min("price").alias("precio_minimo"),
            max("price").alias("precio_maximo"),
            (max("price") - min("price")).alias("rango_precios")
        )
        price_trends.show(truncate=False)
        
        # Top 5 barrios más caros
        print("\n=== Top 5 Barrios más Caros ===")
        metrics_df.orderBy(desc("avg_price")).limit(5).show(truncate=False)
    
    print(f"\nEsperando nuevos datos...")

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
    checkpoint_path = "checkpoints/streaming_analysis"
    
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
        
        # Crear el streaming DataFrame con el esquema inferido
        streaming_df = spark.readStream \
            .schema(schema) \
            .option("header", "true") \
            .option("maxFilesPerTrigger", 1) \
            .csv(input_path)
        
        # Iniciar el procesamiento del stream
        query = streaming_df.writeStream \
            .foreachBatch(process_batch) \
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
