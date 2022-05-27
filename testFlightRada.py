from  FlightRadar24.api import FlightRadar24API

#IMPORT PLOTTING LIBRARIES
import logging
import threading
import time
import csv
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import numpy as np

import sqlManager as sqlM

#FUNCTION TO CONVERT GCS WGS84 TO WEB MERCATOR
#POINT

def convertToDataSource(flight):
    data = {'id': flight.id,
        'altitude': flight.altitude}
    return data
def wgs84_web_mercator_point(lon,lat):
    k = 6378137
    x= lon * (k * np.pi/180.0)
    y= np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return x,y

#DATA FRAME
def wgs84_to_web_mercator(df, lon="long", lat="lat"):
    k = 6378137
    df.x = df.longitude * (k * np.pi/180.0)
    df.y = np.log(np.tan((90 + df.latitude) * np.pi/360.0)) * k
    return df

def convertFlightsToDataSource(flights):

    lons = []
    lats = []
    trend=[]
    for airf in flights:
        df = wgs84_web_mercator_point(airf.longitude,airf.longitude)
        lons.append(xy_min[0])
        lats.append(xy_min[1])
        trend.append(airf.altitude)

    data=dict(    x=list(lons),    y=list(lats),    trend=trend)
    return data

def extractLatLon(flights):    
    lons = []
    lats = []
    labels = []
    
    for airf in flights:
        lons.append(airf.longitude)
        lats.append(airf.latitude)
        labels.append(airf.aircraft_code)
    
    return lons, lats,labels

#######################################
## MAIN
#######################################
ddbb = sqlM.sqlliteManager(r"airFlight.db")
ddbb.createTables()

fr_api = FlightRadar24API()

zones = fr_api.get_zones()

zoneS = "southamerica"
zone = fr_api.get_zones()[zoneS]
boundsZ = fr_api.get_bounds(zone)


for i in range(1,100):
    flights = fr_api.get_flights(bounds = boundsZ)

    ddbb.insertFlightsIntoTable(flights)
    print(' new query ... ')
    for airf in flights:
      ##  print(airf)  
        accumRow =[airf.longitude,airf.latitude,airf.aircraft_code]  
        with open('flights.csv', mode='a') as multi_file:
            multi_writer = csv.writer(multi_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            multi_writer.writerow(accumRow)
    for j in range(1,150):
        print('.', end='')
        time.sleep(3)

#end for

x,y,s = extractLatLon(flights)

fig, ax = plt.subplots()
ax.scatter(x, y)

for i, txt in enumerate(s):
    ax.annotate(txt, (x[i], y[i]))

plt.show()

    
input()