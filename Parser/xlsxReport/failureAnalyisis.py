from xlsxwriter.workbook import Workbook
from LogParser.logDataStructure import dataForEachStation


from LogParser.DiagCompareUtility import compareCmdLine
from statistics import mean
import os
import re
import numpy
import statistics
import logging
from LogParser.utilityString import getDistribution
import datetime



class failureAnayslis():
    def __init__(self,loginfo):
        
        
        