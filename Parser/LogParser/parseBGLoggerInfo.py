import re
import logging
from LogParser.utilityString import getMaxDataFromString, getHBMTempDelta,getMinDataFromString

compileRe={}

'''
bglogger output for PG414
Power (INPUT_TOTAL_BOARD): [ 92994 92954 93043 93246 93051 93229 93335 93270 93294 93359 93472 93448 ]
    Power (INPUT_NVVDD): [ 50832 50974 50811 50775 51056 51056 51167 51167 51041 51182 51004 50864 ]
    Power (INPUT_SRAM): [ 13986 13887 13956 14035 14015 14025 14045 14035 14045 14134 14035 14035 ]
    Power (INPUT_PEX12V): [ 89994 89954 90043 90246 90051 90229 90335 90270 90294 90359 90472 90448 ]
    Power (INPUT_PEX3V3): [ 3000 3000 3000 3000 3000 3000 3000 3000 3000 3000 3000 3000 ]
    Power (INPUT_PWR_SRC_PP): [ 25176 25093 25276 25436 24980 25148 25123 25068 25208 25043 25433 25549 ]
    Power (OUTPUT_NVVDD): [ 55046 55221 55097 54478 30569 55022 55157 55009 55301 55316 55463 54990 ]
    Power (OUTPUT_NVVDD): [ 54079 54114 54143 54163 54224 54214 54258 54238 54275 54307 54277 54270 ]
    IntTemp: [ 63.5 63.7 64.0 64.1 64.2 64.3 64.5 64.5 64.6 64.7 64.8 64.9 ]
'''
compileRe={}
compileRe["gpuMaxTemp"]=[re.compile("TSOSC_AVG:\s+\[\s+(?P<data>.+)\s+\]",re.IGNORECASE),
                         re.compile("IntTemp:\s+\[\s+(?P<data>.+)\s+\]",re.IGNORECASE),
                         ]

compileRe["RValue"]=[re.compile("Min:\s+(?P<data>\d+)\s*",re.IGNORECASE),
                         re.compile("Max:\s+(?P<data>\d+)\s+",re.IGNORECASE),
                         ]

compileRe["TSOSC_OFFSET_MAX"]=[re.compile("TSOSC_OFFSET_MAX:\s+\[\s+(?P<data>.+)\s+\]",re.IGNORECASE)
                         ]

