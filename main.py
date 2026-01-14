from datetime import datetime, timedelta
from modules.logging_func import loggin_function
from modules.extract_func import extract_func
from modules.load_func import load_func
from modules.unzip_func import unzip_func
import os 
from dotenv import load_dotenv

load_dotenv() 

app_key = os.getenv("AMP_API_KEY")
app_secret_key = os.getenv("AMP_SECRET_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
bucket_name = os.getenv("bucket_name")

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')

url = 'https://analytics.eu.amplitude.com/api/2/export'

data_dir = "data"

## Functions

# Extract logs
extract_logger = loggin_function('extract', timestamp)

# Extracting data
extract_func(url, 3, app_key, app_secret_key, start_time, end_time, extract_logger)

# Unzipping and decompresseing files
unzip_func(data_dir)

# Load logs
load_logger = loggin_function('load', timestamp)

# Loading data into S3
load_func(AWS_ACCESS_KEY, AWS_SECRET_KEY, bucket_name, data_dir, timestamp, load_logger)