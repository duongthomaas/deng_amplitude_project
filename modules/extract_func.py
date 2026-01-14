import requests 
import time  

def extract_func(url, no_of_tries, app_key, app_secret_key, start_time, end_time, logger):
    
    params = {
    'start': start_time,
    'end': end_time
    }
    
    response = requests.get(url, params=params, auth=(app_key, app_secret_key), timeout=60)

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