import re
import logging

compileRe={}

compileRe["nvvdd"]=[re.compile("NVVDD\s+=\s+(?P<data>.+)\s+mV",re.IGNORECASE)]
compileRe["ClkGpc"]=[re.compile("ClkGpc\s+=\s+(?P<data>.+)\s+MHz",re.IGNORECASE)]





getDataforSubStation=True

compileRe["ExitCode"]=[   re.compile("Exit\s+(?P<errorCode>\d+)\s+:\s+(?P<testName>.+)\s+\(test\s+(?P<testNumber>.+)\)\s+\[virtual\s+test\s+id\s+(?P<testID>.+)\]\s+(?P<errorDescript>.+)\s+\[(?P<exitTime>\d+\.\d+)\s+seconds\]")
                               ]
compileRe["ExitCode"].append(re.compile("Exit\s+(?P<errorCode>\d+)\s+:\s+(?P<testName>.+)\s+\(test\s+(?P<testNumber>.+)\)\s+(?P<errorDescript>.+)\s+\[(?P<exitTime>\d+\.\d+)\s+seconds\]")
                                  )
compileRe["ExitCode"].append(re.compile("Error\s+(?P<errorCode>\d+)\s+:\s*(?P<testName>.+)\s*(?P<errorDescript>.+?)\s*\[(?P<exitTime>\d+\.\d+)\s+seconds\]"))
compileRe["ModsDrvBreakPoint"]=[re.compile("\*\*\s+ModsDrvBreakPoint\s+\*\*",re.IGNORECASE)]
compileRe["Gflops"]=[re.compile("GFLOPS\s+=\s+(?P<data>.+)", re.IGNORECASE)]
#New FB SBE at PhysAddr=0x0037b96408 FBIO=M Subpart=0 HbmSite=3 HbmChan=2 PseudoCh=1 Bank=9 Row=37b Col=30 Beat=1 BtOffset=0

compileRe["ECCFailure"]=[re.compile("New\s+FB\s+(SBE)?(DBE)?\s+at\s+PhysAddr=(?P<physAddr>\w+)\s+FBIO=(?P<partition>\w+)\s+Subpart=(?P<subpart>\w+)\s+HbmSite=(?P<hbmsite>\w+)\s+\
HbmChan=(?P<hbmchan>\w+)\s+PseudoCh=(?P<pseudoCh>\w+)\s?(StackID=0)?(StackID=1)?\s+Bank=(?P<bank>\w+)\s+Row=(?P<row>\w+)\s+Col=(?P<col>\w+)\s+Beat=(?P<beat>\w+)\s+BtOffset=(?P<btoffset>\w+)", re.IGNORECASE)]
#Fusing siteID 0, stackID 0, channel 2, bank 12, row 425

