import logging
import os

def setup_logger(filename):
    # Create a custom logger
    logger = logging.getLogger('AdvancedLogger')
    logger.setLevel(logging.DEBUG)
    
    log_filename = f"{filename}.log"

    # Create handlers
    console_handler = logging.StreamHandler()  # Logs to console
    file_handler = logging.FileHandler(log_filename)  # Logs to file

    # Set levels for handlers
    console_handler.setLevel(logging.WARNING)
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger