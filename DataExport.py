import pandas as pd

from Config import *
from Bee import *

def daten_exportieren(hive_group, bee_group, total_food_amount):
    # Sammle generelle Daten für Legende und Dateiexport
    timetag = str(round((pygame.time.get_ticks() / 1000),1))
    gathered_food = sum([hive.food_count for hive in hive_group])
    general_data = {
        "timetag [s]": [timetag], 
        "gathered_food": [gathered_food], 
        "total_food_amount": [total_food_amount]
    }
    telemetry_df_temp = pd.DataFrame(general_data)

    # Sammle Bienendaten für Legende und Dateiexport
    total_scouts, total_employed, total_onlooker, total_returner, total_dancer = 0,0,0,0,0     
    for id,bee in enumerate(bee_group):
        id += 1
        match bee.occupation: 
            case Occupation.SCOUT:
                total_scouts += 1
            case Occupation.EMPLOYED:
                total_employed += 1
            case Occupation.ONLOOKER:
                total_onlooker += 1
            case Occupation.DANCER:
                total_dancer += 1
        if EXPORT_COMPLETE_BEE_GROUP == True:
            bee_data_temp = {
                "bee_"+str(id)+"_occupation": [str(bee.occupation).split('.')[1]],
                "bee_"+str(id)+"_capacity": [bee.capacity],
                "bee_"+str(id)+"_success": [bee.success]
            }                                                       
            telemetry_df_temp = pd.concat([telemetry_df_temp,pd.DataFrame(bee_data_temp)],axis=1)          
    bee_population_data = {
            "total_scouts": [total_scouts],
            "total_employed": [total_employed],
            "total_onlooker": [total_onlooker],
            "total_dancer": [total_dancer]
    }
    telemetry_df_temp = pd.concat([telemetry_df_temp,pd.DataFrame(bee_population_data)],axis=1)

    return telemetry_df_temp