compileRe["fusedAddr"]=[re.compile("Fusing\s+siteID\s+(?P<site>\w+),\s+stackID\s+(?P<stackID>\w+),\s+channel\s+(?P<channel>\w+),\s+bank\s+(?P<bank>\w+),\s+row\s+(?P<row>\w+)", re.IGNORECASE)]
#ERROR: ADC_GPC4 mean sampled code (24.433) differs from expected (27) @ nvvdd=618750 uV
#Blacklisted Pages: 4
compileRe["pageRetirements"]=[re.compile("Blacklisted\s+Pages:\s+(?P<data>\d+)", re.IGNORECASE)]
#compileRe["AdcError"]=[re.compile("ERROR:\s+(?P<GPC>\w+)\s+mean\s+sampled\s+code\s+\((?P<readCode>.+)\)\s+differs\s+from\s+expected\s+\((?P<expectCode>.+)\)\s+@\s+nvvdd=(?P<nvvdd>\d+)\s+uV", re.IGNORECASE)]
compileRe["failurePartition"]=[re.compile("in\s+partition\s+(?P<partition>\w+),\s+subpartition\s+(?P<subpartition>\d+)", re.IGNORECASE)]##for cudalinpack test which didn't report new FB ****
#001d81df1c f1eb4e56 f1eb4e57 G111431 01d8 028   G224 000000000000e454   7    57    84   F   2
compileRe["memoryfaildetails"]=[re.compile("\s+(?P<PSHCBEU>([A-Z]){1,2}(\w){4,5}(\d){2,3})\s+(?P<row>\w{4})\s+(?P<col>\w{3})\s+(?P<bits>[A-Z]{1}\w{4,12})", re.IGNORECASE)]##for cudalinpack test which didn't report new FB ****
#HBM Site Info  : Year/Week/Loc/Serial#/Part#              
#HBM Site 0     : 2018/01/0x9/0x2408e70aa/0x21             
#HBM Site 1     : 2018/01/0x9/0x2408e732a/0x21             
#HBM Site 2     : 2018/01/0x9/0x2408e7352/0x21             
#HBM Site 3     : 2018/01/0x9/0x2408e7752/0x21  
compileRe["hbmsite"]=[re.compile("Device\s+Id\s+Data\s+for\s+Site\s+(?P<hbmsite>\d+)", re.IGNORECASE),re.compile("Manfucturing\s+Year\s+:\s+(?P<hbm_wy>\d+)", re.IGNORECASE),
                      re.compile("Manfucturing\s+Week\s+:\s+(?P<hbm_ww>\d+)", re.IGNORECASE),re.compile("HBM\s+Site\s+(?P<hbmsite>\d+)\s+:\s+(?P<hbm_wy>\d+)/(?P<hbm_ww>\d+)/(?P<hbm_sn>\w+)/(?P<hbm_lot>\w+)", re.IGNORECASE)]


