import pandas as pd
import time 

def export_szenario(environment_data,file_date):   
    df_export = pd.DataFrame(environment_data).T    
    df_export.to_csv(file_date + "_Szenario.csv", mode='a',header=False, index=False)


            
    
    

    

    
