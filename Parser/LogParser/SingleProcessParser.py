import re
import os
import time
import sys
from LogParser import logDataStructure
from LogParser import regexTemp
from FilePathParser import FileUtility 
from xlsxReport import reportGenerator
import logging
from xlsxwriter.workbook import Workbook
from LogParser.regexTemp import regex_pex

from LogParser import parseFactoryInfo 
from LogParser.parseBGLoggerInfo import parseBGLoggerInfo

from LogParser.parseTestInfo import parseTestInfo
from LogParser.logFindRValure import parseRInfo

from LogParser.parseDiagTimeInfo import parseModsStartTimeInfo

from multiprocessing import  Pool,Process, Lock
import multiprocessing
from LogParser.logParser import logFileParser

from queue import  Queue

que=Queue()
if __name__=="__main__":
    
    #dir=None
    dirName=None
    if len(sys.argv)>1:
        dirName=sys.argv[1]
    if not dirName:
        dirName=os.getcwd()#if len(sys.argv)<=1 else dir=sys.argv[1]  
    #logging.debug("Openning Directory %s"%dirName)
    reportName="" if len(sys.argv)<=1 else sys.argv[2]
    reportName="Test_"
    dirName="/home/tesla_pde/Desktop/Geforece Log"
    fileList=FileUtility.workThroughDir(dirName,".log")
    resultList=[]
    #/mnt/storageDisk1/PG503/FAIL/7_to_10/
    ####################define the logging and print them to logs
    logging.basicConfig(level=logging.DEBUG,
                format='%(process) -12s%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='reportGenerate.log',
                filemode='w')
    #logging.basicConfig(filename='K80Download.log',filemode='w',level=logging.DEBUG)
    
    #############defube console and put the log level above debug to screen###############
    console = logging.StreamHandler()  
    console.setLevel(logging.DEBUG)  
    formatter = logging.Formatter('%(name)-12s : %(levelname)-8s %(filename) -12s%(process)s[line:%(lineno)d] %(message)s')  
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console) 
    count=0
    resultList=[]
    logging.debug("Openning Directory %s"%dirName)
    total=len(fileList)
    totalSize=0         
    parseSize=0
    startTime=time.time()

    for eachfile in fileList:
        totalSize=totalSize+os.path.getsize(eachfile)/(1024*1024)
        
    for eachLog in fileList:
        count+=1
        parseSize=os.path.getsize(eachLog)/(1024*1024)+parseSize
        currentTime=time.time()
        if not (
            "eft" in eachLog \
            or "fct" in eachLog \
            or "bat" in eachLog \
            or "bit" in eachLog \
            or "fpt" in eachLog \
            or "heatsink" in eachLog \
            or "lanerepair" in eachLog \
            or "sbt" in eachLog 
            or "310.log" in eachLog
            or "249.log" in eachLog
            or "hsa_r.log" in eachLog
            or "log" in eachLog 
            or "blacklist_check" in eachLog
           ):
            pass

        logging.debug("start process log %s finished,count %d,totally %d"%(eachLog,count,total))
        logging.debug("parsed %.2f MB  finished,totally %.2f MB"%(round(parseSize,2),totalSize))
        parser=logFileParser(eachLog)
        parser.logAnalysis()
        resultList.append(parser)

        logging.debug("%.3f min for this log,already run for %.3f min, need %.3f min for this analysis"%((time.time()-currentTime)/60,(currentTime-startTime)/60,(currentTime-startTime)/60*totalSize/parseSize))
    report=reportGenerator.reportGenerate(reportName+"loginfo.xlsx",resultList)
    #report.writeLoninfo("sheet1")
    report.failureAnalysis("sheet1")
    report.failureByECID("HBMfailureByECID")
    #report.writeHistogram("test")
    report.ttoAnalysis(False)
    report.closeWorkbook()