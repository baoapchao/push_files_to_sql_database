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

# define function to read json, excel, or csv:
def file_to_df(filepath):
    filename, ext = os.path.splitext(os.path.basename(filepath))
    df = ''
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
    return df    

def create_schema(engine, schema):
    try:
        engine.execute(CreateSchema(schema))
        print(f"Created new schema: {schema}")
    except: 
        print(f"Schema {schema} already existed.")   

def import_table_to_sql(engine, df, table_name, schema):
    create_schema(engine, schema)
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

def import_files_to_sql(c_string, file_list:list):
    engine = create_engine(c_string, fast_executemany=True)
    #csv or json or excel
    for filepath in file_list:
        filename, ext = os.path.splitext(os.path.basename(filepath))

        table_name = filename

        schema = ext.replace('.', '')

        df_import = ''
        df_import = file_to_df(filepath)

        import_table_to_sql(engine, df_import, table_name, schema)

def import_folders_to_sql(c_string, folder_list:list):
    engine = create_engine(c_string, fast_executemany=True)
    for folderpath in folder_list:
        for file in os.listdir(folderpath):
            filepath = os.path.join(folderpath, file)
            filename, ext = os.path.splitext(file)

            schema = ext.replace('.', '')

            df_import = ''

            try:
                df_import = file_to_df(filepath)
                if len(df_import) > 0:
                    table_name = filename
                    import_table_to_sql(engine, df_import, table_name, schema)
                else: pass
            except Exception as e:
                print(f'Error {e}')

        
def combine_and_import_folder_to_sql(c_string, folder_list:list):
    engine = create_engine(c_string, fast_executemany=True)
    for folderpath in folder_list:
        df_combine = pd.DataFrame([])
        for dirpath, dirs, files in os.walk(folderpath):
            if files != []:
                for file in files:
                    filepath = os.path.join(dirpath, file)

                    df = ''
                    df = file_to_df(filepath)

                    df_combine = df_combine.append(df)

                    filename, ext = os.path.splitext(file)
                    schema = ext.replace('.', '')

        if len(df_combine) > 0:
            try:
                table_name = os.path.basename(folderpath)
                table_schema = schema
                import_table_to_sql(engine, df_combine, table_name, table_schema)

            except Exception as e:
                print(f'Error {e}')

        else: pass


