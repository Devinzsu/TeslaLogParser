import re
from FilePathParser import FileUtility 
import logging
from LogParser import logParser
from xlsxReport import reportGenerator
import os
import sys

if __name__=="__main__":
    
    dirName=None
    if len(sys.argv)>1:
        dirName=sys.argv[1]
    else:
        dirName=os.getcwd()#if len(sys.argv)<=1 else dir=sys.argv[1]  
    
    fileList=FileUtility.workThroughDir(dirName, "log")
    resultList=[]
    logging.basicConfig(filename='K80Download.log',filemode='w',level=logging.DEBUG)
    console = logging.StreamHandler()  
    console.setLevel(logging.DEBUG)  
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')  
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console) 
    count=0
    total=len(fileList)
    analysisFolder=[]
    
    for eachLog in fileList:
        print(os.path.dirname(eachLog))
        if os.path.dirname(eachLog) not in analysisFolder:
            analysisFolder.append(os.path.dirname(eachLog))
    for eachFolder in analysisFolder:
        
        logList=FileUtility.workThroughDir(eachFolder, "log")
        #print(logList)
        
        excelName=eachFolder.split(os.sep)[len(eachFolder.split(os.sep))-3]+eachFolder.split(os.sep)[len(eachFolder.split(os.sep))-2]+eachFolder.split(os.sep)[len(eachFolder.split(os.sep))-1]
        resultList=[]
        for eachFile in logList:
    
            count+=1
            logging.debug("start process log %f finished,count %d,totally %d"%(round(float(count/total),2),count,total))
            logging.debug("start process log %s"%eachFile)
            parser=logParser.logFileParser(eachFile)
            parser.logAnalysis()
            resultList.append(parser)
        report=reportGenerator.reportGenerate(excelName+".xlsx",resultList)
        report.compareLogs("compare", 0, 0)
    #report
    
            
            

    