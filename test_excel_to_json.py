import json
import pandas as pd

df = pd.read_excel(r'input_import.xlsx', sheet_name= 'list_folders_to_import_db')

dict1 = df.to_dict('records')

print(dict1)