compileRe["HBM2_COMBINED_MAX"]=[re.compile("HBM2_COMBINED_MAX:\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["hbm0Temp"]=[re.compile("HBM2_DEFAULT\s+\(siteIdx\s+=\s+0\):\s+\[\s+(?P<data>.+)\s+\]")]
 
compileRe["hbm1Temp"]=[re.compile("HBM2_DEFAULT\s+\(siteIdx\s+=\s+1\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["hbm2Temp"]=[re.compile("HBM2_DEFAULT\s+\(siteIdx\s+=\s+2\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["hbm3Temp"]=[re.compile("HBM2_DEFAULT\s+\(siteIdx\s+=\s+3\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["INPUT_TOTAL_BOARD"]=[re.compile("Power\s+\(INPUT_TOTAL_BOARD\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["INPUT_PEX12V"]=[re.compile("Power\s+\(INPUT_PEX12V\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["INPUT_PEX3V3"]=[re.compile("Power\s+\(INPUT_PEX3V3\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["INPUT_PWR_SRC_PP"]=[re.compile("Power\s+\(INPUT_PWR_SRC_PP\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["INPUT_SRAM"]=[re.compile("Power\s+\(INPUT_SRAM\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["INPUT_FBVDD"]=[re.compile("Power\s+\(INPUT_FBVDD\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["INPUT_NVVDD"]=[re.compile("Power\s+\(INPUT_NVVDD\):\s+\[\s+(?P<data>.+)\s+\]")]
 
compileRe["INPUT_EXT12V_8PIN0"]=[re.compile("Power\s+\(INPUT_EXT12V_8PIN0\):\s+\[\s+(?P<data>.+)\s+\]")]
compileRe["OUTPUT_NVVDD"]=[re.compile("Power\s+\(OUTPUT_NVVDD\):\s+\[\s+(?P<data>.+)\s+\]")]
def parseBGLoggerInfo(line,logInfoResult,loginfoForSubStation,currentStation,currentSubStation):
    
    #if substation =="":
        #return
    if "exitErroCode" in logInfoResult[currentStation] and logInfoResult[currentStation]["exitErroCode"]=="ModsDrvBreakPoint":
        
        return True    
    if  currentStation==None:
        return False
    
    for key,eachRegexList in compileRe.items():
        
        for eachRegex in eachRegexList:
            result=eachRegex.search(line)

            if result is not None:
                
                if key == "RValue":
                    if "RValue" not in logInfoResult[currentStation]:
                        logInfoResult[currentStation]["RValue"]=result.group("data")
                    else:
                        logInfoResult[currentStation]["RValue"]=logInfoResult[currentStation]["RValue"]+" "+result.group("data")
                        
                    RValueList=logInfoResult[currentStation]["RValue"].split(" ")
                    indexCount=0
                    
                    for eachRValue in ["hbmdetla_min_R","hbmdetla_max_R","hbm0_min_R","hbm0_max_R","hbm1_min_R","hbm1_max_R",
                                       "hbm2_min_R","hbm2_max_R","hbm3_min_R","hbm3_max_R"]:
                        logInfoResult[currentStation][eachRValue]="" if len(RValueList)<indexCount+1 else RValueList[indexCount]
                        indexCount+=1
                    
                    #logInfoResult[currentStation]["hbmdetla_min_R"]="" if len(RValueList)<1 else RValueList[0]
                    #logInfoResult[currentStation]["hbmdetla_max_R"]="" if len(RValueList)<2 else RValueList[1]
                    #logInfoResult[currentStation]["hbm0_min_R"]="" if len(RValueList)<3 else RValueList[2]
                    #logInfoResult[currentStation]["hbm0_max_R"]="" if len(RValueList)<4 else RValueList[3]
                    #logInfoResult[currentStation]["hbm1_min_R"]="" if len(RValueList)<5 else RValueList[4]
                    #logInfoResult[currentStation]["hbm1_max_R"]="" if len(RValueList)<6 else RValueList[5]
                    #logInfoResult[currentStation]["hbm2_min_R"]="" if len(RValueList)<7 else RValueList[6]
                    #logInfoResult[currentStation]["hbm2_max_R"]="" if len(RValueList)<8 else RValueList[7]
                    #logInfoResult[currentStation]["hbm3_min_R"]="" if len(RValueList)<9 else RValueList[8]
                    #logInfoResult[currentStation]["hbm3_max_R"]="" if len(RValueList)<10 else RValueList[9]
                    
                if key =="gpuMaxTemp":
                    if "bgPrintCount" not in logInfoResult[currentStation]:
                        logInfoResult[currentStation]["bgPrintCount"]=1
                    else:
                        logInfoResult[currentStation]["bgPrintCount"]=logInfoResult[currentStation]["bgPrintCount"]+1
                    if logInfoResult[currentStation]["bgPrintCount"]<6:
                        logInfoResult[currentStation]["GpuTemp_5Minutes"]=result.group("data") if "GpuTemp_5Minutes"  not in logInfoResult[currentStation] \
                                                                                            else logInfoResult[currentStation]["GpuTemp_5Minutes"]+" "+result.group("data")
                    
                
                maxValue=getMaxDataFromString(result.group("data")) if key+"_Max" not in logInfoResult[currentStation] else max(logInfoResult[currentStation][key+"_Max"],getMaxDataFromString(result.group("data")))
                minValue=getMinDataFromString(result.group("data")) if key+"_Min" not in logInfoResult[currentStation] else min(logInfoResult[currentStation][key+"_Min"],getMinDataFromString(result.group("data")))
                
                logInfoResult[currentStation][key+"_Max"]=maxValue
                logInfoResult[currentStation][key+"_Min"]=minValue
                #logInfoResult[currentStation][key+"lastMax"]=getMaxDataFromString(result.group("data"))
                #logInfoResult[currentStation][key+"RawData"]=str(getMaxDataFromString(result.group("data"))) if key+"RawData" not in logInfoResult[currentStation] else logInfoResult[currentStation][key+"RawData"]+" " +str(getMaxDataFromString(result.group("data"))) 

                #logInfoResult[currentStation][key+"print"]=result.group("data") if key+"print" not in logInfoResult[currentStation] else logInfoResult[currentStation][key+"print"]+" "+result.group("data")
                
#                 if key=="hbm3Temp":
#                     
#                     logInfoResult[currentStation]["hbm01Delta"]=getHBMTempDelta("10 -20 0 0" if "hbm01Delta" not in logInfoResult[currentStation] else logInfoResult[currentStation]["hbm01Delta"],\
#                                                                                 logInfoResult[currentStation]["hbm0Tempprint"],logInfoResult[currentStation]["hbm1Tempprint"])
#                     logInfoResult[currentStation]["hbm02Delta"]=getHBMTempDelta("10 -20 0 0" if "hbm02Delta" not in logInfoResult[currentStation] else logInfoResult[currentStation]["hbm02Delta"],\
#                                                                                 logInfoResult[currentStation]["hbm0Tempprint"],logInfoResult[currentStation]["hbm2Tempprint"])
#                     logInfoResult[currentStation]["hbm03Delta"]=getHBMTempDelta("10 -20 0 0" if "hbm03Delta" not in logInfoResult[currentStation] else logInfoResult[currentStation]["hbm03Delta"],\
#                                                                                 logInfoResult[currentStation]["hbm0Tempprint"],logInfoResult[currentStation]["hbm3Tempprint"])
#                     logInfoResult[currentStation]["hbm12Delta"]=getHBMTempDelta("10 -20 0 0" if "hbm12Delta" not in logInfoResult[currentStation] else logInfoResult[currentStation]["hbm12Delta"],\
#                                                                                 logInfoResult[currentStation]["hbm1Tempprint"],logInfoResult[currentStation]["hbm2Tempprint"])
#                     logInfoResult[currentStation]["hbm13Delta"]=getHBMTempDelta("10 -20 0 0" if "hbm13Delta" not in logInfoResult[currentStation] else logInfoResult[currentStation]["hbm13Delta"],\
#                                                                                 logInfoResult[currentStation]["hbm1Tempprint"],logInfoResult[currentStation]["hbm3Tempprint"])
#                     logInfoResult[currentStation]["hbm23Delta"]=getHBMTempDelta("10 -20 0 0" if "hbm23Delta" not in logInfoResult[currentStation] else logInfoResult[currentStation]["hbm23Delta"],\
#                                                                                 logInfoResult[currentStation]["hbm2Tempprint"],logInfoResult[currentStation]["hbm3Tempprint"])
#                     
                    #logging.info(logInfoResult[currentStation]["hbm01Delta"])
                #logging.info(result.group("data"))
                if currentSubStation in loginfoForSubStation:
                    if key not in loginfoForSubStation[currentSubStation]:
                        #pass
                        #logging.info(key)
                        #logging.info(result.group("data"))
                        #logging.info(getMaxDataFromString(result.group("data")))
                        loginfoForSubStation[currentSubStation][key]=result.group("data")
                    else:
                        #pass
                        #logging.info(key)
                        loginfoForSubStation[currentSubStation][key]=loginfoForSubStation[currentSubStation][key]+" "+result.group("data")
                return True
    return False