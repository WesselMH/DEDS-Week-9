import json
import os
import sqlite3
import time
import pandas as pd
from textblob import TextBlob
from textblob_nl import PatternTagger, PatternAnalyzer
from csv import DictWriter
import FileLib

inputpath = os.path.dirname(__file__)+"/input/data.txt"
outputpath = os.path.dirname(__file__)+'/output/Sentiment/'
dbpath = outputpath+"sentiment.sqlite"
    
def PreformAnalysis(text):
    blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    score = blob.sentiment[0] #textblob-nl maintainer forgot to structure the return correctly so get the polarity by hand
    
    if score > 0:
        score_label = "positief"
    elif score == 0:
        score_label = "neutraal"
    else:
        score_label = "negatief"
    
    return [score_label,  str(text).encode("charmap", errors="replace").decode("charmap")]


def saveDictToSQLITE(database, table, data):
    # connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # create the table if it doesn't exist
    column_names = ", ".join(data.keys())
    c.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, {column_names})")

    # insert the data into the table
    placeholders = ", ".join("?" * len(data))
    values = tuple(data.values())
    c.execute(f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})", values)

    # commit the changes and close the connection
    conn.commit()
    conn.close()

def saveDictToJSON(output, data):
    with open(output, 'w', encoding="utf8", newline="") as out:
        json.dump(data, out, ensure_ascii=False)  
    
def saveDictToCSV(output, data):
    with open(output, 'w', encoding="utf8", newline="") as out:
        write = DictWriter(out, fieldnames=data[0].keys())
        write.writeheader()
        for entry in data:
            write.writerow(entry)





def start():
    data = pd.read_csv(inputpath, skiprows=1)

    results = []

    with open(inputpath, "r",encoding="utf-8") as file:
        for line in file:
            
            skunr, text = line.strip().split(",", 1)
            
            analysis = PreformAnalysis(text.replace("\"",""))
            results.append(dict(sku = skunr, sentiment = analysis[0], text = analysis[1]))
    
    saveDictToJSON(outputpath+"Sentiment.json", results)
    saveDictToCSV(outputpath+"Sentiment.csv", results)

    for line in results:
        saveDictToSQLITE(dbpath,"Sentiment",line)



       
       
       
       
        
starttime = time.time()
start()
print(time.time()- starttime)