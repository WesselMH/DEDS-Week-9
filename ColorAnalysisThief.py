from collections import Counter
from threading import Thread, Lock 
import time
import cv2
import os
import csv
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import webcolors as wc
from colorthief import ColorThief
import FileLib

imagePath = os.path.dirname(__file__)+'/input/Images/'
outputpath = os.path.dirname(__file__)+'/output/Color/'

csv_file = 'ColorAnalysis.csv'
header = ['Image Name', 'Result']
results = []

def GetClosestColour(requested_colour):
    min_colours = {}
    for key, name in wc.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = wc.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def ColorAnalysis(img):
    
    ColorNames = []
    ColorHex = []
    
    color_thief = ColorThief(img)
    palette = color_thief.get_palette(color_count=6)
    for i in palette:
        ColorHex.append(wc.conversion.rgb_to_hex(i))
        ColorNames.append(GetClosestColour(i))
    
    output = {}
    for i in range(len(ColorNames)):
        tempdict = {}
        tempdict["colorname"+str(i)] = ColorNames[i]
        tempdict["colorhex"+str(i)] = ColorHex[i]
        output.update(tempdict)
    return output


def FindImages(path):
    images = []
    for file_name in os.listdir(path):
        if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
            images.append(os.path.join(imagePath, file_name))
    return images


def start():
    imgs = FindImages(imagePath)
    results = []
    
    for i in imgs:
        analysis = ColorAnalysis(i)
        # print(analysis)
        output = dict(skunr = i.split("/")[-1].split(".")[0])
        output.update(analysis)
        print(output)
        results.append(output)
        
    FileLib.EnsureFileExists(outputpath)
    FileLib.saveDictToJSON(outputpath+"Color.json",results)
    FileLib.saveDictToCSV(outputpath+"Color.csv",results)
    for line in results:
        FileLib.saveDictToSQLITE(outputpath+"Color.sqlite","Analysis_Color",line)


    






starttime = time.time()        
start()
print("Time elapsed:", time.time() - starttime, "seconds")
