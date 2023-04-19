import os
import time
import pandas as pd
from textblob import TextBlob
from textblob_nl import PatternTagger, PatternAnalyzer
import csv
import FileLib

outputpath = os.path.dirname(__file__)+'/output/Sentiment/'
    
    
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
    data = pd.read_csv(os.path.dirname(__file__)+"/data.csv", skiprows=1)

    results = []

    for index, row in data.iterrows():
        
        text = ". ".join(row[2:].values.tolist())[0:]
        results.append(dict(sku = row[0], sentiment = PreformAnalysis(text)))
    FileLib.WriteDataToJSON(outputpath+"Sentiment.json", results)
    FileLib.WriteDictToSQLite("D:\Coding\SE2\DEDS\DEDS-DataStrait\die.sqlite",results)
        
starttime = time.time()

start()
    
print(time.time()- starttime)