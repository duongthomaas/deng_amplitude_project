import boto3
from dotenv import load_dotenv 
import os 
import logging 
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv() 

# Ensure these match the keys in your .env file exactly
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
bucket_name = os.getenv("bucket_name")

# --- LOGGING SETUP ---
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

# Fix: Ensure 'logs' directory exists before writing, or code will crash for new users
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_filename = log_dir / f"{timestamp}.log"

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=str(log_filename)
)

logger = logging.getLogger()

# --- AWS CONNECTION ---
# Optimization: Initialize the client ONCE, outside the loop
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# --- FILE GATHERING ---
data_list = [] 

script_location = Path(__file__).resolve().parent
path = script_location / "data"

# Check if path exists to avoid errors
if path.exists():
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            data_list.append(full_path)
else:
    print(f"Warning: Folder not found at {path}")

# --- UPLOAD LOOP ---
if len(data_list) > 0:

    for filepath in data_list:
        
        s3_filename = os.path.basename(filepath)
        s3_filepath = f"python-import/{s3_filename}"

        try:
            s3_client.upload_file(filepath, bucket_name, s3_filepath)
            
            # os.remove(filepath)
            
            logger.info(f"{s3_filename} upload successful at {timestamp}") 
            print(f"{s3_filename} upload successful")
            
        except Exception as e:
            print(f"Failed to upload {s3_filepath}: {e}")
            logger.error(f"An error occurred with {s3_filename}: {e}")  
else:
    print("No files uploaded")