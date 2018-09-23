import re
import logging


'''
*****INTERRUPT AND RESTART*****


Factory Information
Monitor SN:MONQ00871
HardDisk SN:W3TQRNA3
HardDisk Health:100 %
Power-On Time Count:7046
Drive Power Cycle Count:373
CPUID:000306E4
Brand String:      Intel(R) Xeon(R) CPU E5-1620 v2 @ 3.70GHz
Mac Address:1C1B0D23AE8E,1C1B0D23AE8F
DiagVer:618-20930-S384-CMF
PCIE Riser Card ID:NONE
BrdSN:0323917105670
FLAT ID:7K-13
Routing:EFT
FOX_Routing:EFT
PN:900-2G503-0410-000
BIOS:88.00.13.00.02
Error Code:E020000199282
StartTestTime:20171009050550
EndTesttime:20171009154342
Operator:G4715507
SFC:YES
****END****


'''

compileRe={}


compileRe["VBIOSVersion"]=[re.compile("ROM\s+Version\s+:\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["BuildDate"]=[re.compile("Build\s+Date\s+:\s+(?P<data>.+) ",re.IGNORECASE)]

compileRe["699PN"]=[re.compile("699\s+Prod\s+Part\s+Num\s+:\s+(?P<data>.+) ",re.IGNORECASE)]
compileRe["Project"]=[re.compile("Project\s+:\s+(?P<data>.+) ",re.IGNORECASE)]
compileRe["ateSpeedo"]=[re.compile("AteSpeedo\s+:\s+(?P<data>\d+)")]
compileRe["AteIddq"]=[re.compile("AteIddq\s+:\s+(?P<data>\d+)")]
 
 
 
compileRe={
            "commandLine":[re.compile("^Command\s+Line\s+:(?P<data>.+-spec.+)", re.IGNORECASE)],
            "E2992SN:":[re.compile("E2992SN:(?P<data>.+)$",re.IGNORECASE)],
            "E3664SN:":[re.compile("E3664SN:(?P<data>.+)$",re.IGNORECASE)],
            "RADIATION_SN":[re.compile("RADIATION_SN:(?P<data>.+)$",re.IGNORECASE)],
            "MonitorSN":[re.compile("Monitor\s+SN:(?P<data>.+)$",re.IGNORECASE)],
           "HardDiskSN":[re.compile("HardDisk\s+SN:(?P<data>.+)$",re.IGNORECASE)],
           "HardDiskHealth":[re.compile("HardDisk\s+Health:(?P<data>.+)", re.IGNORECASE)],
           "PowerOnTimeCount":[re.compile("Power-On\s+Time\s+Count:(?P<data>.+)$",re.IGNORECASE)],
           "DrivePowerCycleCount":[re.compile("Drive Power Cycle Count:(?P<data>.+)$",re.IGNORECASE)],
           "MacAddress":[re.compile("Mac\s+Address:(?P<data>.+)$",re.IGNORECASE)],
           "DiagVer":[re.compile("DiagVer:(?P<data>.+)$",re.IGNORECASE)],
           "BrdSN":[re.compile("BrdSN:(?P<data>.+)$",re.IGNORECASE)],
           "FLATID":[re.compile("FLAT\s+ID:(?P<data>.+)$",re.IGNORECASE)],
           "ErrorCode":[re.compile("Error\s+Code:(?P<data>.+)$")],
           "Routing":[re.compile("Routing:(?P<data>.+)$",re.IGNORECASE)],
           "StartTestTime":[re.compile("StartTestTime:(?P<data>.+)$",re.IGNORECASE)],
           "EndTesttime":[re.compile("EndTesttime:(?P<data>.+)$",re.IGNORECASE)],
             
           }
compileRe["IRQ"]=[re.compile("kernel:\s+mods.+\s+IRQ\s+(?P<data>\d+)$",re.IGNORECASE)]
compileRe["ModsIRQ"]=[re.compile("IRQ\s+:\s+(?P<data>\d+)",re.IGNORECASE)]
compileRe["HostName"]=[re.compile("HostName\s+:\s+(?P<data>.+)")]

compileRe["Nautilus Fatorcy Code"]=[re.compile("Factory\s+Error\s+Code\s+=(?P<data>.+)")]


def parseFactoryInfo(line,logInfoResult,currentStation):
    

    if "exitErroCode" in logInfoResult[currentStation] and logInfoResult[currentStation]["exitErroCode"]=="ModsDrvBreakPoint":
        
        return True
    if currentStation is None:
        return False
    
    for key,eachRegexList in compileRe.items():
        
        for eachRegex in eachRegexList:
            
            result=eachRegex.search(line)
            if key=="IRQ" and result is not None:
                logInfoResult[currentStation][key]=result.group("data")
            if key in logInfoResult:
                '''only record factory info if it's not in records'''
                continue            
            
            if result is not None:           
                logInfoResult[currentStation][key]=result.group("data")
                return True
    return False
            
