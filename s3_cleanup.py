import boto3
from datetime import datetime, timedelta, timezone

def delete_old_files(bucket_name, prefix, days=7):
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Calculate the cutoff date, make it offset-aware by setting UTC timezone
    cutoff_date = datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(days=days)

    # Get the list of files in the bucket
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    # Loop through each page of results
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                last_modified = obj['LastModified']
                # Ensure both datetimes are offset-aware for comparison
                if last_modified < cutoff_date:
                    # Print file name and last modified date
                    print(f"Deleting {obj['Key']}, last modified: {last_modified}")
                    # Delete the file
                    s3.delete_object(Bucket=bucket_name, Key=obj['Key'])

# Example usage
bucket_name = 'your-bucket-name'
prefix = 'your/folder/path/'
days = 7  # Specify the number of days here
delete_old_files(bucket_name, prefix, days)