compileRe["PEXLanesXStatus"]=[re.compile("GPU\s+0\s+.+:\s+PEX\s+Lane\(0\-15\)\s+X_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]

compileRe["PEXLanesYStatus"]=[re.compile("GPU\s+0\s+.+:\s+PEX\s+Lane\(0\-15\)\s+Y_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
#compileRe["T148Failure"]=[re.compile("ERROR:\s+\(Loop\s+(?P<data>\d+)\)",re.IGNORECASE)]
#ERROR: (Loop 88)


# compileRe["local_Correctable"]=[re.compile("Local\s+Correctable\s+=\s+(?P<data>\d+)")]
# 
# compileRe["host_Correctable"]=[re.compile("Host\s+Correctable\s+=\s+(?P<data>\d+)")]
# compileRe["local_none_fatal"]=[re.compile("Local\s+Non-Fatal\s+=\s+(?P<data>\d+)")]
# compileRe["host_none_fatal"]=[re.compile("Host\s+Non-Fatal\s+=\s+(?P<data>\d+)")]
# compileRe["local_fatal"]=[re.compile("Local\s+Fatal\s+=\s+(?P<data>\d+)")]
# compileRe["host_fatal"]=[re.compile("Host\s+Fatal\s+=\s+(?P<data>\d+)")]
# compileRe["local_unsupported_request"]=[re.compile("Local\s+Unsupported\s+Request\s+=\s+(?P<data>\d+)")]
# compileRe["host_unsupported_request"]=[re.compile("Host\s+Unsupported\s+Request\s+=\s+(?P<data>\d+)")]
# 
# compileRe["local_lineErrors"]=[re.compile("Local\s+LineErrors\s+=\s+(?P<data>\d+)")]
# compileRe["local_CRCErrors"]=[re.compile("Local\s+CRCErrors\s+=\s+(?P<data>\d+)")]
# 
# compileRe["local_NAKs_received"]=[re.compile("Local\s+NAKs\s+Received\s+=\s+(?P<data>\d+)")]
# compileRe["local_NAKs_received"]=[re.compile("Local\s+NAKs\s+Received\s+=\s+(?P<data>\d+)")]
# 
# compileRe["local_failedL0sExits"]=[re.compile("Local\s+FailedL0sExits\s+=\s+(?P<data>\d+)")]
# compileRe["local_NAKs_sent"]=[re.compile("Local\s+NAKs\s+Sent\s+=\s+(?P<data>\d+)")]

compileRe["NVLink0X"]=[re.compile("GPU\s+0\s+.+:\s+NVLink0.+Lane\(0\-7\)\s+X_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink0Y"]=[re.compile("GPU\s+0\s+.+:\s+NVLink0.+Lane\(0\-7\)\s+Y_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink1X"]=[re.compile("GPU\s+0\s+.+:\s+NVLink1.+Lane\(0\-7\)\s+X_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink1Y"]=[re.compile("GPU\s+0\s+.+:\s+NVLink1.+Lane\(0\-7\)\s+Y_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink2X"]=[re.compile("GPU\s+0\s+.+:\s+NVLink2.+Lane\(0\-7\)\s+X_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink2Y"]=[re.compile("GPU\s+0\s+.+:\s+NVLink2.+Lane\(0\-7\)\s+Y_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink3X"]=[re.compile("GPU\s+0\s+.+:\s+NVLink3.+Lane\(0\-7\)\s+X_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink3Y"]=[re.compile("GPU\s+0\s+.+:\s+NVLink3.+Lane\(0\-7\)\s+Y_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink4X"]=[re.compile("GPU\s+0\s+.+:\s+NVLink4.+Lane\(0\-7\)\s+X_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink4Y"]=[re.compile("GPU\s+0\s+.+:\s+NVLink4.+Lane\(0\-7\)\s+Y_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink5X"]=[re.compile("GPU\s+0\s+.+:\s+NVLink5.+Lane\(0\-7\)\s+X_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]
compileRe["NVLink5Y"]=[re.compile("GPU\s+0\s+.+:\s+NVLink5.+Lane\(0\-7\)\s+Y_STATUS\s+=\s+(?P<data>.+)",re.IGNORECASE)]


'''
Enter CudaLinpackDgemm.Run (test 199) [virtual test id 199-b] {Nsize=512, Ksize=8192} Thu Oct  5 07:05:09 2017
Exit 000000000000 : CudaLinpackDgemm.Run (test 199) [virtual test id 199-g] {Nsize=384, Ksize=616} ok [312.027 seconds]

Enter JsGpuTest.CudaMatsPatCombi (test 144) Thu Oct  5 04:22:32 2017
Exit 000000000000 : NewWfMatsTest.WfMatsMedium (test 118) ok [222.095 seconds]

'''
compileRe["EnterTest"]=[
                        re.compile("Enter\s+(?P<testName>.+)\s+\(test\s+(?P<testNumber>\d{1,4})\)\s+(?P<virtualID>\[.+\]\s+\{.+\})\s+(?P<enterTime>.+)",re.IGNORECASE),
                        re.compile("Enter\s+(?P<testName>.+)\s+\(test\s+(?P<testNumber>\d{1,4})\)\s+(?P<virtualID>\[.+\])\s+(?P<enterTime>.+)",re.IGNORECASE),
                        re.compile("Enter\s+(?P<testName>.+)\s+\(test\s+(?P<testNumber>\d{1,4})\)\s+\[.+\]\s+(?P<enterTime>.+)",re.IGNORECASE),
                        re.compile("Enter\s+(?P<testName>.+)\s+\(test\s+(?P<testNumber>\d{1,4})\)\s+\{.+\}\s+(?P<enterTime>.+)",re.IGNORECASE),

                        re.compile("Enter\s+(?P<testName>.+)\s+\(test\s+(?P<testNumber>\d{1,4})\)\s+(?P<enterTime>.+)",re.IGNORECASE),
                        ]

def addHBMFailure(logInfoResult,site,partition,bits,row,col):
    
    partition=partition.lower()
    if site is None and partition is None:
        return False
    
    site=str(site if site is not None else int((ord(partition)-ord('a'))/4))
    if "failuresite" not in logInfoResult:
        logInfoResult["failuresite"]=site  
    else: 
        logInfoResult["failuresite"]=logInfoResult["failuresite"] if site in  logInfoResult["failuresite"] else logInfoResult["failuresite"]+","+site
    
    if col is None and row is None:
        col="NA"
        row="NA"    
    if "ecid" in logInfoResult:
        #logging.info(site)
        ecid=logInfoResult["ecid"]
        if "site"+site+"Col" not in logInfoResult:
            logInfoResult["site"+site+"Col"]=col
            #databyECID[logInfoResult[currentStation]["ecid"]]["site"+site+"Col"]=result.group("col")
        elif "site"+site+"Col" in logInfoResult:# and result.group("col") not in databyECID[logInfoResult[currentStation]["ecid"]]["site"+site+"Col"]:
           # databyECID[logInfoResult["ecid"]]["site"+site+"Col"]= databyECID[logInfoResult["ecid"]]["site"+site+"Col"]+", "+result.group("col")
            logInfoResult["site"+site+"Col"]= logInfoResult["site"+site+"Col"]+", "+col if col not in logInfoResult["site"+site+"Col"] else logInfoResult["site"+site+"Col"]
        
        if "site"+site+"Row" not in logInfoResult:                                                  
            #databyECID[logInfoResult[currentStation]["ecid"]]["site"+site+"Row"]=result.group("row")
            logInfoResult["site"+site+"Row"]=row
        elif "site"+site+"Row" in  logInfoResult:# and  result.group("row") not in databyECID[logInfoResult[currentStation]["ecid"]]["site"+site+"Row"]:
            #databyECID[logInfoResult["ecid"]]["site"+site+"Row"]=databyECID[logInfoResult["ecid"]]["site"+site+"Row"]+", "+result.group("row")
            logInfoResult["site"+site+"Row"]=logInfoResult["site"+site+"Row"]+", "+row if row not in logInfoResult["site"+site+"Row"] else logInfoResult["site"+site+"Row"]

    
    
def getTestName(testList,testName):
    if testList is None:
        return testName
    
    test_suffix=0
    
    #logging.info(testName)
    tempName=testName+"_"+str(test_suffix)
    while(tempName in testList):
        test_suffix=test_suffix+1
        tempName=testName+"_"+str(test_suffix)

    #logging.info("new test Name %s, old name is %s"%(tempName,testName))
    #logging.info(testName+"_"+str(test_suffix))
    return tempName
        


def parseTestInfo(line,logInfoResult,logInfoForSubstation,databyECID,currentStation,currentSubstation):
    
    #if substation=="":
        #return
    
    #lastEnterTest=""
    if  currentStation==None:
        return False
    if "exitErroCode" in logInfoResult[currentStation] and logInfoResult[currentStation]["exitErroCode"]=="ModsDrvBreakPoint":
        
        return True
    
    if currentSubstation==None:
        currentSubstation=currentStation
        if currentSubstation not in logInfoForSubstation:
            logInfoForSubstation[currentSubstation]={}
    logInfoResult[currentStation]["lastStation"]=currentSubstation
    if "ecid" in logInfoResult and logInfoResult["ecid"] not in databyECID:
        
        databyECID[logInfoResult["ecid"]]={}
        
    for key, eachRegexList in compileRe.items():
        
        findflg=False
        for eachRegex in eachRegexList:
            result=eachRegex.search(line)
            #logging.info(currentSubstation)
            if result is not None:                        
                
                if (key=="nvvdd" or key=="ClkGpc") and currentSubstation!=None:
                    if currentSubstation not in logInfoForSubstation:
                        logInfoForSubstation[currentSubstation]={}
                    logInfoForSubstation[currentSubstation][key]=result.group("data")
                    #logging.info(result.group("data"))
                
                if key=="EnterTest":
                    try:                        
                        name=result.group("testName")+"$"+result.group("testNumber")+"$"+result.group("virtualID")
                    except IndexError as e: 
                        name=result.group("testName")+"$"+result.group("testNumber")
                    
                    logInfoResult[currentStation]["lastEnterTest"]=name
                    logInfoResult[currentStation]["lastEnterTestNumber"]=result.group("testNumber")
                    logInfoResult[currentStation]["lastStation"]=currentStation
                    logInfoResult[currentStation]["lastEnterTestTime"]=result.group("enterTime")
                #logging.info(key)
                elif key=="failurePartition":
                    partitionName=result.group("partition")
                    addHBMFailure(logInfoResult[currentStation], None, partitionName, None, None, None)
                    #logging.info(partitionName)
                    if "failurePartition" not in logInfoResult[currentStation]:
                    
                        logInfoResult[currentStation]["failurePartition"]=partitionName
                    else:
                        logInfoResult[currentStation]["failurePartition"]=logInfoResult[currentStation]["failurePartition"]+partitionName if partitionName not in logInfoResult[currentStation]["failurePartition"] else logInfoResult[currentStation]["failurePartition"]
                    #logging.info(result.group("enterTime"))
                elif key=="memoryfaildetails":
                    #logging.info(line)
                    logging.info(result.group("PSHCBEU"))
                    #logging.info(result.group("PSHCBEU")[0:2])
                    partitionName=result.group("PSHCBEU")[0]
                    logging.info(partitionName)
                    #site=result.group("PSHCBEU")[len(result.group("PSHCBEU"))-6]
                    addHBMFailure(logInfoResult[currentStation],None,partitionName,None,result.group("row"),result.group("col"))
                    logInfoResult[currentStation]["PSHCBEU"]=result.group("PSHCBEU") if "PSHCBEU" not in logInfoResult[currentStation] else logInfoResult[currentStation]["PSHCBEU"]+","+result.group("PSHCBEU")
                    
                    if "failurePartition" not in logInfoResult[currentStation]:
                        logInfoResult[currentStation]["failurePartition"]=partitionName
                    else:
                        logInfoResult[currentStation]["failurePartition"]=logInfoResult[currentStation]["failurePartition"]+partitionName if partitionName not in logInfoResult[currentStation]["failurePartition"] else logInfoResult[currentStation]["failurePartition"]
                    #logging.info(result.group("enterTime"))
                elif key=="Gflops":
                    name=currentStation+"_"+logInfoResult[currentStation]["lastEnterTest"]+"_"+"fptGflops"
                    logInfoResult[currentStation][name]=result.group("data")
                elif key=="ExitCode":
                    
                    re_resultdict=result.groupdict()
                    testID="NA" if "testID" not in re_resultdict else re_resultdict["testID"]
                    testNumber="NA$" if "testNumber" not in re_resultdict else re_resultdict["testNumber"]+"$"
                    testList=None if "testList1" not in logInfoForSubstation[currentSubstation] else logInfoForSubstation[currentSubstation]["testList1"]
                    #if "testList1" in logInfoForSubstation[currentSubstation]:
                        #logging.info(logInfoForSubstation[currentSubstation]["testList1"])
                    testName=re_resultdict["testName"]+"$"+testNumber+testID
                    testNumer_wIndex=getTestName(testList, testName)
                    
                    failureCode=result.group("errorCode")
                    try:                        
                        name=result.group("testName")+"$"+result.group("testNumber")+"$"+result.group("errorCode")+"$"+result.group("errorDescript")+"$"+result.group("exitTime")
                    except IndexError as e: 
                        name=result.group("testName")+"$"+"TestNumber NA"+"$"+result.group("errorCode")+"$"+result.group("errorDescript")+"$"+result.group("exitTime")
                     
                    try:    

                        exitTestInfo=result.group("testNumber")+"$"+result.group("errorCode")+"$"+result.group("errorDescript")+"$"+result.group("exitTime")
                    except IndexError:
                        exitTestInfo="NA"+"$"+result.group("errorCode")+"$"+result.group("errorDescript")+"$"+result.group("exitTime")
                    #getTestName()
                    if getDataforSubStation and currentSubstation!=None and "Exit" in line:          
                        if "testList" not in logInfoForSubstation[currentSubstation]:
                            logInfoForSubstation[currentSubstation]["testList1"]=[testNumer_wIndex]
                            logInfoForSubstation[currentSubstation]["testList"]=[exitTestInfo]
                            
                        else:
                            logInfoForSubstation[currentSubstation]["testList"].append(exitTestInfo)
                            logInfoForSubstation[currentSubstation]["testList1"].append(testNumer_wIndex)
                    
                    if int(result.group("errorCode"))>0:
                        
                        testNameTemp=""
                        
                        if "139" in result.group("errorCode") and "bgPrintCount" in logInfoResult[currentStation] and "EC139FailTime" not in logInfoResult[currentStation]:
                            #logInfoResult[currentStation]["EC139FailTime"]=logInfoResult[currentStation]["bgPrintCount"]
                            #logging.info(logInfoResult[currentStation]["EC139FailTime"])
                            #logging.info("")
                            pass
                        #logging.info(self.factoryInfo["filePath"])    
                        #logging.info(re_resultdict)
                        
                       
                        
                        logInfoResult[currentStation][testNameTemp+"FailureTestTime"]=result.group("exitTime")

                        if "Failure Details" not in logInfoResult[currentStation]:
                            logInfoResult[currentStation]["Failure Details"]=currentSubstation+"$"+testNumer_wIndex+"$"+failureCode
                        else:
                            logInfoResult[currentStation]["Failure Details"]=logInfoResult[currentStation]["Failure Details"]+"$$"+currentSubstation+"$"+testNumer_wIndex+"$"+failureCode if currentSubstation+"$"+testNumer_wIndex+"$"+failureCode not in logInfoResult[currentStation]["Failure Details"] else logInfoResult[currentStation]["Failure Details"]
                        codeName=result.group("errorCode")
                        
                        if "gpuMaxTemplastMin" in logInfoResult[currentStation]:
                            #codeName=codeName+"#GPUMax "+str(logInfoResult[currentStation]["gpuMaxTemplastMin"])
                            logInfoResult[currentStation][codeName+"GpuMaxByCode"]=logInfoResult[currentStation]["gpuMaxTemplastMin"]
                        if "hbm2_COMBINED_MAX_TemplastMin" in logInfoResult[currentStation]:
                            #codeName=codeName+"#hbm2_COMBINED_MAX_Temp "+str(logInfoResult[currentStation]["hbm2_COMBINED_MAX_TemplastMin"])
                            logInfoResult[currentStation][codeName+"HBMComeBinedByCode"]=logInfoResult[currentStation]["hbm2_COMBINED_MAX_TemplastMin"]
                        if "totalPowerReg_PWRlastMin" in logInfoResult[currentStation]:
                            #codeName=codeName+"#totalPowerReg_PWR "+str(logInfoResult[currentStation]["totalPowerReg_PWRlastMin"])
                            logInfoResult[currentStation][codeName+"TotalPowerByCode"]=logInfoResult[currentStation]["totalPowerReg_PWRlastMin"]
                        
                        if "Failure Code" not in logInfoResult[currentStation]:
                            logInfoResult[currentStation]["Failure Code"]=codeName
                        else:
                            
                            logInfoResult[currentStation]["Failure Code"]=logInfoResult[currentStation]["Failure Code"]+"$"+codeName if codeName not in logInfoResult[currentStation]["Failure Code"] else logInfoResult[currentStation]["Failure Code"] 
                elif key=="ModsDrvBreakPoint":
                    logInfoResult[currentStation][key]=0 if key not in logInfoResult[currentStation] else logInfoResult[currentStation][key]+1
                    if logInfoResult[currentStation][key]>=2:
                        logInfoResult[currentStation]["exitErroCode"]="ModsDrvBreakPoint"
                elif "local" in key or "host" in key:
                    logging.info(key)
                    logInfoResult[currentStation][key]=int(result.group("data")) if key  not in logInfoResult[currentStation] else int(result.group("data"))+logInfoResult[currentStation][key]
                elif key=="AdcError":
                    
                    logInfoResult[currentStation][key]=result.group("GPC")+"@"+result.group("readCode")+"@"+result.group("expectCode")+"@"+result.group("nvvdd") if key not in logInfoResult[currentStation] else logInfoResult[currentStation][key]+"$"+result.group("GPC")+"@"+result.group("readCode")+"@"+result.group("expectCode")+"@"+result.group("nvvdd")
                    keyName=key+result.group("GPC")
                    
                    if keyName not in  logInfoResult[currentStation]:
                        logInfoResult[currentStation][keyName+"readCode"]=result.group("readCode")
                        logInfoResult[currentStation][keyName+"expectCode"]=result.group("expectCode")
                        logInfoResult[currentStation][keyName+"nvvdd"]=result.group("nvvdd")
                    
                    #logging.info(logInfoResult[currentStation][key])
                elif key=="ECCFailure":
                    site=result.group("hbmsite")
                    
                    addHBMFailure(logInfoResult[currentStation],result.group("hbmsite"),result.group("partition"),None, result.group("row"), result.group("col"))
                    
                    
                                        #logInfoResult[currentStation]["site"+site+"Col"]=result.group("col") if "site"+site+"Col" not in logInfoResult[currentStation] else logInfoResult[currentStation]["site"+site+"Col"]+", "+result.group("col")
                    #logInfoResult[currentStation]["site"+site+"Row"]=result.group("row") if "site"+site+"Row" not in logInfoResult[currentStation] else logInfoResult[currentStation]["site"+site+"Row"]+", "+result.group("row")
                    #logging.info(logInfoResult[currentStation]["site"+site+"Col"])
                elif key=="fusedAddr":
                    fuseAddr="site"+result.group("site")+"channel"+result.group("channel")+"bank"+result.group("bank")+"row"+result.group("row")
                   # logging.info(fuseAddr)
                    if "ecid" in logInfoResult:
                        if key  not in databyECID[logInfoResult["ecid"]]:
                            databyECID[logInfoResult["ecid"]][key]=fuseAddr
                        elif  fuseAddr not in databyECID[logInfoResult["ecid"]][key]:
                            databyECID[logInfoResult["ecid"]][key]=databyECID[logInfoResult["ecid"]][key]+", "+fuseAddr
                    logInfoResult[currentStation][key]="site"+result.group("site")+"channel"+result.group("channel")+"bank"+result.group("bank")+"row"+result.group("row") if key not in logInfoResult[currentStation] else  logInfoResult[currentStation][key]+" ,"+fuseAddr   
                elif key=="pageRetirements":
                    if key not in logInfoResult[currentStation]:
                        logInfoResult[currentStation][key]=int(result.group("data"))
                    else:
                        logInfoResult[currentStation][key]=int(result.group("data")) if int(result.group("data"))> logInfoResult[currentStation][key] else  logInfoResult[currentStation][key]
                    if key not in databyECID:
                        databyECID[key]=int(result.group("data"))
                    else:
                        databyECID[key]=int(result.group("data")) if int(result.group("data"))> databyECID[key] else databyECID[key]

                elif key=="hbmsite":
                    
                    searchResult=result.groupdict()
                    
                    if "hbmsite" in searchResult:
                        logInfoResult[currentStation]["Currentsite_number_HBMInfo"]="site"+searchResult["hbmsite"]+"_WW"
                        #logInfoResult[currentStation]["site"+result.group("data")+"_WW"]=""
                    if "hbm_wy" in searchResult:
                        site=logInfoResult[currentStation]["Currentsite_number_HBMInfo"]
                        logInfoResult[currentStation][site]=searchResult["hbm_wy"] if site not in logInfoResult[currentStation] else logInfoResult[currentStation][site]+"_WW"+searchResult["hbm_wy"]
                    if "hbm_ww" in searchResult:
                        site=logInfoResult[currentStation]["Currentsite_number_HBMInfo"]
                        logInfoResult[currentStation][site]=searchResult["hbm_ww"] if site not in logInfoResult[currentStation] else logInfoResult[currentStation][site]+"_WW"+searchResult["hbm_ww"]

                    #if "Device" in line:
                        #logInfoResult[currentStation]["Currentsite_number_HBMInfo"]="site"+result.group("data")+"_WW"
                    #else:
                       # site=logInfoResult[currentStation]["Currentsite_number_HBMInfo"]
                        #logInfoResult[currentStation][site]=result.group("data") if site not in logInfoResult[currentStation] else logInfoResult[currentStation][site]+"_WW"+result.group("data")
                        #logging.info(logInfoResult[currentStation][site])
                else:
                    logInfoResult[currentStation][key]=result.group("data")
                    #logging.info(result.group("data"))
                return True
    return False
