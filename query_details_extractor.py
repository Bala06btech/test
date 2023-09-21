import re
import os
import pandas as pd

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

# Define a function to process a .py file and extract table and column details
def process_py_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Use regular expressions to find Spark SQL queries
        sql_queries = re.findall(r'spark\.sql\(.*?\.sql\(["\'](.*?)["\']\)', content, re.DOTALL)
        
        # Extract table names and columns from each SQL query
        for idx, query in enumerate(sql_queries, start=1):
            table_names, columns_used = extract_table_and_columns(query)
            
            data.append({
                "File": file_path,
                "Query Number": idx,
                "Table Names": ', '.join(table_names),
                "Columns Used": ', '.join(columns_used)
            })

# Define the directory containing the .py files
directory = '/path/to/your/py/files'

# Iterate through .py files in the directory and process each file
for filename in os.listdir(directory):
    if filename.endswith('.py'):
        file_path = os.path.join(directory, filename)
        process_py_file(file_path)

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
