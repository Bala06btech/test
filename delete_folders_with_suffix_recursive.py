import boto3

def delete_folders_with_suffix_recursive(bucket_name, root_folder):
    s3 = boto3.client('s3')
    
    def delete_objects_in_folder(prefix):
        objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        for obj in objects.get('Contents', []):
            key = obj['Key']
            if key.endswith('$folder$'):
                print(f'Deleting folder: {key}')
                s3.delete_object(Bucket=bucket_name, Key=key)
            elif key.endswith('/'):
                # Recursively delete subfolders
                delete_objects_in_folder(key)
    
    delete_objects_in_folder(root_folder)

# Replace these values with your own
bucket_name = 'your-bucket-name'
root_folder = 'your-root-folder/'

delete_folders_with_suffix_recursive(bucket_name, root_folder)
