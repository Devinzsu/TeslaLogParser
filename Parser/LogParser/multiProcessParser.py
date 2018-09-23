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
from queue import  Queue

from LogParser.logParser import processLogs,logFileParser
import LogParser
#import codes
#from codes import unicode

def allocResouce(fileList,start,processors,totalSize):
    
    end=start
    size=0
    eachSize=totalSize/processors
    #print("eachSize %d"%(eachSize))
    
    for index in range(start,len(fileList)):
        size+=os.path.getsize(fileList[index])/(1024*1024)
        #print("size %d"%(size))
        end=index
        if size>eachSize:
            break
    return end+1
    
    
    
        
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
    reportName="PG503_2018_FAIL_"
    dirName="/home/tesla_pde/logfiles/2018/logfiles/FAIL/08/G503"
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
    total=len(fileList)
    totalSize=0
    for index in range(len(fileList)):
        totalSize+=os.path.getsize(fileList[index])/(1024*1024)
    
    parseSize=0
    startTime=time.time()
    
    processor=multiprocessing.cpu_count() 
    
    pool = Pool(processes = processor)
    #p = Pool(processor)\
    resList=[]
    
    lock=Lock()
    
    start=0
    end=0
    #print("total %d"%(len(fileList)))
    for i in range(processor):
        start=0 if i==0 else end
        
        end=allocResouce(fileList, start, processor, totalSize)
        argus=[]
        argus=[fileList[start:end],que]
        p = pool.apply_async(processLogs, (fileList[start:end],))
        #p.wait(999999999)
        #print(end)
        #os.system("sleep 1")
        resList.append(p)
        if end==total-1:
            break
          
    
    pool.close()
    pool.join()
    logging.info("done")
    for eachProcess in resList:
        result=eachProcess.get()
        #logging.info(eachProcess.get())
        for each in result:
            resultList.append(each)
    #print(resultList)
    
    report=reportGenerator.reportGenerate(reportName+"loginfo.xlsx",resultList)
    logging.info(reportName)
    #report.writeLoninfo("sheet1")
    report.failureAnalysis("sheet1")
    logging.info("sheet1")
    
    report.failureByECID("HBMfailureByECID")
    #report.writeHistogram("test")
    report.ttoAnalysis(False)
    report.closeWorkbook()
    
       
            
        
        
    
    
    
    
        
        