import re
import logging


compileRe={}

compileRe["modsStartTime"]=[re.compile("MODS\s+start:\s+(?P<data>.+) ",re.IGNORECASE)]
 
 
compileRe["modsEndTime"]=[re.compile("MODS\s+end\s+:.+\s+\[(?P<data>.+)\s+seconds.+\]",re.IGNORECASE)]
compileRe["VBIOSVersion"]=[re.compile("ROM\s+Version\s+:\s+(?P<data>.+) ",re.IGNORECASE)]
compileRe["ModsVersion"]=[re.compile("MODS\s+:\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["BuildDate"]=[re.compile("Build\s+Date\s+:\s+(?P<data>.+)",re.IGNORECASE),re.compile("BoardBuildDate:\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["SerialNumber"]=[
                           re.compile("Serial\s+Number\s+:\s+(?P<data>.+)",re.IGNORECASE),
                           re.compile("Prod\s+Ser\.\s+No\.\s+:\s+(?P<data>\d+)\s+"),
                           re.compile("BoardSerialNumber:\s+(?P<data>\d+)",re.IGNORECASE)
                           ]

# #Object           : OBD (v1.1)
#   Build Date       : 2018/01/10
#   Marketing Name   : TESLA P4
#   Serial Number    : 0420218022604
#   Memory Man.      : S
#   Memory Part ID   : 161-0172-600
#   Memory Date Code : 
#   Product Part Num : 900-2G414-0000-000
#  699 Prod Part Num : 699-2G414-0200-101
#Scan SN: 0420218022603
compileRe["ScanSN"]=[re.compile("Scan\s+SN:\s+(?P<data>.+)")]
compileRe["MemorySize"]=[re.compile("Memory\s+Size\s+:\s+(?P<data>\d+)")]

#Memory Size    : 32768 MB 
compileRe["MarketingName"]=[re.compile("Marketing\s+Name\s+:\s+(?P<data>.+)",re.IGNORECASE),re.compile("MarketingName:\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["MemoryVendor"]=[re.compile("Memory\s+Man\.\s+:\s+(?P<data>.+)",re.IGNORECASE),re.compile("MemoryManufacturer:\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["MemoryPN"]=[re.compile("Memory\s+Part\s+ID\s+:\s+(?P<data>.+)",re.IGNORECASE),re.compile("MemoryPartID:\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["ProductPN"]=[re.compile("Product\s+Part\s+Num\s+:\s+(?P<data>.+)",re.IGNORECASE),re.compile("BoardProductPartNumber:\s+(?P<data>.+)",re.IGNORECASE)]


compileRe["699PN"]=[re.compile("699\s+Prod\s+Part\s+Num\s+:\s+(?P<data>.+)",re.IGNORECASE),re.compile("Board699PartNumber:\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["Project"]=[re.compile("Project\s+:\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["ateSpeedo"]=[re.compile("AteSpeedo\s+:\s+(?P<data>\d+)")]
compileRe["AteIddq"]=[re.compile("AteIddq\s+:\s+(?P<data>\d+)")]
compileRe["KernelDriver"]=[re.compile("KernelDriver\s+:\s+(?P<data>.+)")]
compileRe["ecid"]=[re.compile("ECID\s+:\s+(?P<data>.+-.+\w)\s+"),re.compile("ECID\s+=\s+(?P<data>.+-.+\w)")]
compileRe["exitErroCode"]=[re.compile("Error\s+Code\s+=\s+(?P<data>\d+)\s+\(.+\)"),re.compile("\*{1,5}(?P<data>INTERRUPT\s+AND\s+RESTART)\*{1,5}",re.IGNORECASE)]

def parseModsStartTimeInfo(line,logInfoResult,currentStation):
    
    '''
    add mods start time info to unique data and only get the first match
    '''
    if "exitErroCode" in logInfoResult[currentStation] and logInfoResult[currentStation]["exitErroCode"]=="ModsDrvBreakPoint":
        
        return True
    if currentStation==None:
        return False
    for key, eachRegexList in compileRe.items():
        
        for eachRegex in eachRegexList:
        
            result=eachRegex.search(line)
            
            if result is not None:
                if key=="exitErroCode":
                    '''record the last error code == xxxxx and mods end time'''
                    #logging.info(currentStation)
                    #logging.info(result.group("data"))
                    logInfoResult[currentStation][key]=result.group("data")
                if key not in logInfoResult[currentStation]:
                    '''''' 
                    #logging.info(key)
                    logInfoResult[currentStation][key]=result.group("data")
                return True
                
    return False