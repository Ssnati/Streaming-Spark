from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
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

def main():
    # Configuración de rutas
    input_path = "files/csv"
    checkpoint_path = "checkpoints/streaming_analysis"
    
    # Asegurarse de que exista el directorio de checkpoints
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    
    # Iniciar sesión de Spark
    spark = create_spark_session()
    
    try:
        # Esquema de los datos de entrada
        schema = "title STRING, price STRING, neighborhood STRING, rooms STRING, area_m2 STRING, publisher STRING"
        
        # Configurar el stream
        print("Iniciando el análisis en tiempo real...")
        print(f"Monitoreando la carpeta: {os.path.abspath(input_path)}")
        print("Presiona Ctrl+C para detener\n")
        
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
        print(f"Error durante la ejecución: {str(e)}")
        raise
    finally:
        spark.stop()
        print("Análisis detenido.")

if __name__ == "__main__":
    main()
