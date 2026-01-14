import boto3
from pathlib import Path
import os 

def load_func(AWS_ACCESS_KEY, AWS_SECRET_KEY, bucket_name, data_dir, timestamp, logger):
    
    s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
    )

    # --- FILE GATHERING ---
    data_list = [] 

    script_location = Path(__file__).resolve().parent
    path = script_location.parent / data_dir

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