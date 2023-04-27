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


def start():
    data = pd.read_csv(inputpath, skiprows=1)
    results = []

    with open(inputpath, "r",encoding="utf-8") as file:
        for line in file:
            
            skunr, text = line.strip().split(",", 1)
            
            analysis = PreformAnalysis(text.replace("\"",""))
            results.append(dict(sku = skunr, sentiment = analysis[0], text = analysis[1]))
    
    
    FileLib.EnsureFileExists(outputpath)
    FileLib.saveDictToJSON(outputpath+"Sentiment.json", results)
    FileLib.saveDictToCSV(outputpath+"Sentiment.csv", results)
    for line in results:
        FileLib.saveDictToSQLITE(dbpath,"Analysis_Sentiment",line)


        
starttime = time.time()
start()
print(time.time()- starttime)