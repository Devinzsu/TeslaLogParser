import re
import logging
import numpy

def getDistribution(parameterValues):
    
    maxValue=max(parameterValues)
    minValue=min(parameterValues)
    binValue=30
    #numpy.histogram(a, bins, range, normed, weights, density)
    
    #logging.info("Min Value %s"%(minValue))
    #logging.info("Max Value %s"%(maxValue))
    #logging.info("Bin Value %s"%(binValue))
    
    counts,bins=numpy.histogram(parameterValues, binValue, range=(minValue,maxValue)) 
    #print(len(bins))
    #for i in range(len(bins)):
        
       # bins[i]=bins[i]+minValue+binValue*i
    countsArray=counts.tolist()
    binsArray=bins.tolist()
    resultCountList=[]
    resultBinList=[]
    for index in range(len(countsArray)):
        #logging.info(index)
        if countsArray[index]==0:
            #countsArray.pop(index)
            #binsArray.pop(index)
            pass
        else:
            #binsArray[index]=round(binsArray[index],1)
            resultBinList.append(round(binsArray[index],1))
            resultCountList.append(round(countsArray[index],1))
    
    
    return [resultCountList,resultBinList]
    
    
    

def getMaxDataFromString(data):
    
    #logging.info(result)
    if data is None:
        return None
        #print(data)
    splitData=data.split(" ")
    
    result=[]
    for each in splitData:
        try:
            temp=float(each)
            result.append(temp)
        except ValueError as e:
            print(e)
            print(each)
    #logging.info(result)
    return max(result)
def getMinDataFromString(data):
    
    #logging.info(result)
    if data is None:
        return None
        #print(data)
    splitData=data.split(" ")
    
    result=[]
    for each in splitData:
        try:
            temp=float(each)
            result.append(temp)
        except ValueError as e:
            print(e)
            print(each)
    #logging.info(result)
    return min(result)
def isNumber(hbmtemp):
    hbmtemp=hbmtemp.strip()
    hbmtempNum=[]
    for each in hbmtemp.split(" "):
        
        try:
            float(each)
            hbmtempNum.append(float(each))
        except ValueError:
            return False
    return hbmtempNum
        
def getHBMTempDelta(original,hbm0,hbm1):
    
    if not (isNumber(hbm0) and isNumber(hbm1)):
        
        return original
    hbm0Num=isNumber(hbm0)
    hbm1Num=isNumber(hbm1)
    originalNum=isNumber(original)
    hbm01=[]
    count=0
    sum=originalNum[3]
    #logging.info(hbm1Num)
    
    for each in hbm0Num:
        #max=each-hbm1Num[count] if abs(number)
        hbm01.append(each-hbm1Num[count])
        originalNum[2]+=1
        originalNum[3]=originalNum[3]+each-hbm1Num[count]
        count+=1
    #hbm01=map(lambda x,y:x - y,hbm0Num,hbm1Num)
    
    returnValue=str(min(hbm01) if originalNum[0]>min(hbm01) else originalNum[0])+" "+str(max(hbm01) if originalNum[1]<max(hbm01) else originalNum[1])
#     if original.split(" ")[0]!=returnValue.split(" ")[0] or original.split(" ")[1]!=returnValue.split(" ")[1]:
#         logging.info("max %s, Min %s  "%(max(hbm01),min(hbm01)))
#         logging.info("orginal value %s "%(original))
#         logging.info("New value %s "%(returnValue))
#         logging.info("hbm0 value %s "%(hbm0))
#         logging.info("hbm1 value %s "%(hbm1))
        #print()
    return returnValue+ " "+str(originalNum[2])+" "+ str(originalNum[3]) #str(min(hbm01) if original[0]>min(hbm01) else original[0])+" "+str(max(hbm01) if original[1]<max(hbm01) else original[1])
        
    