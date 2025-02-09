from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Création de la session Spark avec les dépendances S3
spark = SparkSession.builder \
    .appName("KafkaTransactionConsumer") \
    .master("local[*]") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3," + 
            "org.apache.hadoop:hadoop-aws:3.3.4," +
            "com.amazonaws:aws-java-sdk-bundle:1.12.261") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "minio123") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .getOrCreate()

# Configuration du niveau de log
spark.sparkContext.setLogLevel("WARN")
spark.conf.set("spark.sql.adaptive.enabled", "false")

# Définition du schéma des données
schema = StructType([
    StructField("id_transaction", StringType(), True),
    StructField("type_transaction", StringType(), True),
    StructField("montant", DoubleType(), True),
    StructField("devise", StringType(), True),
    StructField("date", StringType(), True),
    StructField("lieu", StringType(), True),
    StructField("moyen_paiement", StringType(), True),
    StructField("produit", StringType(), True),
    StructField("quantite", IntegerType(), True),
    StructField("prix_unitaire", DoubleType(), True),
    StructField("id_utilisateur", StringType(), True),
    StructField("nom_utilisateur", StringType(), True),
    StructField("adresse_utilisateur", StringType(), True),
    StructField("email_utilisateur", StringType(), True)
])


# Lecture du flux Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:19092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "earliest") \
    .load()

# Transformation des données
parsed_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

transformed_df = parsed_df \
    .withColumn("date", to_timestamp("date")) \
    .withColumn("timezone", lit("Europe/Paris")) \
    .filter(col("moyen_paiement") != "erreur") \
    .filter(col("adresse_utilisateur").isNotNull()) \
    .filter(col("lieu").isNotNull())

# Écriture en streaming vers MinIO
query = transformed_df \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "s3a://transactions/output") \
    .option("checkpointLocation", "s3a://transactions/checkpoints") \
    .start()

# Pour lire les données depuis MinIO une fois qu'elles sont écrites
def read_from_minio():
    df_minio = spark.read.parquet("s3a://transactions/output")
    print("Schema des données lues depuis MinIO:")
    df_minio.printSchema()
    print("\nAperçu des données:")
    df_minio.show(5)
    return df_minio

read_from_minio()
# Attente de la fin du traitement streaming
query.awaitTermination()

