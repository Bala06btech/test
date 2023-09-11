import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import pandas as pd
from openpyxl import load_workbook

# Initialize AWS Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_bucket', 'output_bucket', 'input_prefix', 'output_prefix'])

# Read Excel file with specific sheet name using pandas
excel_file_path = f"s3://{args['input_bucket']}/{args['input_prefix']}"
sheet_name = "Sheet1"

# Load Excel data into a pandas DataFrame
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# Perform transformations if needed
# For example: df['newColumn'] = df['oldColumn'] + 1

# Write DataFrame to Excel file with specific sheet name using openpyxl
output_excel_file_path = f"s3://{args['output_bucket']}/{args['output_prefix']}"
sheet_name_output = "Sheet2"

# Create a Pandas Excel writer using openpyxl
with pd.ExcelWriter(output_excel_file_path, engine='openpyxl') as writer:
    # Write the DataFrame to the specified sheet
    df.to_excel(writer, sheet_name=sheet_name_output, index=False)

# Commit the Glue job
job.commit()
