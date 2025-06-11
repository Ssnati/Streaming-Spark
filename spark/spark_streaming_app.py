from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time

def create_spark_streaming_app():
    """
    Crea una aplicación de Spark Streaming para procesar datos de propiedades en tiempo real.
    """
    
    # Crear SparkSession
    spark = SparkSession.builder \
        .appName("RealEstateStreamingAnalysis") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    # Definir esquema para los datos JSON
    property_schema = StructType([
        StructField("url", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("scraped_at", StringType(), True),
        StructField("title", StringType(), True),
        StructField("price", LongType(), True),
        StructField("location", StringType(), True),
        StructField("rooms", IntegerType(), True),
        StructField("bathrooms", IntegerType(), True),
        StructField("area_m2", IntegerType(), True),
        StructField("floors", IntegerType(), True),
        StructField("parking", IntegerType(), True),
        StructField("description", StringType(), True),
        StructField("amenities", StringType(), True),
        StructField("property_type", StringType(), True),
        StructField("construction_year", IntegerType(), True),
        StructField("condition", StringType(), True),
        StructField("error", StringType(), True)
    ])
      # Leer stream de archivos JSON
    df_stream = spark \
        .readStream \
        .format("json") \
        .schema(property_schema) \
        .option("path", "../data/streaming_data/") \
        .load()
    
    # Limpiar y procesar datos
    df_clean = df_stream \
        .filter(col("error").isNull()) \
        .filter(col("price") > 0) \
        .withColumn("price_millions", round(col("price") / 1000000, 2)) \
        .withColumn("price_per_m2", 
                   when(col("area_m2") > 0, round(col("price") / col("area_m2"), 0))
                   .otherwise(0)) \
        .withColumn("timestamp_parsed", to_timestamp(col("timestamp"))) \
        .withColumn("hour", hour(col("timestamp_parsed"))) \
        .withColumn("minute", minute(col("timestamp_parsed")))
    
    return spark, df_clean

def start_real_time_analytics():
    """
    Inicia múltiples análisis en tiempo real.
    """
    spark, df_clean = create_spark_streaming_app()
    
    print("🚀 Iniciando Spark Streaming para Análisis de Propiedades")
    print("=" * 60)
    
    # 1. Mostrar todas las propiedades procesadas
    query1 = df_clean \
        .select("title", "price_millions", "location", "rooms", "bathrooms", "area_m2", "property_type") \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", False) \
        .option("numRows", 5) \
        .trigger(processingTime="10 seconds") \
        .queryName("AllProperties") \
        .start()
    
    # 2. Estadísticas de precios por ubicación
    query2 = df_clean \
        .groupBy("location") \
        .agg(
            count("*").alias("total_properties"),
            avg("price_millions").alias("avg_price_millions"),
            max("price_millions").alias("max_price_millions"),
            min("price_millions").alias("min_price_millions")
        ) \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", False) \
        .trigger(processingTime="15 seconds") \
        .queryName("PricesByLocation") \
        .start()
    
    # 3. Análisis por tipo de propiedad
    query3 = df_clean \
        .filter(col("property_type") != "N/A") \
        .groupBy("property_type") \
        .agg(
            count("*").alias("count"),
            avg("price_millions").alias("avg_price"),
            avg("area_m2").alias("avg_area")
        ) \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", False) \
        .trigger(processingTime="20 seconds") \
        .queryName("PropertyTypeAnalysis") \
        .start()
    
    # 4. Propiedades con mejor relación calidad-precio
    query4 = df_clean \
        .filter((col("area_m2") > 0) & (col("price_per_m2") > 0)) \
        .select("title", "location", "price_millions", "area_m2", "price_per_m2", "rooms", "bathrooms") \
        .orderBy("price_per_m2") \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", False) \
        .option("numRows", 3) \
        .trigger(processingTime="25 seconds") \
        .queryName("BestValueProperties") \
        .start()
    
    # 5. Alertas de propiedades premium (precio > 500M)
    query5 = df_clean \
        .filter(col("price_millions") > 500) \
        .select("title", "location", "price_millions", "rooms", "bathrooms", "amenities") \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", False) \
        .trigger(processingTime="30 seconds") \
        .queryName("PremiumProperties") \
        .start()
    
    return [query1, query2, query3, query4, query5]

def run_streaming_analysis():
    """
    Ejecuta el análisis de streaming completo.
    """
    try:
        queries = start_real_time_analytics()
        
        print("📊 Análisis de Streaming Activos:")
        print("1. ✅ Todas las propiedades (cada 10s)")
        print("2. ✅ Estadísticas por ubicación (cada 15s)")
        print("3. ✅ Análisis por tipo de propiedad (cada 20s)")
        print("4. ✅ Mejores relaciones calidad-precio (cada 25s)")
        print("5. ✅ Alertas propiedades premium (cada 30s)")
        print("\n⏳ Presiona Ctrl+C para detener...")
        
        # Esperar a que terminen todas las queries
        for query in queries:
            query.awaitTermination()
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo Spark Streaming...")
        for query in queries:
            query.stop()
    except Exception as e:
        print(f"❌ Error en Spark Streaming: {e}")

if __name__ == "__main__":
    run_streaming_analysis()
