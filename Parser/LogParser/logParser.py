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
import LogParser
#import codes
#from codes import unicode
class logFileParser:
    def __init__(self,path):
        self.filePath=path
        self.currentStation=None
        self.currentSubStation=None
        self.stationName=""
        self.uniqueData={}
        self.factoryInfo={}
        self.databyECID={}
        self.dataForeachSubstation={}
        self.logInfo={}
        self.testInfo={}
        self.rawTemp=[]
        self.gputemp=""
        self.hbmcmbtemp=""
        self.pexError={}
        
    def parserOfSingleLine(self,reCompile,line):
        
        ret=reCompile.search(line)
        data=ret.group("data") if ret is not None else None
        #print(data)
        return data
    def findPexLaneInfo(self,key,regexCompileList,line,searchType):
        '''
        regex is the complile regex, 
        searchType means 0 for only once,1 for multiple time
        '''
        if searchType==0 and key in self.dataForeachSubstation[self.currentSubStation]:
            '''the data is already stored in dataForeachSubstation'''
            return
        for eachRegex in regexCompileList:
            result=eachRegex.search(line)
            if result is not None:
                key="pexLane"+"$"+result.group("radias")
                self.dataForeachSubstation[self.currentSubStation][key]=result.group("data")
                break
    def findNvlinkInfo(self,key,regexCompileList,line,searchType):
        '''
        regex is the complile regex, 
        searchType means 0 for only once,1 for multiple time
        '''
        if searchType==0 and key in self.dataForeachSubstation[self.currentSubStation]:
            '''the data is already stored in dataForeachSubstation'''
            return
        for eachRegex in regexCompileList:
            result=eachRegex.search(line)
            if result is not None:
                key=result.group("nvlinkNum")+"$"+result.group("radias")
                self.dataForeachSubstation[self.currentSubStation][key]=result.group("data")
                #print(result.group("data"))
                #print(key)
                break
    def findPCIEErrorInfo(self,keyDict,line,searchType):
        
        for eachKey,regexList in keyDict.items():
            for eachRegex in regexList:
                result=eachRegex.search(line)
                if self.currentSubStation!="" and result is not None:
                    maxvalue=max(int(result.group("errorCount")),0 if eachKey not in self.dataForeachSubstation[self.currentSubStation] else self.dataForeachSubstation[self.currentSubStation][eachKey])
                    self.dataForeachSubstation[self.currentSubStation][eachKey]=maxvalue
                    #print(eachKey,result.group("errorCount"),maxvalue)
    def findStation(self,eachline):
        for key,eachRegexList in regexTemp.regexCompileMult.items():
                '''Find the data for each perfpoint'''
                find=False
                for eachRegex in eachRegexList:
                    data=self.parserOfSingleLine(eachRegex,eachline)
                    
                    if data is not None:
                        find=True
                        if key=="station":
                            
                            if data not in self.uniqueData:
                                self.uniqueData[data]={}
                            elif data in self.uniqueData and "exitErroCode" in self.uniqueData[data]:
                                self.uniqueData[data]["exitErroCode"]=None
                            elif data in self.uniqueData and "modsEndTime" in self.uniqueData[data]:
                                self.uniqueData[data].pop("modsEndTime")
                            elif data in self.uniqueData and "modsStartTime" in self.uniqueData[data]:
                                self.uniqueData[data].pop("modsStartTime")
                            elif data in self.uniqueData and "bgPrintCount" in self.uniqueData[data]:
                                self.uniqueData[data].pop("bgPrintCount")
                                
                            self.currentStation=data
                            if "Running" in eachline or "Heatsink" in eachline:
                                self.currentSubStation=data
                                if data not in self.dataForeachSubstation:
                                    self.dataForeachSubstation[data]={}
                            #logging.info(data)
                            
                        elif key=="subStation":
                            #logging.info(self.factoryInfo["filePath"])
                            #logging.info(self.currentStation)
                            #logging.info(data)
                            name=("" if self.currentStation is None else self.currentStation) +data
                            if self.currentSubStation is None:
                                self.currentSubStation=name
                            else:##add the suffix
                                self.currentSubStation=name
                    
                            

                            if name not in self.dataForeachSubstation:
                                self.dataForeachSubstation[name]={}
                        elif key=="exitErroCode":
                            self.currentStation=None
                            self.currentSubStation=None
                        if self.currentSubStation!=None:
                        
                            if key in ["pstate","nvvdd","subStation","station","ClkGpc"]:
                                #print(key,data)
                                if key =="nvvdd" and key in self.dataForeachSubstation[self.currentSubStation]:
                                    pass
                                elif key=="pstate" and key not in self.dataForeachSubstation[self.currentSubStation]:
                                    
                                    stationName=self.currentSubStation+"@"+data if "@" not in self.currentSubStation else self.currentSubStation
                                    self.currentSubStation=stationName
                                    #print(stationName)
                                    self.dataForeachSubstation[self.currentSubStation]={}
                                    
                                    if "subStationList" not in self.uniqueData:
                                
                                        self.uniqueData["subStationList"]=[stationName]
                                    else:
                                        self.uniqueData["subStationList"].append(stationName)
                                    self.dataForeachSubstation[self.currentSubStation][key]=data
                        return True
        return False
    def logAnalysis(self):
        
        self.factoryInfo["filePath"]=self.filePath
        fileReader=open(self.filePath,'r',errors='ignore')
        #count=0
        for eachFileline in fileReader:
            line = bytes(eachFileline, 'utf-8').decode('utf-8', 'ignore')
            eachline=re.sub("/", "", line)
            #count=count+1
            #logging.info(count)
            if self.findStation(eachline):
                pass
            #parseRInfo(line,self.uniqueData)
            if self.currentStation==None:
                continue
            
            if parseBGLoggerInfo(line, self.uniqueData,self.dataForeachSubstation,self.currentStation,self.currentSubStation):
                '''
                find the bglogger information and add them to substation data
                '''
                continue
            
            if parseModsStartTimeInfo(line,self.uniqueData,self.currentStation):
                '''
                find the mods start time
                '''
                continue
            
            elif parseFactoryInfo.parseFactoryInfo(line, self.uniqueData,self.currentStation):
                '''
                find the factory information from logs and added them to unique data
                '''
                continue            
            
            
            
            elif parseTestInfo(line, self.uniqueData,self.dataForeachSubstation,self.databyECID,self.currentStation,self.currentSubStation):
                '''
                find the information about the test like test number test time/test result/variants
                '''
                continue
            
            
                            
            #for key,regexList in regexTemp.regexCompileMultTest.items():
                
                #for eachRegex in regexList:
                    #print(eachRegex)
                    
                    #result=eachRegex.search(eachline)
                    
                   # if result is not None and self.currentSubStation!="":
                        #exitName=""
                        #if key=="ExitCode":
                            #pass
