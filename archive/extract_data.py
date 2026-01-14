## Script to extract amplitude extract data using API call
## Documentation here https://amplitude.com/docs/apis/analytics/export

## Import libraries

import requests 
import os 
from datetime import datetime
import time  
import logging 
from dotenv import load_dotenv
from datetime import timedelta

## Build the request

# Get credentials
load_dotenv()

app_key = os.getenv("AMP_API_KEY")
app_secret_key = os.getenv("AMP_SECRET_KEY")

# Get time frames
yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')

url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start_time,
    'end': end_time
}

# Make the GET request with basic authentication
response = requests.get(url, params=params, auth=(app_key, app_secret_key), timeout=60)

## Loggings

logs_folder = 'logs'
if os.path.exists(logs_folder):
     pass
else:
    os.mkdir(logs_folder)

filename = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # use timestamp to name files

log_filename = f"logs/{filename}.log" # put logs into logs folder

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

## Add the following to your script when you want logging to occur:
# logger.debug("This is a debug message")    
# logger.info("System working")            
# logger.warning("Something unexpected")        
# logger.error("An error occurred")             
# logger.critical("Critical system error")

## Check errors

no_of_tries = 3
count = 0

while count <= no_of_tries:

    response_code = response.status_code
    
    if response.status_code == 200:
        # The request was successful
        data = response.content ## catches any type of data
        print('Data retrieved successfully.')
        logger.info("Data retrieved successfully.") 
        # JSON data files saved to a zip folder 'data.zip'
        with open('data.zip', 'wb') as file: # ensures the file closes after this operaion even when errors occur
            file.write(data)
        break 

    elif response_code > 499 or response_code < 200:
        print(response.reason)
        logger.warning("Something unexpected")  
        time.sleep(10) # wait 10 secs before trying again
        count +=1

    else: 
        print(response.reason)
        logger.error("An error occurred")  
        break 