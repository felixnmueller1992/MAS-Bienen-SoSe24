import pandas as pd
import time 

export_file_name = time.strftime("%Y%m%d_%H%M%S_Exportfile.csv")

def export_szenario(environment_data):   
    df_export = pd.DataFrame(environment_data).T    
    df_export.to_csv(export_file_name, mode='a',header=False, index=False)


            
    
    

    

    
