import pandas as pd
import os

import functions_file_preparation as ffprep
import variables

# create and move to directory for raw files that will be merged. 
os.chdir(os.path.dirname(__file__))
os.chdir('../data/')

# download data
url = 'https://www.fao.org/fishery/static/Data/Capture_2022.1.1.zip'
ffprep.write_from_url(url, 'Capture_2022.1.1.zip')

# extract and cleanup
ffprep.unzip_and_cleanup('Capture_2022.1.1.zip', 'Capture_Data_Raw')


# load in the quantity (mass) of fish captured
fish_capture_quantity = pd.read_csv("./Capture_Data_Raw/Capture_Quantity.csv")

# rename columns
fish_capture_quantity.rename(columns = {'VALUE': 'Quantity'}, inplace = True)

# replace the NaN (which are created due to blank values) with "OFF" for OFFICIAL
fish_capture_quantity['STATUS'].fillna("OFF", inplace = True)

# use function to merge codelist files
fish_capture_quantity = ffprep.merge_codelist_files(fish_capture_quantity, "./Capture_Data_Raw/CL_FI_SPECIES_GROUPS.csv", 
                                        ["3A_Code", "Name_En", "Scientific_Name"], "SPECIES.ALPHA_3_CODE", "Species")

fish_capture_quantity = ffprep.merge_codelist_files(fish_capture_quantity, "./Capture_Data_Raw/CL_FI_COUNTRY_GROUPS.csv", 
                                        ["UN_Code", "Name_En"], "COUNTRY.UN_CODE", "Country")

fish_capture_quantity = ffprep.merge_codelist_files(fish_capture_quantity, "./Capture_Data_Raw/CL_FI_WATERAREA_GROUPS.csv", 
                                        ["Code", "Name_En"], "AREA.CODE", "WaterArea")

fish_capture_quantity = ffprep.merge_codelist_files(fish_capture_quantity, "./Capture_Data_Raw/FSJ_UNIT.csv", ["Code", "Name_En"], 
                                        "MEASURE", "Measure_Unit_Quantity")

fish_capture_quantity = ffprep.merge_codelist_files(fish_capture_quantity, "./Capture_Data_Raw/CL_FI_SYMBOL.csv", ["Symbol", "Name_En"], 
                                        "STATUS", "Statistical_Symbol_Quantity")


# split the data into animal and non-animal
non_fish_capture_quantity, fish_capture_quantity = ffprep.split_plant_animal(fish_capture_quantity, variables.plant_list)

#write final merged dataframe to file
fish_capture_quantity.to_csv("Capture_Quantity_Code_Merged.csv", index = False)
non_fish_capture_quantity.to_csv("Capture_Non_Fish_Quantity_Code_Merged.csv", index = False)