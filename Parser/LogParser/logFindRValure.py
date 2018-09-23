import re
import logging
from LogParser.utilityString import getMaxDataFromString, getHBMTempDelta,getMinDataFromString

compileRe={}

compileRe["HBMIndex"]=[re.compile("===HBM2_DEFAULT\s+\(siteIdx\s+=\s+(?P<data>\d)\)===",re.IGNORECASE),
                       re.compile("===(?P<data>\w+_\w+)===",re.IGNORECASE)]



#R at 10 seconds after idle: 5.20708371301e-05
compileRe["RValueTime"]=[re.compile("R\s+at\s+(?P<time>\d+)\s+seconds\s+after\s+idle:\s+(?P<Rdata>.+)",re.IGNORECASE)]
#R at max: 7.41243681499e-05

compileRe["R_Max"]=[re.compile("R\s+at\s+max:\s+(?P<Rdata>.+)",re.IGNORECASE)]


def parseRInfo(line,logInfoResult):
    
    currentStation="RValueCheckSpec"
    
    hbmIndex=""
    
    if currentStation not in logInfoResult:
        logInfoResult[currentStation]={}
        
    if  "hbmIndex" in  logInfoResult[currentStation]:
        hbmIndex=logInfoResult[currentStation]["hbmIndex"]
        #logging.info(hbmIndex)
    
    for key,eachRegexList in compileRe.items():
        for eachRegex in eachRegexList:
            
            result=eachRegex.search(line)
            
            if result is not None:
                if key =="HBMIndex":
                   # if "TSOSC_AVG" in 
                    logInfoResult[currentStation]["hbmIndex"]="HBMIndex_"+result.group("data")
                    #logging.info(result.group("data"))
                    #logging.info(line)
                    
                    if "TSOSC_AVG" in line:
                        logInfoResult[currentStation]["hbmIndex"]="GPU"
                        logging.info(result.group("data"))
                    
                elif key =="RValueTime":
                    time=result.group("time")
                    logInfoResult[currentStation][hbmIndex+"_RValue_at_"+time]=result.group("Rdata")
                elif key=="R_Max":
                    logInfoResult[currentStation][hbmIndex+"_RMax"]=result.group("Rdata")
            
                #logging.info(logInfoResult[currentStation])
                        
                        
            

