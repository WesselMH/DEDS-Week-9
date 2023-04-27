Scrapers = ./Scrapers/Scrapers
BeverOutput = $(Scrapers)/Bever/output
BolOutput = $(Scrapers)/Bol/output
Hadoop = ./Hadoop
Analysis = ./Analysis
AnalysisInput = $(Analysis)/input

all:
	py $(Scrapers)/Bever/BeverBot.py
	powershell cp $(BeverOutput)/* $(AnalysisInput)/ -Recurse -Force
	py $(Analysis)/Sentiment.py
	py $(Analysis)/ColorAnalysisThief.py