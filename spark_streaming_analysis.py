from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

# Configuración de Spark
spark = SparkSession.builder \
    .appName("RealEstateAnalysis") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

# Definir el esquema para los datos de propiedades
property_schema = StructType([
    StructField("title", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("location", StringType(), True),
    StructField("neighborhood", StringType(), True),
    StructField("rooms", StringType(), True),
    StructField("bathrooms", StringType(), True),
    StructField("area_m2", StringType(), True),
    StructField("publisher", StringType(), True),
    StructField("url", StringType(), True)
])

# Cargar datos de barrios (datos estáticos)
barrios_df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("files/barrios_tunja_completo.csv")

# Limpiar y seleccionar columnas relevantes de barrios
barrios_df = barrios_df.select(
    col("nombre").alias("neighborhood"),
    col("poblacion").cast("int"),
    col("viviendas").cast("int"),
    col("area").cast("float").alias("area_hectareas")
)

def process_properties(df, epoch_id):
    if df.count() == 0:
        return
    
    # Procesar datos de propiedades
    properties_df = df.select(
        col("title"),
        col("price"),
        col("neighborhood"),
        when(col("rooms").rlike(r'^\d+$'), col("rooms").cast("int")).otherwise(None).alias("rooms"),
        when(col("area_m2").rlike(r'^\d+$'), col("area_m2").cast("int")).otherwise(None).alias("area_m2"),
        col("publisher")
    )
    
    # Filtrar propiedades con barrio conocido
    properties_with_neighborhood = properties_df.filter(col("neighborhood") != "N/A")
    
    # Unir con datos de barrios
    joined_df = properties_with_neighborhood.join(
        barrios_df, 
        lower(properties_with_neighborhood["neighborhood"]) == lower(barrios_df["neighborhood"]),
        "left_outer"
    )
    
    # Calcular métricas
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
    stats_df = properties_df.agg(
        count("*").alias("total_properties"),
        avg("price").alias("avg_price"),
        avg("area_m2").alias("avg_area_m2"),
        avg("price" / col("area_m2")).alias("avg_price_per_m2")
    )
    
    print("\n=== Estadísticas Generales ===")
    stats_df.show(truncate=False)

# Configurar el stream de Spark
streaming_df = spark.readStream \
    .schema(property_schema) \
    .option("header", "true") \
    .option("maxFilesPerTrigger", 1) \
    .csv("files/csv/*.csv")

# Procesar el stream
query = streaming_df.writeStream \
    .foreachBatch(process_properties) \
    .outputMode("update") \
    .start()

print("Iniciando el análisis en tiempo real...")
print("Presiona Ctrl+C para detener")

try:
    query.awaitTermination()
except KeyboardInterrupt:
    print("\nDeteniendo el análisis...")
    query.stop()
    spark.stop()
