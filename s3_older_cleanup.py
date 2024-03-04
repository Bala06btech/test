import boto3
from datetime import datetime, timedelta, timezone

# Your AWS S3 bucket name
bucket_name = 'your-bucket-name'
# The folder path in your bucket
folder_path = 'your/folder/path/'
# Setting up the S3 client
s3 = boto3.client('s3')

def delete_old_files(bucket, folder):
    # Calculate the date 30 days ago from now
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    
    # List all objects within the specified folder
    objects_to_delete = []
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=folder)
    
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                # If the object is older than 30 days, mark it for deletion
                if obj['LastModified'] < thirty_days_ago:
                    objects_to_delete.append({'Key': obj['Key']})
    
    # Delete the objects that are older than 30 days
    if objects_to_delete:
        response = s3.delete_objects(
            Bucket=bucket,
            Delete={
                'Objects': objects_to_delete
            }
        )
        print(f"Deleted {len(objects_to_delete)} objects")
    else:
        print("No objects older than 30 days to delete")

# Run the function
delete_old_files(bucket_name, folder_path)
