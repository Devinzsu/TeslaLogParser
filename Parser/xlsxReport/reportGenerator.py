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
from fileinput import filename
#from django.template.defaultfilters import first
#from numpy.lib.function_base import average
#from tracemalloc import Statistic
class reportGenerate():
    
    def __init__(self,fileName,data):
        self.wk=Workbook(fileName)
        self.wk.set_properties({
                'title':    'This is a Tesla Loginfo',
                'subject':  'With document properties',
                'author':   'Devin Xu',
                'manager':  'Levy Li',
                'company':  'NVIDIA',
                'category': 'Log parser spreadsheets',
                'comments': 'Created with Python and XlsxWriter',
            })
        self.loginfo=data
        self.defineTitle=["filePath","^SN","SerialNumber","ScanSN","ecid","IRQ","KernelDriver","ModsIRQ","ateSpeedo","VBIOSVersion","AteIddq","MemorySize","T148Failure"
                          ,"MarketingName"
                          ,"MemoryVendor"
                          ,"MemoryPN"
                          ,"ProductPN"
                          
                          ,"Station","BuildDate","ModsVersion","699PN","Project","exitErroCode","LastErrorCode","failuresite",
                        "site\d+.+","fused*","failurePartition","pageRetirements","Nautilus Fatorcy Code","Failure Details","Failure Code",".+TestTime","EC139FailTime"
                          "modsStartTime","modsEndTime","TestTime","HostName","FLATID","E.+SN","DiagVer","StartTestTime","EndTesttime","ErrorCode","lastEnterTest","lastEnterTestTime",
                         # "lastStation",
                          "reboot",
                          ".+Gflops",
                        #  ,"INPUT.+"
                        #  ,"OUTPUT_NVVDD"
                         # ,"AdcError*"
                          "_MAX$"
                          ,".+RawData"
                          #,"_Min",".+lastMax",".+Delta"
                          ,"_R$"
                          ,"hbmIndex.+","GPU_"
                          ,".+print"
                          ,"local*","host*","PEXLanesXStatus","PEXLanesYStatus"
                          ,"NVLink0X"
                          ,"NVLink0Y"
                          ,"NVLink1X"
                          ,"NVLink1Y"
                          ,"NVLink2X"
                          ,"NVLink2Y"
                          ,"NVLink3X"
                          ,"NVLink3Y"
                          ,"NVLink4X"
                          ,"NVLink4Y"
                          ,"NVLink5X"
                          ,"NVLink5Y"
                          
                   ]
        self.orderTitleList=[]
    def addNVLinkTittleList(self):
        nvlinkList=[]
        nvlinkList.append("NVLink0$X_STATUS")
        nvlinkList.append("NVLink0$Y_STATUS")
        
        nvlinkList.append("NVLink1$X_STATUS")
        nvlinkList.append("NVLink1$Y_STATUS")
        
        nvlinkList.append("NVLink2$X_STATUS")
        nvlinkList.append("NVLink2$Y_STATUS")
        
        nvlinkList.append("NVLink3$X_STATUS")
        nvlinkList.append("NVLink3$Y_STATUS")
        
        nvlinkList.append("NVLink4$X_STATUS")
        nvlinkList.append("NVLink4$Y_STATUS")
        
        nvlinkList.append("NVLink5$X_STATUS")
        nvlinkList.append("NVLink5$Y_STATUS")
        
        for eachTittle in nvlinkList:
            if eachTittle not in self.titleList:
                self.titleList.append(eachTittle)
        
    def addPexTittleList(self):
        
        
        pexList=[]
        pexList.append("local_Correctable")
        pexList.append("host_Correctable")
        pexList.append("local_none_fatal")
        pexList.append("host_none_fatal")
        pexList.append("local_fatal")
        pexList.append("host_fatal")
        pexList.append("local_lineErrors")
        pexList.append("local_CRCErrors")
        pexList.append("local_NAKs_received")
        pexList.append("local_NAKs_received")
        pexList.append("local_failedL0sExits")
        pexList.append("local_NAKs_sent")
        
        for eachTittle in pexList:
            if eachTittle not in self.titleList:
                self.titleList.append(eachTittle)
        #print(self.titleList)
        return pexList
    def addPexErrorInfo(self,data,eachSubStationInfo):
        
        
        pexList=self.addPexTittleList()
        for eachPex in pexList:
            data[eachPex]="" if eachPex not in eachSubStationInfo else eachSubStationInfo[eachPex]
            
        
        
    def addDataPerTittleList(self):
        
        pass
        
    def getTitleList(self):
        'return the unordered title list'
        titleSet=set()
        self.orderTitleList=[]
        for eachlogInfo in self.loginfo:
            col=0
            #if "FunctionalSpec" in eachlogInfo.logInfo and \
            uniqueData=eachlogInfo.uniqueData
            fatoryInfo=eachlogInfo.factoryInfo
            #print(uniqueData)
            eachSubStationData=eachlogInfo.dataForeachSubstation
            for eachStation in uniqueData:
                titleSet.update(uniqueData[eachStation])
            titleSet.update(eachSubStationData)
            titleSet.update(fatoryInfo)
            titleSet.update(["Station"])
            titleSet.update(["TestTime"])
            titleSet.update(["LastErrorCode"])
            
            
        for eachOrderTitle in self.defineTitle:
            
            tempList=[]
            for eachGetTitle in list(titleSet):
                #logging.info(eachOrderTitle)
                #logging.info(eachGetTitle)
            
                result=re.search(eachOrderTitle, eachGetTitle, re.IGNORECASE)
                if result is not None and eachGetTitle not in self.orderTitleList:
                    
                    
                    tempList.append(eachGetTitle)
            
            #logging.info("add %s to title list"%(sorted(tempList)))
            self.orderTitleList=self.orderTitleList+sorted(tempList)
        logging.info(self.orderTitleList)
        return list(self.orderTitleList)
    def ttoAnalysis(self,run_on_error):
        
        
        failureListByStation={}
        loginfoSheet=self.wk.add_worksheet("TTO_Failure Details")
        
        if run_on_error==False:
            
            for eachLoginfo in self.loginfo:
                
                logData=eachLoginfo.uniqueData
                fileName=eachLoginfo.factoryInfo["filePath"]
                
                for eachStation in logData:
                    if "List" in eachStation:
                        continue
                    failureInfo=None if "Failure Details" not in logData[eachStation] else logData[eachStation]["Failure Details"]
                    
                    if failureInfo is None:
                        continue
                    failureList=failureInfo.split("$$")
                    #logging.info(failureList)
                    for eachFailureTest in failureList:
                        failureSplit=eachFailureTest.split('$')
                        #logging.info(fileName)
                        #logging.info(eachFailureTest)
                        #logging.info(failureSplit)
                        station=failureSplit[0]
                        testName="NA" if len(failureSplit)<2 else failureSplit[1]
                        testNumber="NA" if len(failureSplit)<3 else failureSplit[2]
                        testID="NA" if len(failureSplit)<4 else failureSplit[3]
                        errorCode="NA" if len(failureSplit)<5 else failureSplit[4]
                        
                        failreDict={"testName":testName,"testNumber":testNumber,"testID":testID,"errorCode":errorCode,"faileName":fileName}
                        
                        if station not in failureListByStation:
                            failureListByStation[station]=[failreDict]
                        else:
                            failureListByStation[station].append(failreDict)
            row=0
            for eachStation in failureListByStation:
                logging.info(eachStation)
                col=0###
                loginfoSheet.write_row(0,0,["Station","Test","Test Number","Test ID","error Code","FileName"])
                for eachFailureDict in failureListByStation[eachStation]:
                    logging.info(row)
                    row+=1
                    col=0
                    loginfoSheet.write(row,col,eachStation)
                    col+=1
                    loginfoSheet.write(row,col,eachFailureDict["testName"]+eachFailureDict["testNumber"]+eachFailureDict["testID"] )
                    col+=1
                    loginfoSheet.write(row,col,eachFailureDict["testNumber"])
                    col+=1
                    loginfoSheet.write(row,col,eachFailureDict["testID"].replace("NA",""))
                    col+=1
                    loginfoSheet.write(row,col,eachFailureDict["errorCode"])
                    col+=1
                    #logging.info(eachFailureDict["faileName"])
                    loginfoSheet.write(row,col,eachFailureDict["faileName"])
                    
                        
            
            
        
    def getDataFromLoginfo(self,logInfo,key):
        
        value=0
        if "pwr".upper()in key.upper() or "temp".upper()in key.upper():
            data=self.getDataFromStr(logInfo[key])
            value=max(data)
        else:
            value=logInfo[key]
        return value
            
    def failureByECID(self,sheetName):
        
        self.defineTitle=["^SN","SerialNumber","ecid","IRQ","ModsIRQ","ateSpeedo","VBIOSVersion","ModsVersion","AteIddq","BuildDate","699PN","Project","exitErroCode",
                          "PSHCBEU","failuresite","site.+","failurePartition","fused*","pageRetirements","Failure Code"]
        row=0
        col=0
        self.getTitleList()
        loginfoSheet=self.wk.add_worksheet(sheetName)
        loginfoSheet.write_row(row, col, self.orderTitleList)
        ecidData={}
        for eachlogInfo in self.loginfo:
            
            col=0
            uniqueData=eachlogInfo.uniqueData
            
            factoryInfo=eachlogInfo.factoryInfo
            ecidInfo=eachlogInfo.databyECID
            #logging.info(uniqueData)
            eachSubStationData=eachlogInfo.dataForeachSubstation
            
                
               # if 
            #logging.debug(eachSubStationData)
            for eachStation in  uniqueData:
                data=[]
                #logging.info(eachStation)
                #logging.info(uniqueData[eachStation])
                if "List"  in eachStation or "ecid" not in uniqueData[eachStation]:
                    continue
                ecid=uniqueData[eachStation]["ecid"]
                if uniqueData[eachStation]["ecid"] not in ecidData:
                    ecidData[ecid]={}
                for eachTitle in self.orderTitleList:
                    
                    
                    
                    if eachTitle in uniqueData[eachStation] and "site" in eachTitle:
                        if "site" in eachTitle:
                            if eachTitle not in ecidData[ecid]:
                                ecidData[ecid][eachTitle]=uniqueData[eachStation][eachTitle] 
                            else:
                                for eachSitefailInfo in uniqueData[eachStation][eachTitle].split(","):
                                    ecidData[ecid][eachTitle]=ecidData[ecid][eachTitle] if eachSitefailInfo  in ecidData[ecid][eachTitle] and len(ecidData[ecid][eachTitle])>250 else  ecidData[ecid][eachTitle]+", "+eachSitefailInfo
                                                                    
                        #data.append(uniqueData[eachStation][eachTitle])
                    #elif eachTitle in eachSubStationData:
                        #data.append(eachSubStationData[eachStation][eachTitle])
                    elif eachTitle in uniqueData[eachStation] and "fuse" in eachTitle:
                        if eachTitle not in ecidData[ecid]:
                            ecidData[ecid][eachTitle]=uniqueData[eachStation][eachTitle] if eachTitle not in ecidData[ecid] else ecidData[ecid][eachTitle]+", "+uniqueData[eachStation][eachTitle]
                            
                        else:
                            for eachfuse in uniqueData[eachStation][eachTitle].split(","):
                                if eachfuse.strip() not in ecidData[ecid][eachTitle]:
                                    ecidData[ecid][eachTitle]=ecidData[ecid][eachTitle]+", "+eachfuse.strip()
                    elif eachTitle in uniqueData[eachStation] and "page" in eachTitle:
                        if eachTitle not in ecidData[ecid]:
                            ecidData[ecid][eachTitle]=int(uniqueData[eachStation][eachTitle])
                        else:
                            ecidData[ecid][eachTitle]=int(ecidData[ecid][eachTitle]) if int(uniqueData[eachStation][eachTitle])<int(ecidData[ecid][eachTitle]) \
                                                                                   else int(uniqueData[eachStation][eachTitle])
                                                                                   
                    elif eachTitle in uniqueData[eachStation] and ("failurePartition" in eachTitle or "PSHCBEU" in eachTitle): 
                        if eachTitle not in ecidData[ecid]:
                            ecidData[ecid][eachTitle]=uniqueData[eachStation][eachTitle]
                        else:
                            ecidData[ecid][eachTitle]=ecidData[ecid][eachTitle] if uniqueData[eachStation][eachTitle] in ecidData[ecid][eachTitle] and len(ecidData[ecid][eachTitle])>250\
                                                                                   else ecidData[ecid][eachTitle]+","+uniqueData[eachStation][eachTitle]
                    elif eachTitle in uniqueData[eachStation] and "exit" in eachTitle and uniqueData[eachStation][eachTitle] is not None:
                        if eachTitle not in ecidData[ecid]:
                            ecidData[ecid][eachTitle]=uniqueData[eachStation][eachTitle]
                        elif ecidData[ecid][eachTitle] is not None:
                            ecidData[ecid][eachTitle]=ecidData[ecid][eachTitle] if uniqueData[eachStation][eachTitle] in ecidData[ecid][eachTitle] \
                                                                                   else ecidData[ecid][eachTitle]+"$"+uniqueData[eachStation][eachTitle]
                                                      
                    elif eachTitle in factoryInfo:
                        ecidData[ecid][eachTitle]=factoryInfo[eachTitle]
                    elif eachTitle in uniqueData[eachStation]:
                        ecidData[ecid][eachTitle]=uniqueData[eachStation][eachTitle]

                        #data.append(factoryInfo[eachTitle])
                    elif eachTitle=="Station":
                        data.append(eachStation)
        fulldata=[]
        #for title in self.orderTitleList:
        col=0
        row=0
        loginfoSheet.write_row(row, col, self.orderTitleList)

        for eachECID in ecidData:
            eachdata=[]
            data=[]
            row=row+1
            for title in self.orderTitleList:
                if title=="ecid":
                    data.append(eachECID)
                elif title in ecidData[eachECID]:
                    data.append(ecidData[eachECID][title])
                else:
                    data.append("")
            loginfoSheet.write_row(row, col,data)
        #logging.info(ecidData)
       # self.wk.close()
    def failureAnalysis(self,sheetName):
        row=0
        col=0
        self.getTitleList()        
        
        loginfoSheet=self.wk.add_worksheet(sheetName)
        loginfoSheet.write_row(row, col, self.orderTitleList)
        for eachlogInfo in self.loginfo:
            
            col=0
            uniqueData=eachlogInfo.uniqueData
            
            factoryInfo=eachlogInfo.factoryInfo
            #logging.debug(uniqueData)
            eachSubStationData=eachlogInfo.dataForeachSubstation
            #logging.debug(eachSubStationData)
            for eachStation in  uniqueData:
                data=[]
                #logging.info(eachStation)
                #logging.info(uniqueData[eachStation])
                if "List"  in eachStation:
                    continue
                for eachTitle in self.orderTitleList:
                    if eachTitle in uniqueData[eachStation]:
                        data.append(uniqueData[eachStation][eachTitle])
                    #elif eachTitle in eachSubStationData:
                        #data.append(eachSubStationData[eachStation][eachTitle])
                    elif eachTitle in factoryInfo:
                        data.append(factoryInfo[eachTitle])
                    elif eachTitle=="Station":
                        data.append(eachStation)
                    elif eachTitle=="TestTime":
                        if "modsEndTime" in uniqueData[eachStation]:
                            data.append(uniqueData[eachStation]["modsEndTime"])
                        elif "bgPrintCount" in uniqueData[eachStation]:
                            data.append(uniqueData[eachStation]["bgPrintCount"]*60)
                            print(uniqueData[eachStation]["bgPrintCount"])
                        elif "lastEnterTestTime" in uniqueData[eachStation] and "modsStartTime" in uniqueData[eachStation]:
                            start=datetime.datetime.strptime(uniqueData[eachStation]["modsStartTime"],"%a %b  %d %H:%M:%S %Y")
                            end=datetime.datetime.strptime(uniqueData[eachStation]["lastEnterTestTime"],"%a %b  %d %H:%M:%S %Y")
                            testTime=(end-start).seconds+(end-start).days*24*60*60
                            #print(start,testTime,testTime)
                            data.append(testTime)
                            pass
                        else:
                            data.append(0)
                    elif eachTitle=="LastErrorCode":# and "SerialNumber" in uniqueData[eachStation]:
                        lastErrorCode=self.getLastErrorCode(self.loginfo, uniqueData[eachStation],eachStation)
                        #data.append(lastErrorCode)
                        data.append("NA")
                    #elif eachTitle=="exitErroCode":
                      #  data.append(uniqueData[eachStation][eachTitle] if not ("ModsDrvBreakPoint" not in uniqueData[eachStation] or uniqueData[eachStation]["ModsDrvBreakPoint"]<5) else "ModsDriveBreakPoint")
                    else:
                        data.append(None)
                #print()
                row=row+1
                #logging.debug("write the %d row "%row)
                #logging.debug(data)
                #logging.debug(row)
            
                loginfoSheet.write_row(row,0,data)
                #self.wk.save()
       # self.wk.close()
            
    def closeWorkbook(self):
        #self.wk.save() 
        self.wk.close()                
    def getLastErrorCode(self,loginfo,dataForStation,station):
        #logging.info(station)
        #logging.info(station)
        lastErrorCode=None if "exitErroCode" not in dataForStation else dataForStation["exitErroCode"]
        logging.info("First %s"%lastErrorCode)
        if "SerialNumber" not in dataForStation:
            return lastErrorCode
        sn=dataForStation["SerialNumber"]
        lastTestTime=None
        if "lastEnterTestTime" in dataForStation:
            lastTestTime=datetime.datetime.strptime(dataForStation["lastEnterTestTime"],"%a %b  %d %H:%M:%S %Y")
        else:
            return lastErrorCode
        for eachlogInfo in loginfo:
            
            if station not in eachlogInfo.uniqueData:
                continue
            data=eachlogInfo.uniqueData[station]
            if "lastEnterTestTime" in data and "exitErroCode" in data and "SerialNumber" in data and sn==data["SerialNumber"]:
                #logging.info()
                testTime=datetime.datetime.strptime(data["lastEnterTestTime"],"%a %b  %d %H:%M:%S %Y")
                if testTime>lastTestTime:
                    lastErrorCode=data["exitErroCode"]
                    lastTestTime=testTime
        #logging.info("last%s"%lastErrorCode)
        return lastErrorCode
            
        
        #pass
        
        
                    
    def writeLoninfo(self,sheetName):
        row=0
        col=0
        self.getTitleList()        
        
        loginfoSheet=self.wk.add_worksheet("logInfo")
        loginfoSheet.write_row(row, col, self.orderTitleList)
        row+=1
        #print(len(self.loginfo))
        count=0
        for eachlogInfo in self.loginfo:
            #print(count)
            count=count+1
            col=0
            
            #if "FunctionalSpec" in eachlogInfo.logInfo and \
            uniqueData=eachlogInfo.uniqueData
            #print(uniqueData)
            eachSubStationData=eachlogInfo.dataForeachSubstation
            #logging.debug(eachSubStationData)
            logging.debug(eachlogInfo.uniqueData["filePath"])
            for eachSpec in eachSubStationData:
                data={}
                dataForEachStation=eachSubStationData[eachSpec]
                
                if True:
                    col=0
                    #print(eachSpec)
                    data["filePath"]=eachlogInfo.uniqueData["filePath"]
                    
                    #logging.debug(dataForEachStation)
                    data["SN"]=None if "SN" not in eachlogInfo.uniqueData else eachlogInfo.uniqueData["SN"]
                    data["ecid"]=None if "ecid" not in eachlogInfo.uniqueData else eachlogInfo.uniqueData["ecid"]
                    data["ateSpeedo"]=None if "ateSpeedo" not in eachlogInfo.uniqueData else eachlogInfo.uniqueData["ateSpeedo"]
                    
                    #"modsStartTime","FLATID","lastEnterTest","reboot",
                    data["modsStartTime"]=None if "modsStartTime" not in eachlogInfo.uniqueData else eachlogInfo.uniqueData["modsStartTime"]
                    data["FLATID"]=None if "FLATID" not in eachlogInfo.uniqueData else eachlogInfo.uniqueData["FLATID"]
                    data["lastEnterTest"]=None if "lastEnterTest" not in eachlogInfo.uniqueData else eachlogInfo.uniqueData["lastEnterTest"]
                    data["reboot"]=None if "reboot" not in eachlogInfo.uniqueData else eachlogInfo.uniqueData["reboot"]

                    stationName=None if "Station" not in data else data["Station"]
                    data["initNvvdd"]=None if "initNvvdd" not in eachlogInfo.uniqueData else eachlogInfo.uniqueData["initNvvdd"]
                    data["exitErroCode"]="pass" if "exitErroCode" not in  eachlogInfo.uniqueData else eachlogInfo.uniqueData["exitErroCode"]
                    data["LastErroCode"]=self.getLastErrorCode(self.loginfo, data["SN"], stationName)
                    
                    #data["subStation"]=None if "subStation" not in dataForEachStation else dataForEachStation["subStation"]
                    #print(data["subStation"])
                    data["subStation"]=eachSpec
                    data["Failure Code"]="pass" if "ErrorCode" not in dataForEachStation else dataForEachStation["ErrorCode"]
                    data["pstate"]=None if "pstate" not in dataForEachStation else dataForEachStation["pstate"]
                    data["nvvdd"]=None if "nvvdd" not in dataForEachStation else dataForEachStation["nvvdd"]
                    data["pexLaneX"]=None if "pexLane$X_STATUS" not in dataForEachStation else dataForEachStation["pexLane$X_STATUS"]
                    data["pexLaneY"]=None if "pexLane$Y_STATUS" not in dataForEachStation else dataForEachStation["pexLane$Y_STATUS"]
                    
                    data["NVLink0$X_STATUS"]=None if "NVLink0$X_STATUS" not in dataForEachStation else dataForEachStation["NVLink0$X_STATUS"]
                    data["NVLink0$Y_STATUS"]=None if "NVLink0$Y_STATUS" not in dataForEachStation else dataForEachStation["NVLink0$Y_STATUS"]
                    
                    data["NVLink1$X_STATUS"]=None if "NVLink1$X_STATUS" not in dataForEachStation else dataForEachStation["NVLink1$X_STATUS"]
                    data["NVLink1$Y_STATUS"]=None if "NVLink1$Y_STATUS" not in dataForEachStation else dataForEachStation["NVLink1$Y_STATUS"]
                    
                    data["NVLink2$X_STATUS"]=None if "NVLink2$X_STATUS" not in dataForEachStation else dataForEachStation["NVLink2$X_STATUS"]
                    data["NVLink2$Y_STATUS"]=None if "NVLink2$Y_STATUS" not in dataForEachStation else dataForEachStation["NVLink2$Y_STATUS"]
                    
                    data["NVLink3$X_STATUS"]=None if "NVLink3$X_STATUS" not in dataForEachStation else dataForEachStation["NVLink3$X_STATUS"]
                    data["NVLink3$Y_STATUS"]=None if "NVLink3$Y_STATUS" not in dataForEachStation else dataForEachStation["NVLink3$Y_STATUS"]
                    
                    data["NVLink4$X_STATUS"]=None if "NVLink4$X_STATUS" not in dataForEachStation else dataForEachStation["NVLink4$X_STATUS"]
                    data["NVLink4$Y_STATUS"]=None if "NVLink4$Y_STATUS" not in dataForEachStation else dataForEachStation["NVLink4$Y_STATUS"]
                    
                    data["NVLink5$X_STATUS"]=None if "NVLink5$X_STATUS" not in dataForEachStation else dataForEachStation["NVLink5$X_STATUS"]
                    data["NVLink5$Y_STATUS"]=None if "NVLink5$Y_STATUS" not in dataForEachStation else dataForEachStation["NVLink5$Y_STATUS"]
                    
                    #self.addPexErrorInfo(data,dataForEachStation)
                    
                    #print( data["pexLane"])
                    #data["gpuMax"]=mean(dataForEachStation["gpuMax"].split(" "))
                    if "gpuMax" in dataForEachStation:
                        try:
                            results = [float(i) for i in dataForEachStation["gpuMax"].split(" ")]
                            data["Max gpuTemp"]=round(mean(results),1)
                            data["Average gpuTemp"]=round(max(results),1)
                            results = [float(i) for i in dataForEachStation["hbm2_COMBINED_MAX"].split(" ")]
                            data["Average hbm2_COMBINED_MAX"]=round(mean(results),1)
                            data["Max hbm2_COMBINED_MAX"]=round(max(results),1)
                            #logging.debug(dataForEachStation["hbm0Temp"])
                            results = [float(i) for i in dataForEachStation["hbm0Temp"].split(" ")]
                            data["Average hbm0Temp"]=round(mean(results),1)
                            data["Max hbm0Temp"]=round(max(results),1)
                            results = [float(i) for i in dataForEachStation["hbm1Temp"].split(" ")]
                            data["Average hbm1Temp"]=round(mean(results),1)
                            data["Max hbm1Temp"]=round(max(results),1)
                            results = [float(i) for i in dataForEachStation["hbm2Temp"].split(" ")]
                            data["Average hbm2Temp"]=round(mean(results),1)
                            data["Max hbm2Temp"]=round(max(results),1)
                            results = [float(i) for i in dataForEachStation["hbm3Temp"].split(" ")]
                            data["Average hbm3Temp"]=round(mean(results),1)
                            data["Max hbm3Temp"]=round(max(results),1)
                            results = [float(i) for i in dataForEachStation["totalPowerReg"].split(" ")]
                            data["Average totalPower"]=round(mean(results),1)
                            data["Max totalPower"]=round(max(results),1)
                        except ValueError as e:
                            logging.debug(e)
                        #logging.debug(data)
                    for eachCol in self.titleList:
                        #print(len(self.titleList))
                        loginfoSheet.write(row,col,None if eachCol not in data else data[eachCol])
                        col+=1
                row+=1    
        self.wk.close()
        
    def writeHistogram(self,sheetName,col=0,row=0):
        pass
        
        station=["fct","eft","bi","fpt","sbt"]
        parameter=["INPUT_NVVDD_Max","INPUT_TOTAL_BOARD_Max","OUTPUT_NVVDD_Max","INPUT_PWR_SRC_PP_Max","gpuMaxTemp_Max","HBM2_COMBINED_MAX_Max"]
         
        parameterDict={}
         
        row=0
        col=0
         
        loginfoSheet=self.wk.add_worksheet("logInfo")
        loginfoSheet.write_row(row, col, self.orderTitleList)
        #print(len(self.loginfo))
                 
        count=0
        for eachlogInfo in self.loginfo:
            count=count+1
            col=0
            uniqueData=eachlogInfo.uniqueData
            #print(uniqueData)
            eachSubStationData=eachlogInfo.dataForeachSubstation
            #logging.debug("Histogram")
            #logging.debug(eachlogInfo.uniqueData["filePath"])
            for eachSpec in uniqueData:
                 
                if "List" in eachSpec:
                    continue
                #logging.info(uniqueData[eachSpec])
                 
                     
                for parameterName in parameter:
                     
                    logStationName = eachSpec
                    if logStationName not in parameterDict:
                        parameterDict[logStationName] = {}
                        #logging.info("add %s"%(logStationName))
                     
                    if parameterName in uniqueData[eachSpec]:
                        if parameterName not in parameterDict[logStationName]:
                             
                            parameterDict[logStationName][parameterName] = [uniqueData[eachSpec][parameterName]]
 
                        else:
                            parameterDict[logStationName][parameterName].append(uniqueData[eachSpec][parameterName])
                 
                 
        logging.info(parameterDict)        
                
        for station, parameterDict in parameterDict.items():
             
            #logging.info(station)
            #logging.info(parameterDict)
            sheetName=station+" "+"Hist"
            sheetName=sheetName if len(sheetName)<30 else sheetName[0:29]
            loginfoSheet=self.wk.add_worksheet(sheetName)
            cell_format =self.wk.add_format()
            cell_format.set_border()
            #cell_format.set_bor
            row=0
            col=0
            for orderParameterName in parameter:
 
                for parameterName, parameterValues in parameterDict.items():
                     
                    if parameterName==orderParameterName:
                         #logging.info(parameterValues)
                         hist=getDistribution(parameterValues)
                         #logging.info(hist[0])
                         #logging.info(hist[1])
                          
                         loginfoSheet.write(row,0,parameterName +" Histogram")
                         row=row+1
                         loginfoSheet.write(row,0,parameterName,cell_format)
                         loginfoSheet.write_row(row,1,hist[1],cell_format)
                         row=row+1
                         loginfoSheet.write(row,0,"Count",cell_format)
                         loginfoSheet.write_row(row,1,hist[0],cell_format)
                         row=row+1
                         loginfoSheet.write_row(row,0,["Min","Max","Average","Std Value","-3.5 sigma","+3.5 Sigma"],cell_format)
                         row=row+1
                         loginfoSheet.write_row(row,0,[min(parameterValues),max(parameterValues),mean(parameterValues),statistics.pstdev(parameterValues),
                                                       mean(parameterValues)-3.5*statistics.pstdev(parameterValues),mean(parameterValues)+3.5*statistics.pstdev(parameterValues)],cell_format)
                         if len(hist[0])+1<=26:
                             colName=str(chr(96+len(hist[0])+1))
                         else:
                             colName=str(chr(96+int(len(hist[0])/26)))+str(chr(96+len(hist[0])%26+1))
                              
                         
                         #logging.info(colName)
                          
                         chart = self.wk.add_chart({'type': 'column'})
                         colName=colName.upper()
                         #chart.add_series
                         logging.info('=\'{sheetname}\'!$B${row}:${col}${row}'.format(sheetname=sheetName,col=colName,row=row+1-2, end=len(hist[0])+1))
                         logging.info('=\'{sheetname}\'!$B${row}:${col}${row}'.format(sheetname=sheetName,col=colName,row=row-2, end=len(hist[0])+1))
                         chart.add_series({
                                               'values':     '=\'{sheetname}\'!$B${row}:${col}${row}'.format(sheetname=sheetName,col=colName,row=row+1-2, end=len(hist[0])+1),
                                               'categories': '=\'{sheetname}\'!$B${row}:${col}${row}'.format(sheetname=sheetName,col=colName,row=row-2, end=len(hist[0])+1),
                                               'gap':        2,
                                           })
                         chart.set_title({"name":parameterName +" Histogram"})
                         row=row+2
                         loginfoSheet.insert_chart(row, 4, chart)
                         row=row+20
                 
                 
                 
                 
                        
                    
        
        
    def compareLogs(self,sheetName,col=0,row=0):
        
        print("compare loginfo for two logs")
        if len(self.loginfo)!=2:
            print("Don't have 2 logs in the log info")
            return 1    
        firstLog=self.loginfo[0] if "_1" in self.loginfo[0].filePath else self.loginfo[1]
        secondLog=self.loginfo[1] if "_2" in self.loginfo[1].filePath else self.loginfo[0]
        #print(firstLog.uniqueData)
        for each in firstLog.uniqueData:
            print(each)
            if "memory" not in each and "ModsVersion" in firstLog.uniqueData[each] :
                if float(secondLog.uniqueData[each]["ModsVersion"])-float(firstLog.uniqueData[each]["ModsVersion"])<0:
                    temp=firstLog
                    firstLog=secondLog
                    secondLog=temp
            else:
                continue
        firstLogInfo=firstLog.dataForeachSubstation
        secondLog
        sheet=self.wk.add_worksheet("compare")
        cellFormat=self.wk.add_format()
        cellFormat.set_num_format("0.0")
        cellFormat.set_border()
        col=0
        tempData=["",""]
        powerData=["",""]
        #print("start ....")
        print(firstLog.uniqueData["subStationList"])
        print(secondLog.uniqueData["subStationList"])
        #print(secondLog.uniqueData)
        for orderSubStation in firstLog.uniqueData["subStationList"]:
            #print(orderSubStation)
            #for eachSpec in firstLogInfo:
             #   if orderSubStation == eachSpec:
              #      continue
                row=0 
                eachSpec=orderSubStation   
                logging.info(eachSpec)            
                sheet.write(row,col,eachSpec)
                eachSubStationData=firstLogInfo[eachSpec]
                #print(eachSubStationData)
                eachSubStationDataSecond=secondLog.dataForeachSubstation[eachSpec]
                #print(eachSubStationDataSecond)
                
                testList=None if "testList" not in eachSubStationData else eachSubStationData["testList"]
                
                if "gpuMaxTemp" in eachSubStationData:
                    logging.info(eachSubStationData["gpuMaxTemp"])
                    results = [float(i) for i in eachSubStationData["gpuMaxTemp"].split(" ")]
                    maxGputemp=round(max(results),1)
                    tempData[0]=tempData[0]+" "+eachSubStationData["gpuMaxTemp"]
                     
                    results = [float(i) for i in eachSubStationData["INPUT_TOTAL_BOARD"].split(" ")]
                    maxTotalPwr=round(max(results),1)
                    powerData[0]=powerData[0]+" "+eachSubStationData["INPUT_TOTAL_BOARD"]
                     
                     
                    results = [float(i) for i in eachSubStationDataSecond["gpuMaxTemp"].split(" ")]
                    maxGputempSec=round(max(results),1)
                    tempData[1]=tempData[1]+" "+eachSubStationDataSecond["gpuMaxTemp"]
                     
                    results = [float(i) for i in eachSubStationDataSecond["INPUT_TOTAL_BOARD"].split(" ")]
                    maxTotalPwrSec=round(max(results),1)
                    powerData[1]=powerData[1]+" "+eachSubStationDataSecond["INPUT_TOTAL_BOARD"]
                    row=row+1
                     
                    sheet.write_row(row,col,["FileName",firstLog.filePath.split(os.sep)[len(firstLog.filePath.split(os.sep))-1]],cellFormat)
                    sheet.write_row(row,col+5,["FileName",secondLog.filePath.split(os.sep)[len(secondLog.filePath.split(os.sep))-1]],cellFormat)
                    row=row+1
                     
                    sheet.write_row(row,col,["nvvdd",float(eachSubStationData["nvvdd"])],cellFormat)
                    sheet.write_row(row,col+5,["nvvdd",float(eachSubStationDataSecond["nvvdd"])],cellFormat)
                    row=row+1
                    sheet.write_row(row,col,["GpcClk",float(eachSubStationData["ClkGpc"])],cellFormat)
                    sheet.write_row(row,col+5,["GpcClk",float(eachSubStationDataSecond["ClkGpc"])],cellFormat)
                    row=row+1
         
                    sheet.write_row(row,col,["MaxGpuTemp",maxGputemp],cellFormat)
                    sheet.write_row(row,col+5,["MaxGpuTemp",maxGputempSec],cellFormat)
                    row=row+1
                    sheet.write_row(row,col,["MaxBoardTotalPwr",maxTotalPwr],cellFormat)
                    sheet.write_row(row,col+5,["MaxBoardTotalPwr",maxTotalPwrSec],cellFormat)
                     
                    row=row+1
                    sheet.write_row(row,col,["Test","ErrorCode","Test Parameter&&Result","Test Time"],cellFormat)
                    sheet.write_row(row,col+5,["Test","ErrorCode","Test Parameter&&Result","Test Time"],cellFormat)
                    row=row+1
                if testList is None:
                    continue
                secondTestList=secondLog.dataForeachSubstation[eachSpec]["testList"]
                print(secondTestList)
                print(testList)
                totalTimeDiff=0
                
                '''summary the tests which are removed in the new version diag'''
                for eachTest in testList:
                    secondEachTest="N/A$N/A$N/A$" if self.testExist(eachTest, secondTestList) is False else self.testExist(eachTest, secondTestList)
                    if self.testExist(eachTest, secondTestList):
                        secondTestList.remove(secondEachTest)
                        totalTimeDiff=totalTimeDiff+float(secondEachTest.split("$")[3])-float(eachTest.split("$")[3])
