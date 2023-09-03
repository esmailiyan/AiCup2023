import os
import logging

def log(data:str) -> bool:
    # Set the logging configuration
    log_file = '.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='- %(message)s')

    # Log some data
    logging.info(data)