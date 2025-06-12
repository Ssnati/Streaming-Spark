from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col, regexp_extract, lower, current_timestamp, window
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType
import os

# Crear SparkSession
spark = SparkSession.builder \
    .appName("AllInOneStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Asegurarse de que los directorios de entrada existan
input_path1 = "files/csv"
input_path2 = "files/csv2"
os.makedirs(input_path1, exist_ok=True)
os.makedirs(input_path2, exist_ok=True)

# Definir el esquema de los CSV
schema = StructType() \
    .add("title", StringType()) \
    .add("price", DoubleType()) \
    .add("location", StringType()) \
    .add("neighborhood", StringType()) \
    .add("rooms", IntegerType()) \
    .add("bathrooms", IntegerType()) \
    .add("area_m2", IntegerType()) \
    .add("publisher", StringType()) \
    .add("url", StringType())

# Leer dos flujos desde carpetas diferentes
df_csv1 = spark.readStream \
    .option("header", "true") \
    .schema(schema) \
    .csv(input_path1)

df_csv2 = spark.readStream \
    .option("header", "true") \
    .schema(schema) \
    .csv(input_path2)

# ========== PARTE 1: Conteo por ventanas ==========
words1 = df_csv1 \
    .withColumn("timestamp", current_timestamp()) \
    .select(explode(split(col("title"), r"\s+")).alias("word"), col("timestamp"))

windowed_counts = words1 \
    .withWatermark("timestamp", "30 seconds") \
    .groupBy(window(col("timestamp"), "10 seconds", "5 seconds"), col("word")) \
    .count()

# ========== PARTE 2: Palabras con números ==========
from pyspark.sql.functions import when

# Detectar columnas de texto y extraer palabras con números
def extract_words_with_digits(df):
    cols = [c for c, t in df.dtypes if t == "string"]
    exploded = None
    for c in cols:
        e = df.select(explode(split(col(c), r"\s+")).alias("word")).filter(col("word").rlike(r"\d"))
        exploded = e if exploded is None else exploded.union(e)
    return exploded.distinct()

words_with_digits = extract_words_with_digits(df_csv1)

# ========== PARTE 3: Unión de dos flujos ==========
words2 = df_csv2 \
    .withColumn("timestamp", current_timestamp()) \
    .select(explode(split(col("title"), r"\s+")).alias("word"), col("timestamp"))

# Unión de palabras de ambos flujos
union_words = words1.select("word", "timestamp").union(words2.select("word", "timestamp"))

union_counts = union_words \
    .withWatermark("timestamp", "30 seconds") \
    .groupBy(window(col("timestamp"), "10 seconds", "5 seconds"), col("word")) \
    .count()

# ========== Salida ==========
query1 = windowed_counts.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("numRows", 50) \
    .option("truncate", False) \
    .start()

query2 = words_with_digits.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("numRows", 50) \
    .option("truncate", False) \
    .start()

query3 = union_counts.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("numRows", 50) \
    .option("truncate", False) \
    .start()

# Esperar terminación
query1.awaitTermination()
query2.awaitTermination()
query3.awaitTermination()
