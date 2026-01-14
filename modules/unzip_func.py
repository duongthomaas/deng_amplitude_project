import zipfile ## Handles ZIP archive files
import gzip ## Handles GZIP compressed files
import os 
import shutil
import tempfile 

def unzip_func(data_dir):
    temp_dir = tempfile.mkdtemp()

    os.makedirs(data_dir, exist_ok=True)

    with zipfile.ZipFile("data.zip", "r") as zip_ref:
        zip_ref.extractall(temp_dir)
    
    all_items = os.listdir(temp_dir) # Get all files/folders

    # Loop through them to find the one with numbers
    day_folder = None
    for item in all_items:
        if item.isdigit():
            day_folder = item
            break 

    day_path = os.path.join(temp_dir, day_folder) # Create the path

    for root, _, files in os.walk(day_path): # Tuple unpacking: root, _, files (underscore ignores directories list)
        for file in files:                     # os.walk(): Recursively traverses all subdirectories
            if file.endswith('.gz'): # Process each .gz file
                gz_path = os.path.join(root, file)
                json_filename = file[:-3]  
                output_path = os.path.join(data_dir, json_filename)

                with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:            
                    shutil.copyfileobj(gz_file, out_file)
    
    shutil.rmtree(temp_dir)