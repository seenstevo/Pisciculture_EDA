import pandas as pd
import os

import functions_file_preparation as ffprep
import variables

# create and move to directory for raw files that will be merged. 
os.chdir(os.path.dirname(__file__))
os.chdir('../data/')

# download data
url = 'https://www.fao.org/fishery/static/Data/Aquaculture_2022.1.1.zip'
ffprep.write_from_url(url, 'Aquaculture_2022.1.1.zip')

# extract and cleanup
ffprep.unzip_and_cleanup('Aquaculture_2022.1.1.zip', 'Aquaculture_Raw')


# load in both the quantity (mass) of fish raised with the value in USD
fish_quantity = pd.read_csv("./Aquaculture_Raw/Aquaculture_Quantity.csv")
#fish_value = pd.read_csv("./Aquaculture_Raw/Aquaculture_Value.csv")


# merge these two 
# fish_quant_value = pd.merge(fish_quantity, fish_value, how = 'outer',
#                             on = ['PERIOD', 'COUNTRY.UN_CODE', 'SPECIES.ALPHA_3_CODE', 'AREA.CODE', 'ENVIRONMENT.ALPHA_2_CODE'])

# rename columns
# fish_quant_value.rename(columns = {'VALUE_x': 'Quantity', 'VALUE_y': 'ValueUSD'}, inplace = True)
fish_quantity.rename(columns = {'VALUE': 'Quantity'}, inplace = True)

# replace the NaN (which are created due to blank values) with "OFF" for OFFICIAL
# fish_quant_value['STATUS_x'].fillna("OFF", inplace = True)
# fish_quant_value['STATUS_y'].fillna("OFF", inplace = True)
fish_quantity['STATUS'].fillna("OFF", inplace = True)
                                    
                                    
# use function to merge codelist files                                  
fish_quantity = ffprep.merge_codelist_files(fish_quantity, "./Aquaculture_Raw/CL_FI_COUNTRY_GROUPS.csv", 
                                        ["UN_Code", "Name_En"], "COUNTRY.UN_CODE", "Country")

fish_quantity = ffprep.merge_codelist_files(fish_quantity, "./Aquaculture_Raw/CL_FI_WATERAREA_GROUPS.csv", 
                                        ["Code", "Name_En"], "AREA.CODE", "WaterArea")

fish_quantity = ffprep.merge_codelist_files(fish_quantity, "./Aquaculture_Raw/CL_FI_PRODENVIRONMENT.csv", 
                                        ["Code", "Name_En"], "ENVIRONMENT.ALPHA_2_CODE", "Environment")

fish_quantity = ffprep.merge_codelist_files(fish_quantity, "./Aquaculture_Raw/CL_FI_SPECIES_GROUPS.csv", 
                                        ["3A_Code", "Name_En", "Scientific_Name"], "SPECIES.ALPHA_3_CODE", "Species")

fish_quantity = ffprep.merge_codelist_files(fish_quantity, "./Aquaculture_Raw/FSJ_UNIT.csv", ["Code", "Name_En"], 
                                        "MEASURE", "Measure_Unit_Quantity")

# fish_quantity = ffprep.merge_codelist_files(fish_quantity, "./Aquaculture_Raw/FSJ_UNIT.csv", ["Code", "Name_En"], 
#                                         "MEASURE_y", "Measure_Unit_ValueUSD")

fish_quantity = ffprep.merge_codelist_files(fish_quantity, "./Aquaculture_Raw/CL_FI_SYMBOL.csv", ["Symbol", "Name_En"], 
                                        "STATUS", "Statistical_Symbol_Quantity")

# fish_quantity = ffprep.merge_codelist_files(fish_quantity, "./Aquaculture_Raw/CL_FI_SYMBOL.csv", ["Symbol", "Name_En"], 
#                                         "STATUS_y", "Statistical_Symbol_ValueUSD")


# split the data into animal and non-animal
non_fish_quantity, fish_quantity = ffprep.split_plant_animal(fish_quantity, variables.plant_list)


#write final merged dataframe to file
fish_quantity.to_csv("Aquaculture_Quantity_Code_Merged.csv", index = False)
non_fish_quantity.to_csv("Aquaculture_Non_Fish_Quantity_Code_Merged.csv", index = False)