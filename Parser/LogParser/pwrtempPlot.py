import re
from FilePathParser.FileUtility import workThroughDir
from xlsxwriter.workbook import Workbook

gpuTempReg="TSOSC_AVG:\s*\[\s+(?P<data>.+)\s+\]"

hbmCmbTempReg="HBM2_COMBINED_MAX:\s+\[\s+(?P<data>.+)\s+\]"

hbm0TempReg="HBM2_DEFAULT\s+\(siteIdx\s+=\s+0\):\s+\[\s+(?P<data>.+)\s+\]"
hbm1TempReg="HBM2_DEFAULT\s+\(siteIdx\s+=\s+1\):\s+\[\s+(?P<data>.+)\s+\]"
hbm2TempReg="HBM2_DEFAULT\s+\(siteIdx\s+=\s+2\):\s+\[\s+(?P<data>.+)\s+\]"
hbm3TempReg="HBM2_DEFAULT\s+\(siteIdx\s+=\s+3\):\s+\[\s+(?P<data>.+)\s+\]"
totalPowerReg="Power\s+\(INPUT_TOTAL_BOARD\):\s+\[\s+(?P<data>.+)\s+\]"

INPUT_PEX12VReg="Power\s+\(INPUT_PEX12V\):\s+\[\s+(?P<data>.+)\s+\]"
INPUT_NVVDDReg="Power\s+\(INPUT_NVVDD\):\s+\[\s+(?P<data>.+)\s+\]"
switchPstateReg="Switched\s+to\s+PState\s+0\s+\((?P<pstate>.+)\)"

startTCTTestReg="Start\s+Test|s+Temperature\s+Cycling\s+Test\s+timestamp"
regList={
    "totalPower":totalPowerReg,
    "gpuTemp":     gpuTempReg,
    "hbmCmbTemp":    hbmCmbTempReg,
    "hbm0Temp":    hbm0TempReg,
    "hbm1Temp":    hbm1TempReg,
    "hbm2Temp":   hbm2TempReg,
    "hbm3Temp":   hbm3TempReg
         }

regList={
    "totalPower":totalPowerReg,
    "gpuTemp":     gpuTempReg,
    "INPUT_PEX12V":    INPUT_PEX12VReg,
    "INPUT_NVVDD":INPUT_NVVDDReg
    
         }
    
def getTempInfo(line,reg=None):####
    tempResult=re.search(reg, line) 
    ret=None
    maxValue=None
    if tempResult is not None:
        #print(tempResult.group("gpuTemp").strip().split(" "))
        ret=tempResult.group("data").strip()
        
        maxValue=max(ret.split())
        
    return maxValue
        
        
        
if __name__=="__main__":
    filePaths=workThroughDir("/mnt/storageDisk1/PG414/sample",".log")
    wb=Workbook("G414_pwrTemp.xlsx")
    rowIndex=0
    count=0
    for eachFile in filePaths:
        hbmTemp=""
        gpuTemp=""
        fileReader=open(eachFile)
        valueDict={}
        #worksheet=""
        pstate="N/A"
        startTCTCount=0
        count+=1
        print("Start to analyze %d of %d"%(count,len(filePaths)))
        for eachLine in fileReader.readlines():
            
            pstateResult=re.search(switchPstateReg, eachLine)
            startTctResult=re.search(startTCTTestReg, eachLine)
            if pstateResult is not None:
                pstate=pstateResult.group("pstate")
                #print(pstate)
            if startTctResult is not None:
                startTCTCount+=1
            
            for key,value in regList.items():
                
                if key not in valueDict:
                    valueDict[key]=""
                if wb.get_worksheet_by_name(key) is None:
                    wb.add_worksheet(key)  
                gret=getTempInfo(eachLine,value)
                #print(valueDict[key])
                #if gret is not None:
                    #print(value,gret)
                valueDict[key]=valueDict[key]+" "+gret if gret is not None else valueDict[key]
                #print(valueDict)
        #print(valueDict)
        for key,values in valueDict.items():
            #print(key,values)
            sheet=wb.get_worksheet_by_name(key)
            sheet.write_row(rowIndex,0,[eachFile,key])
            data=values.strip().split(" ")
            print(data)
            
            format=wb.add_format()
            format.set_num_format('0.0')
            #sheet.write_row(rowIndex,2,[pstate],format)
            if len(data)<2:
                continue  
            results = [float(i) for i in data]
            #sheet.write(rowIndex,4,results[len(results)-1])                      
            sheet.write_row(rowIndex,2,results,format)
        rowIndex+=1        #print(hbmTemp)
            
    wb.close()       
    #print(filePaths)