#                             exitName= result.group("testNumber")+"_"+result.group("errorCode")
#                             exitTestInfo=result.group("testNumber")+"$"+result.group("errorCode")+"$"+result.group("errorDescript")+"$"+result.group("exitTime")
#                             
#                             if self.currentSubStation!="" and "testList" not in self.dataForeachSubstation[self.currentSubStation]:
#                                 self.dataForeachSubstation[self.currentSubStation]["testList"]=[exitTestInfo]
#                             elif self.currentSubStation!="":
#                                 self.dataForeachSubstation[self.currentSubStation]["testList"].append(exitTestInfo)
                            
                            #print(exitTestInfo)
#                         elif key=="ErrorCode":
#                             exitName= result.group("errorCode")
#                         if self.currentSubStation!="" and key not in self.dataForeachSubstation[self.currentSubStation] and int(result.group("errorCode"))!=0:
#                             self.dataForeachSubstation[self.currentSubStation][key]=exitName
#                         elif self.currentSubStation!="" and key in self.dataForeachSubstation[self.currentSubStation] and int(result.group("errorCode"))!=0:
#                             self.dataForeachSubstation[self.currentSubStation][key]=self.dataForeachSubstation[self.currentSubStation][key]+"$"+exitName
#                     break;
def processLogs(args):
    logging.info("Process ID %d"%(os.getpid()))
    count=0
    resultList=[]
    fileList=args
    #que=args[1]
    total=len(fileList)
    #logging.info(fileList)
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
            #continue
            pass
            #continue
#         if not ( "bit" in eachLog \
#             or "fpt" in eachLog \
#             or "heatsink" in eachLog        
#             ):
#             continue
        
        logging.debug("start process log %s finished,count %d,totally %d"%(eachLog,count,total))
        logging.debug("parsed %.2f MB  finished,totally %.2f MB"%(round(parseSize,2),totalSize))
        parser=logFileParser(eachLog)
        parser.logAnalysis()
       # lock.aqurie()
        resultList.append(parser)
        #logging.debug(resultList)
       # lock.release()
        #while not que.empty():
            #logging.info(que.get())
        logging.debug("%.3f min for this log,already run for %.3f min, need %.3f min for this analysis"%((time.time()-currentTime)/60,(currentTime-startTime)/60,(currentTime-startTime)/60*totalSize/parseSize))
    logging.debug("exit")
    return resultList
def func(x):
    logging.info(x*x)           
            
        
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
    dirName="/home/tesla_pde/logfiles/FAIL/08/G503/TM"
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
    
       
            
        
        
    
    
    
    
        
        