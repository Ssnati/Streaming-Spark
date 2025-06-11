from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
from datetime import datetime

# Configuración de Spark
spark = SparkSession.builder \
    .appName("FileByFileAnalysis") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

def load_and_process_data():
    # Cargar datos de propiedades
    print("Cargando datos de propiedades...")
    properties_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv("files/csv/*.csv")
    
    # Procesar datos de propiedades
    print("Procesando datos de propiedades...")
    properties_processed = properties_df.select(
        col("title"),
        col("price").cast("float"),
        col("neighborhood"),
        when(col("rooms").rlike(r'^\d+$'), col("rooms").cast("int")).otherwise(None).alias("rooms"),
        when(col("area_m2").rlike(r'^\d+$'), col("area_m2").cast("float")).otherwise(None).alias("area_m2"),
        col("publisher")
    )
    
    # Cargar datos de barrios
    print("Cargando datos de barrios...")
    barrios_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv("files/barrios_tunja_completo.csv")
    
    # Procesar datos de barrios
    print("Procesando datos de barrios...")
    barrios_processed = barrios_df.select(
        lower(col("nombre")).alias("neighborhood"),
        col("poblacion").cast("int"),
        col("viviendas").cast("int"),
        col("area").cast("float").alias("area_hectareas")
    )
    
    return properties_processed, barrios_processed

def analyze_data(properties_df, barrios_df):
    # Filtrar propiedades con barrio conocido
    print("Filtrando propiedades con barrio conocido...")
    properties_with_neighborhood = properties_df.filter(
        (col("neighborhood").isNotNull()) & 
        (col("neighborhood") != "N/A") &
        (col("price").isNotNull()) &
        (col("area_m2").isNotNull())
    )
    
    # Convertir nombre del barrio a minúsculas para hacer match consistente
    properties_with_neighborhood = properties_with_neighborhood.withColumn(
        "neighborhood", 
        lower(col("neighborhood"))
    )
    
    # Unir con datos de barrios
    print("Uniendo datos de propiedades con datos de barrios...")
    joined_df = properties_with_neighborhood.join(
        barrios_df, 
        "neighborhood",
        "left_outer"
    )
    
    # Calcular métricas
    print("Calculando métricas...")
    metrics_df = joined_df.groupBy("neighborhood").agg(
        count("*").alias("property_count"),
        avg("price").alias("avg_price"),
        avg("price" / col("area_m2")).alias("avg_price_per_m2"),
        avg("poblacion" / col("viviendas").cast("float")).alias("avg_people_per_house"),
        first("poblacion").alias("population"),
        first("viviendas").alias("total_houses"),
        first("area_hectareas").alias("area_hectares")
    ).orderBy(desc("property_count"))
    
    # Mostrar resultados
    print("\n=== Análisis de Propiedades por Barrio ===")
    print(f"Total de barrios con propiedades: {metrics_df.count()}")
    metrics_df.show(truncate=False)
    
    # Mostrar estadísticas generales
    stats_df = properties_with_neighborhood.agg(
        count("*").alias("total_properties"),
        avg("price").alias("avg_price"),
        avg("area_m2").alias("avg_area_m2"),
        avg("price" / col("area_m2")).alias("avg_price_per_m2")
    )
    
    print("\n=== Estadísticas Generales ===")
    stats_df.show(truncate=False)
    
    return metrics_df

def save_results(df, output_dir="output"):
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Generar nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"analysis_results_{timestamp}")
    
    # Guardar resultados
    print(f"\nGuardando resultados en {output_path}...")
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_path)
    print("Análisis completado y resultados guardados exitosamente!")

def main():
    try:
        # Cargar y procesar datos
        properties_df, barrios_df = load_and_process_data()
        
        # Realizar análisis
        results_df = analyze_data(properties_df, barrios_df)
        
        # Guardar resultados
        save_results(results_df)
        
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
