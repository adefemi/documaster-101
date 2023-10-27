import boto3
from decouple import config

s3 = boto3.client(
    's3', 
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    region_name=config("AWS_REGION_NAME")
)

storage_folder = "pdf_files"
bucket_name = config("AWS_BUCKET_NAME")

def upload_file(file):
    try:
        file_bytes = file.file.read()
        key = f'{storage_folder}/{file.filename}'
        s3.put_object(Bucket=bucket_name, Key=key, Body=file_bytes)
        return f'https://{bucket_name}.s3.amazonaws.com/{key}'
    except Exception as _:
        raise Exception("Error uploading file")

def list_files_in_folder():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'{storage_folder}/')
        files = [item['Key'] for item in response.get('Contents', [])]
        return files
    except Exception as e:
        print(e)
        raise Exception("Error listing files in folder: " + str(e))

def get_file_in_folder(file_name):
    try:
        file_key = f'{storage_folder}/{file_name}.pdf'
        file_url = f'https://{bucket_name}.s3.amazonaws.com/{file_key}'
        response = s3.head_object(Bucket='your-bucket-name', Key=file_key)
        return {"file_url": file_url, "metadata": response['Metadata']}
    except s3.exceptions.NoSuchKey:
        raise Exception("File not found")
    
def download_file(file_key):
    try:
        file_path = f'/tmp/{file_key.split("/")[-1]}'
        s3.download_file(bucket_name, file_key, file_path)
        return file_path
    except Exception as e:
        raise Exception(f"Error downloading file: {str(e)}")