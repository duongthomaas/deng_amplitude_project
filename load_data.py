import boto3
from dotenv import load_dotenv 
import os 
import logging 
from datetime import datetime

load_dotenv() 

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
bucket_name = os.getenv("bucket_name")

filename = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

log_filename = f"logs/{filename}.log"

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

data_list =  [] 

path = r"C:\Users\ThomasDuong\Documents\GitHub\deng_amplitude_project\data"

for root, dirs, files in os.walk(path):
    for file in files:
        full_path = os.path.join(root, file)
        data_list.append(full_path)

if len(data_list) > 0:

    for filepath in data_list:

        # 1. Create a session using your specific profile name
        session = boto3.Session(profile_name='til_uk_ds_iam') 
        # 2. Create an S3 client from that session 
        s3 = session.client('s3')

        s3_filename = os.path.basename(filepath)
        s3_filepath=f"python-import/{s3_filename}"

        try:
            s3.upload_file(filepath, bucket_name, s3_filepath)
            # os.remove(filepath)
            logger.info(f"{s3_filename} upload successful at {filename}") 
            print(f"{s3_filename} upload successful")
        except Exception as e:
            print(f"Failed to upload {s3_filepath}: {e}")
            logger.error(f"An error occurred with {s3_filename}: {e}")  
else:
    print("No files uploaded")