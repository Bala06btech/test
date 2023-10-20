import os
import boto3

def list_folders(s3_client, bucket_name):
    folders = set()
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='TWEAKS/')

    for content in response.get('Contents', []):
        folders.add(os.path.dirname(content['Key']))

    return sorted(folders)

s3 = boto3.client("s3")
folder_list = list_folders(s3, 'mybucket')

for folder in folder_list:
    print('Folder found: %s' % folder)
