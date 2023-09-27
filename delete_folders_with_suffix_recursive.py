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

#########################################

import boto3
import urllib.parse

def parse_s3_uri(s3_uri):
    parsed_uri = urllib.parse.urlparse(s3_uri)
    if parsed_uri.scheme != 's3':
        raise ValueError("Not an S3 URI")
    
    bucket_name = parsed_uri.netloc
    root_folder = parsed_uri.path.lstrip('/')
    return bucket_name, root_folder

def list_folders(bucket_name, root_folder):
    s3 = boto3.client('s3')
    folders = []
    
    def list_folders_recursive(prefix):
        objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
        
        for obj in objects.get('CommonPrefixes', []):
            folder_name = obj['Prefix']
            folders.append(folder_name)
            list_folders_recursive(folder_name)
    
    list_folders_recursive(root_folder)
    return folders

def delete_folders_with_suffix(bucket_name, folders_to_delete):
    s3 = boto3.client('s3')
    
    for folder in folders_to_delete:
        if folder.endswith('$folder$/'):
            print(f'Deleting folder: {folder}')
            s3.delete_object(Bucket=bucket_name, Key=folder)

# Replace this with your S3 URI
s3_uri = 's3://your-bucket-name/your-root-folder/'

bucket_name, root_folder = parse_s3_uri(s3_uri)
folders = list_folders(bucket_name, root_folder)
delete_folders_with_suffix(bucket_name, folders)

