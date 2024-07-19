import pandas as pd

from Config import *


def interpolate(x, lowest, highest, min_value=0, max_value=1):
    return min_value + (max_value - min_value) * (x - lowest) / (highest - lowest)

def collect_config_data():
    
    config_df = pd.read_table("Config.py", header=None)
    return config_df