# commom functionalities are written here which can then be used in all other files
import numpy as np
import os 
import pandas as pd 
# dill helps in creating pickle files
import dill
from src.exception import CustomException
from src.logger import logging 
import sys 

def save_object(filepath, obj):
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True) 
        with open(filepath, 'wb') as obj:
            dill.dump(obj,obj) 

    except Exception as e:
        raise CustomException(e,sys)
