from collections import Counter
from threading import Thread, Lock 
import time
import cv2
import os
import csv
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import webcolors as wc

dir_path = 'D:\Coding\SE2\DEDS\DEDS-Week-9\Images'

csv_file = 'ColorAnalysis.csv'
header = ['Image Name', 'Result']
results = []
lock = Lock()

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
    clf = KMeans(n_clusters = 3, n_init='auto',copy_x=True, algorithm='elkan')
    color_labels = clf.fit_predict(img)
    center_colors = clf.cluster_centers_
    counts = Counter(color_labels)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    ColorNames = []
    ColorHex = []
    for i in counts.keys():
        r,g,b = int(ordered_colors[i][0]),int(ordered_colors[i][1]),int(ordered_colors[i][2])
        ColorNames.append(GetClosestColour((r,g,b)))
        ColorHex.append(wc.conversion.rgb_to_hex((r,g,b)))
    
    return [ColorNames,ColorHex]

def PrepImage(img):
    modifiedImage = img.reshape(img.shape[0]*img.shape[1], 3)
    return modifiedImage


def FindImages(path):
    images = []
    for file_name in os.listdir(path):
    # Check if the file is an image
        if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
            # Load the image
            image = cv2.imread(os.path.join(dir_path, file_name))
            images.append(image)
    return images
            
        
        




class MyThread(Thread):
    images = []
    
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        threadName = self.name
        while len(images) > 0:
            
            lock.acquire()
            image = images.pop()
            lock.release()
            print(ColorAnalysis(PrepImage(image)))


def create_threads():
    startTime = time.time()
    for i in range(2): #int(len(images)/250)
        name = "Thread #%s" % (i)
        my_thread = MyThread(name)
        my_thread.start()
    my_thread.join() 
    time.sleep(5)
    print("Time elapsed:", time.time() - startTime, "seconds")

if __name__ == "__main__":
    images = FindImages(dir_path)
    create_threads()