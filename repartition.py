import boto3
from pyspark.sql import SparkSession

# Initialize a Spark session
spark = SparkSession.builder.appName("RepartitionParquet").getOrCreate()

# Define the S3 bucket and list of source prefixes
source_bucket = 'bucket'
source_prefixes = [
    'folder1/data/folder2/actual_folder1.parquet/',
    'folder1/data/folder2/actual_folder2.parquet/',
    # Add more source prefixes as needed
]

# Initialize the Boto3 S3 client
s3_client = boto3.client('s3')

# Loop through each source prefix and process Parquet files
for source_prefix in source_prefixes:
    # Define the target prefix for this source folder
    source_prefix_parts = source_prefix.strip('/').split('/')
    target_prefix = '/'.join(source_prefix_parts[:-1]) + f'/{source_prefix_parts[-1]}_stage/'

    # List the Parquet files in the source folder using Boto3
    response = s3_client.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix)
    source_files = [obj['Key'] for obj in response.get('Contents', [])]

    # Process each Parquet file in the source folder
    for source_file in source_files:
        # Read the Parquet file
        df = spark.read.parquet(f's3a://{source_bucket}/{source_file}')

        # Repartition the DataFrame
        df = df.repartition(128)  # Change the number of partitions as needed

        # Create the target file path
        source_file_parts = source_file.split('/')
        target_file = '/'.join(source_file_parts[:-1]) + f'/{source_file_parts[-1]}'

        # Write the repartitioned DataFrame back to S3
        df.write.parquet(f's3a://{source_bucket}/{target_prefix}/{target_file}', mode='overwrite')

# Stop the Spark session
spark.stop()
