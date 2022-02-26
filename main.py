import os

from sqlalchemy import create_engine
from sqlalchemy.types import BIGINT, NVARCHAR, DATETIME, DECIMAL, BOOLEAN, NUMERIC
from sqlalchemy.schema import CreateSchema

import pandas as pd
import numpy as np

#Define function to get column datatypes
def get_column_dtype(df):
    columntype_dict = {}

    #Get sql server datatype of each column
    for column in df:
        type = df[column].dtype
        sql_type = ''

        #Check if column is text
        if np.issubdtype(type,object):
            
            #Check text length
            max_len = df[column].astype(str).str.len().max()
            
            if max_len <= 50:
                sql_type = NVARCHAR(50)
            elif max_len <= 255:
                sql_type = NVARCHAR(255)
            else:
                sql_type = NVARCHAR

        #Check if column is int
        elif np.issubdtype(type,np.int64):
            sql_type = BIGINT

        #Check if column is decimal
        # elif np.issubdtype(type,float):
        #     sql_type= DECIMAL(12,2)
        # sql_type= NUMERIC(12,2)

        #Check if column is datetime
        elif np.issubdtype(type,np.datetime64):
            sql_type = DATETIME

        #Check if column is boolean    
        elif np.issubdtype(type,np.bool_):
            sql_type = NVARCHAR(10)

        else:
            sql_type = NVARCHAR
        #Append column and sql datatype to dict
        columntype_dict[column] = sql_type
        # columntype_dict[column] = NVARCHAR

    return columntype_dict

def import_table_to_sql(engine, df, table_name, schema):
    try:
        engine.execute(CreateSchema(schema))
        print(f"Created new schema: {schema}")
    except: pass
    try:
        type_dict = get_column_dtype(df)    
        df.to_sql(
                table_name, engine, schema= schema
                ,if_exists = 'replace' , index = False
                ,chunksize= 1000
                ,dtype = type_dict
            )
        print(f"Successfully import data into {schema}.{table_name}")
    except Exception as e:
        print(f'Error {e}')

def import_files_to_sql(connstr, filepath, table_name = '' , schema = ''):
    #csv or json or excel
    engine = create_engine(connstr, fast_executemany=True)
    filename, ext = os.path.splitext(os.path.basename(filepath))
    if table_name == '': 
        table_name = filename
    else:pass

    if schema == '':
        schema = ext
    else:pass

    if ext == '.csv':
        df = pd.read_csv(filepath)
        print('Reading CSV')
    elif ext == '.json':
        df = pd.read_json(filepath)
        print('Reading JSON')
    elif ext == '.xlsx' or ext == '.xls':
        df = pd.read_excel(filepath)
        print('Reading Excel')
    else:pass        

    import_table_to_sql(engine, df, table_name, schema)

def import_folder_to_sql(connstr, folder_path):
    engine = create_engine(connstr, fast_executemany=True)
    for file in os.listdir(folder_path):
        filepath = fr"{folder_path}\{file}"
        filename, ext = os.path.splitext(file)
        if ext == '.csv':
            df = pd.read_csv(filepath)
            print('Reading CSV')
        elif ext == '.json':
            df = pd.read_json(filepath)
            print('Reading JSON')
        elif ext == '.xlsx' or ext == '.xls':
            df = pd.read_excel(filepath)
            print('Reading Excel')
        else:pass
        try:
            if len(df) > 0:
                table_name = filename
                table_schema = ext.replace('.', '')
                import_table_to_sql(engine, df, table_name, table_schema)
            else: pass
        except Exception as e:
            print(f'Error {e}')
            

def combine_and_import_folder_to_sql(connstr, list_to_import_db:list):
    # sample_lst_to_db = [
    #     {'name' : 'historical_price' , 
    #     'directory' : r'C:\Users\ADMIN\OneDrive\__Study\Python\Data Collection\Scraping\Fireant\Historical Price' ,
    #     'schema' : 'stock'
    #     }
    #     ]
    engine = create_engine(connstr, fast_executemany=True)
    for table in list_to_import_db:
        df_combine = pd.DataFrame([])
        for dirpath, dirs, files in os.walk(table['directory']):
            if files != []:
                for file in files:
                    filepath = fr'{dirpath}\{file}'
                    try:
                        df_temp = pd.read_csv(filepath)
                        print('Reading CSV')
                    except:
                        pass
                    try:
                        df_temp = pd.read_json(filepath)
                        print('Reading JSON')
                    except:
                        pass
                    try:
                        df_temp = pd.read_excel(filepath)
                        print('Reading Excel')
                    except:
                        pass                    
                    df_combine = df_combine.append(df_temp)
        if len(df_combine) > 0:
            try:
                table_name = table['name']
                table_schema = table['schema']
                import_table_to_sql(engine, df_combine, table_name, table_schema)

            except Exception as e:
                print(f'Error {e}')

        else: pass


