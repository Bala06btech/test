import re
import pandas as pd
import boto3

# Define a function to extract table names and columns used from a Spark SQL query
def extract_table_and_columns(query):
    # Define regular expressions for identifying table names and columns
    table_pattern = r'\b(?:FROM|JOIN)\s+([a-zA-Z0-9_]+)'
    column_pattern = r'([a-zA-Z0-9_]+)\s*[,)]'

    # Find all table names and columns used in the query
    table_names = re.findall(table_pattern, query)
    columns_used = re.findall(column_pattern, query)

    return table_names, columns_used

# Define a list to store the extracted data
data = []

# Define a function to process a .py file from S3 and extract table and column details
def process_s3_py_file(bucket_name, file_key):
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Download the .py file from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')
    
    # Use regular expressions to find Spark SQL queries
    sql_queries = re.findall(r'spark\.sql\(.*?\.sql\(["\'](.*?)["\']\)', file_content, re.DOTALL)
    
    # Extract table names and columns from each SQL query
    for idx, query in enumerate(sql_queries, start=1):
        table_names, columns_used = extract_table_and_columns(query)
        
        data.append({
            "Query Number": idx,
            "Table Names": ', '.join(table_names),
            "Columns Used": ', '.join(columns_used)
        })

# AWS S3 bucket details
bucket_name = 'your-s3-bucket-name'
prefix = 'path/to/your/py/files'

# List objects in the S3 bucket
s3 = boto3.client('s3')
objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# Iterate through S3 objects and process each .py file
for obj in objects.get('Contents', []):
    file_key = obj['Key']
    
    # Process the .py file from S3
    process_s3_py_file(bucket_name, file_key)

# Create a DataFrame from the extracted data
query_details_dataframe = pd.DataFrame(data)

# Display the DataFrame
print(query_details_dataframe)
