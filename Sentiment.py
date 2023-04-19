import time
import pandas as pd
from textblob import TextBlob
from textblob_nl import PatternTagger, PatternAnalyzer
import csv


    
    
def PreformAnalysis(text):
    blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    score = blob.sentiment[0] #textblob-nl maintainer forgot to structure the return correctly so get the polarity by hand
    
    if score > 0:
        score_label = "positief"
    elif score == 0:
        score_label = "neutraal"
    else:
        score_label = "negatief"
    
    return [score_label, score, str(text).encode("charmap", errors="replace").decode("charmap")]


def start():
    data = pd.read_csv("data.csv", skiprows=1)

    results = []

    for index, row in data.iterrows():
        
        text = ",".join(row[2:].values.tolist())[0:]
        results.append(([row[0]]+PreformAnalysis(text)))
        
    
    with open("resultaten.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sku", "score"])
        writer.writerows(results)
        
starttime = time.time()

start()
    
print(time.time()- starttime)