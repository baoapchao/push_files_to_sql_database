from main import *
from config import *

df = pd.read_excel(r'input_import.xlsx', sheet_name= 'list_folders_to_import_db')
list_folders_to_import_db = df.to_dict('records')

df = pd.read_excel(r'input_import.xlsx', sheet_name= 'list_files_to_import_db')
list_files_to_import_db = df.to_dict('records')

combine_and_import_folder_to_sql(c_string, list_folders_to_import_db)

