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
    
    # Split the file content into lines
    lines = file_content.split('\n')
    
    # Initialize line number
    line_number = 0
    
    # Initialize query buffer
    query_buffer = []
    
    # Iterate through the lines of the file
    for line in lines:
        # Increment the line number
        line_number += 1
        
        # Check if the line contains a Spark SQL query
        if 'spark.sql' in line:
            # Start building the query
            query_buffer.append(line)
            
            # Keep reading lines until the query is complete
            while not line.strip().endswith(')'):
                line = lines[line_number]
                query_buffer.append(line)
                line_number += 1
            
            # Join the lines to form the complete query
            query = '\n'.join(query_buffer)
            
            # Use regular expressions to find Spark SQL queries
            sql_queries = re.findall(r'spark\.sql\(.*?\.sql\(["\'](.*?)["\']\)', query, re.DOTALL)
            
            # Extract table names and columns from each SQL query
            for idx, query in enumerate(sql_queries, start=1):
                table_names, columns_used = extract_table_and_columns(query)
                
                data.append({
                    "File": file_key,
                    "Line Number": line_number,
                    "Query Number": idx,
                    "Table Names": ', '.join(table_names),
                    "Columns Used": ', '.join(columns_used)
                })

# AWS S3 bucket details
bucket_name = 'your-s3-bucket-name'
prefix = 'path/to/your/py/files'

# Create an S3 client
s3 = boto3.client('s3')

# List objects in the S3 bucket
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
