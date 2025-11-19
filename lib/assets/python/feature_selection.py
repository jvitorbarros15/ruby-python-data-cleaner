import pandas as pd 
import os 
import json

# Load configuration from a JSON file given by data controller
def load_config(config_path):
  with open(config_path, "r", encoding="utf8") as f:
    return json.load(f)
  
def remove_duplicates(df):
  return df.drop_duplicates()
