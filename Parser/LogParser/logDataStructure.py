import os
import re

class UniqueInfo():
    def __init__(self):
        self.uniqueData={}
class dataForEachStation():
    def __init__(self,station): 
        self.station=station

        self.subStationInfo={
                             
                             }
class dataStructure():
    
    def __init__(self):
        self.UniqueInfo=UniqueInfo()
    def addExtenStation(self,station):
        self.stationData[station]=dataForEachStation(station)

    