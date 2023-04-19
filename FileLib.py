from csv import writer
import os
import json
import pyodbc
import sqlite3



def WriteDataToJSON(outfile, data):
    EnsureFileExists(outfile)
    with open(outfile, 'w', encoding="utf8", newline="") as out:
        json.dump(data, out) 
        
def WriteDataToCSV(outfile, data):
    EnsureFileExists(outfile)
    with open(outfile, 'w', encoding="utf8", newline="") as out:
        write = writer(out)
        write.writerows(data)
        
        
def EnsureFileExists(outfile):
    directory = os.path.dirname(outfile)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(outfile):
        open(outfile, 'w').close()
    
    
    
    
    
# def WriteDictToSQLite(DBFile, dicts):
#     conn = sqlite3.connect(DBFile)
#     table_name = "DEDS_DATA"
#     keys = dicts[0].keys()
#     query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(keys)})"
#     conn.execute(query)

#     for item in dicts:
#         values = []
#         for value in item.values():
            
#             # Convert boolean values to integer representation
#             if isinstance(value, bool):
#                 value = int(value)
#             values.append(value)
#         placeholders = ', '.join(['?'] * len(values))
#         columns = ', '.join(item.keys())
#         query = f"INSERT INTO {table_name} ({columns}) VALUES (?,?)"
#         conn.execute(query, values)

#     conn.commit()
#     # Close the database connection
#     conn.close()
    

# def WriteDictToAcces(db_file,dicts):
#     conn_str = (r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+db_file+';')
#     with pyodbc.connect(conn_str) as conn:
#         cursor = conn.cursor()

#         keys = set()
        
#         tableName = "dict_table"
        
#         for dictionary in dicts:
#             keys.update(dictionary.keys())
#         columns = ', '.join(keys)
#         cursor.execute(f"CREATE TABLE {tableName} [{columns}]")

#         for dictionary in dicts:
#             values = tuple(dictionary.get(key, '') for key in keys)
#             placeholders = ', '.join('?' * len(keys))
#             cursor.execute(f"INSERT INTO {tableName} [{columns}] VALUES [{placeholders}]", values)
#         conn.commit()