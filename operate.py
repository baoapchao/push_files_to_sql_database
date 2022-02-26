from main import *
# import json
from config import *

# with open('local-sql-connection-string.json', 'r') as f:
#     data = json.load(f)
#     connstr = data['c_string']

df = pd.read_excel(r'input_import.xlsx', sheet_name= 'list_folders_to_import_db')
list_folders_to_import_db = df.to_dict('records')

df = pd.read_excel(r'input_import.xlsx', sheet_name= 'list_files_to_import_db')
list_files_to_import_db = df.to_dict('records')
# import_folder_to_sql(connstr, r'C:\Users\ADMIN\Documents\Code')

import_files_to_sql(c_string, r'C:\Users\ADMIN\OneDrive\__Study\Python\SQLAlchemy\Danh sách văn bản chỉ đạo UBND Quảng Ninh.csv')

