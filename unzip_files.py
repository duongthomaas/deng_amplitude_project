## Unzip the data.zip file, consolidating all the raw JSON files into a single directory. This will prepare them for upload to our cloud storage solution, AWS S3 Bucket.

## Get libraries

import zipfile ## Handles ZIP archive files
import gzip ## Handles GZIP compressed files
import os 
import shutil
import tempfile 

## Unzip!

## Unzip 1

# Create a temporary directory for extraction
temp_dir = tempfile.mkdtemp()

# Create local output directory
data_dir = "data"
os.makedirs(data_dir, exist_ok=True) # make the folder but don't crash if already exists

# Unzip the first zip - revealing several .gz (gzip) files

with zipfile.ZipFile("data.zip", "r") as zip_ref:
    zip_ref.extractall(temp_dir)


## Grey area where not 100% sure

# Locate target folder
# Not really getting this bit:
# day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
# day_path = os.path.join(temp_dir, day_folder)

# A bit longer alternative but easier to read:

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
            print(file)

## Unzip 2 - Unzip the .gz files
# Second Level Extraction (GZ → Final Location)
# To unpack the .gz files to obtain the .json files we will need:
# the filepath of the .gz file
# the filename of the .gz file, and what it will be as .json
# the location of where to store it (data_dir)
# We will then read the contents of the .gz file and write the content to a new json file in our data_dir.

gz_path = os.path.join(root, file)
json_filename = file[:-3]  
output_path = os.path.join(data_dir, json_filename)

with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:            
    shutil.copyfileobj(gz_file, out_file)

# Notes:
# String slicing: file[:-3] removes last 3 characters (.gz)
# Binary file handling: 'rb' (read binary) and 'wb' (write binary)
# shutil.copyfileobj(): Efficient copying between file objects


# We delete the contents of the temporary directory so we remove the data still contained as .gz files.

shutil.rmtree(temp_dir)