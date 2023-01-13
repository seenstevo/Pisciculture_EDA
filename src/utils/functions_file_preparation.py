import pandas as pd
import requests
import zipfile
import os
from typing import List, Set, Dict, Tuple


def merge_codelist_files(fish_quant_value, codelist_file_path: str, columns_to_use: list, left_on: str, rename: str):
    '''
    Take one of the codelist files and merge it with the main dataset
    '''
    codelist_file = pd.read_csv(codelist_file_path, usecols = columns_to_use)
    if 'Symbol' in codelist_file.columns:
        codelist_file.loc[0, 'Symbol'] = "OFF"
    return pd.merge(fish_quant_value, codelist_file, left_on = left_on, right_on = columns_to_use[0]).\
        drop([left_on, columns_to_use[0]], axis = 1).\
            rename(columns = {"Name_En": rename})
            
            
def write_from_url(url: str, file_name: str) -> None:
    r = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.content)
        
    
def unzip_and_cleanup(zip_file_name: str, out_folder: str) -> None:
    with zipfile.ZipFile(zip_file_name) as zip_ref:
        zip_ref.extractall(out_folder)
    os.remove(zip_file_name)
    
    
def split_plant_animal(df: pd.DataFrame, plants_list: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    plant = df[df['Species'].isin(plants_list)]
    animal = df[~df['Species'].isin(plants_list)]
    return (plant, animal)