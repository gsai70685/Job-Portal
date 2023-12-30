"""
This file we have the functionalities that can be used by
all the other code files
"""

import os
import logging

logger_obj = logging.getLogger("jobslogger")

filehandler = logging.FileHandler("file.log")
filehandler.setLevel(logging.WARNING)
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                datefmt='%d-%b-%y %H:%M:%S')
filehandler.setFormatter(file_format)
logger_obj.addHandler(filehandler)



