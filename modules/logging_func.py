import logging 
import os 

def loggin_function(prefix, timestamp):
    
    dir = f"{prefix}_logs"
    os.makedirs(dir, exist_ok= True)

    log_filename = f"{dir}/{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_filename
    )

    return logging.getLogger()