#                         sheet.write_row(row,col,eachTest.split("$"),cellFormat)
#                         sheet.write(row,col+4,"--->>>",cellFormat)
#                         sheet.write_row(row,col+5,secondEachTest.split("$"),cellFormat)
#                         sheet.write(1,col+9,totalTimeDiff,cellFormat)
#                         row+=1
                    else:
                        totalTimeDiff=totalTimeDiff-float(eachTest.split("$")[3])
                        sheet.write_row(row,col,eachTest.split("$"),cellFormat)
                        sheet.write(row,col+4,"--->>>",cellFormat)
                        sheet.write_row(row,col+5,secondEachTest.split("$"),cellFormat)
                        sheet.write(1,col+9,totalTimeDiff,cellFormat)
                        row+=1
                        print(eachTest)
                '''summary the tests which are added in the new version diag''' 
                secondTestList=secondLog.dataForeachSubstation[eachSpec]["testList"]  
                for eachTest in secondTestList:
                    secondEachTest="N/A$N/A$N/A$" if self.testExist(eachTest, testList) is False else self.testExist(eachTest, testList)
                    if self.testExist(eachTest, testList):
                        testList.remove(secondEachTest)
                        totalTimeDiff=totalTimeDiff+float(secondEachTest.split("$")[3])-float(eachTest.split("$")[3])
                    else:
                        totalTimeDiff=totalTimeDiff-float(eachTest.split("$")[3])
                        sheet.write_row(row,col+5,eachTest.split("$"),cellFormat)
                        sheet.write(row,col+4,"<<<---",cellFormat)
                        sheet.write_row(row,col,secondEachTest.split("$"),cellFormat)
                        #sheet.write(1,col+9,totalTimeDiff,cellFormat)
                        row+=1
                    #sheet.wr
                    #print(eachTest)
                col+=10
                #break
        dataSheet=self.wk.add_worksheet("pwrTemp")
        dataSheet.write_row(0,0,["FileName",firstLog.filePath.split(os.sep)[len(firstLog.filePath.split(os.sep))-1]],cellFormat)

        dataSheet.write(1,1,"temperature")
        temp0data=tempData[0]
        dataSheet.write_column(2,1,self.getDataFromStr(temp0data))
        dataSheet.write(1,2,"MaxTotalPwr")
        

        dataSheet.write_column(2,2,self.getDataFromStr(powerData[0]))
        chartTemp=self.wk.add_chart({'type':'line'})
        #print('=pwrTemp!$A$%2:$A1$LHX$1'%(len(temp0data)))
        chartTemp.add_series({'values':'=pwrTemp!$B$3:$B$%d'%(len(self.getDataFromStr(temp0data)))})
        
        dataSheet.write_row(0,3,["FileName",secondLog.filePath.split(os.sep)[len(secondLog.filePath.split(os.sep))-1]],cellFormat)
        dataSheet.write(1,3,"temperature")
        dataSheet.write_column(2,3,self.getDataFromStr(tempData[1]))
        dataSheet.write(1,4,"MaxTotalPwr")
        dataSheet.write_column(2,4,self.getDataFromStr(powerData[1]))
        dataSheet.insert_chart(10, 5, chartTemp)
        
        ###############################################################
        
#         cmdResult=compareCmdLine(firstLog.factoryInfo["commandLine"], secondLog.factoryInfo["commandLine"])
#         
#         cmdSheet=self.wk.add_worksheet("Command Line Diff")
#         
#         row=0
#         for key,value in cmdResult.items():
#             cmdSheet.write(row, 0,key)
#             cmdSheet.write_row(row, 1,value)
#             row=row+1
        
        self.wk.close()
    def getDataFromStr(self,data):
        if data is None:
            return None
        #logging.info(data)
        splitData=data.split(" ")
        
        result=[]
        for each in splitData:
            try:
                temp=float(each)
                result.append(temp)
            except ValueError as e:
                print(e)
                print(each)
        #print(result)
        return result
    def testExist(self,testName,testList):
        actualName=testName.split("$")[0]+testName.split("$")[2]
        if len(testList)<1:
            return False
        for each in testList:
            if actualName==each.split("$")[0]+each.split("$")[2]:
                #print("find tests %s"%(actualName))
                return each 
        return False
                
