import os
import zipfile
import shutil

import subprocess
from shutil import _ntuple_diskusage


def addItemtoDict_string(dict, keywords,item):
    
    if keywords not in dict:
        dict[keywords]=item
    elif item in dict[keywords]:
        return dict
    else:
        dict[keywords]=dict[keywords]+item
    return 
        

def workThroughDir(path,append):
    ################
    '''
    this function will return all the file in a given directory with given file format like ".log" ".mle"
    '''    
    #######################3
    
    sep=os.sep
    filePaths=[]
    if not os.path.exists(path):
        return None
    for rt,dirs,files in os.walk(path):
        for file in files:
            fname = file
            #new = fname[0] + 'b' + fname[1]
            filePath=os.path.join(rt,file)
            #print(fname,dirs,rt)
            if append not in fname.lower():
                continue
            filePaths.append(filePath)
    return filePaths
             #os.rename(os.path.join(rt,f),os.path.join(rt,new))
def unzipFile(src,destFolder):
    
    zfile=zipfile.ZipFile(src,'r')
    #count=0
    
    for fileName in zfile.namelist():
        
        #print(fileName)
        data=zfile.read(fileName)
        targetFileName=fileName.replace(os.sep,"_")
        print()
        targetFullPath=os.path.join(destFolder,targetFileName)
        print(targetFullPath)
        if not os.path.exists(destFolder):
            os.makedirs(destFolder)
        file=open(targetFullPath,'w+b')
        file.write(data)
        
def unzipFolder(zipFileName,sku,targetFolder):
    
    
    #zipfileRead=zipfile.ZipFile(zipFileName)
    unZipFolder=zipFileName.split(".")[0]
    #targetFolder=os.path.join(targetFolder,date)
    if not os.path.exists(unZipFolder):
        os.makedirs(unZipFolder)
    print(unZipFolder)
    result=os.system("7za x {zipName} -y -o{outputDir}".format(zipName=zipFileName,outputDir=unZipFolder))
    
    zipFileList=workThroughDir(unZipFolder, ".zip")
    
    for eachfile in zipFileList:
        fileNameSplit=eachfile.split(os.sep)
        testResult=fileNameSplit[len(fileNameSplit)-7]
        hour=fileNameSplit[len(fileNameSplit)-8]
        project=fileNameSplit[len(fileNameSplit)-4]
        skuName=fileNameSplit[len(fileNameSplit)-3]
        station=fileNameSplit[len(fileNameSplit)-2]
        SN=fileNameSplit[len(fileNameSplit)-1].replace(".zip","")
        
        
        destFolder=os.path.join(targetFolder,testResult,hour,project,skuName,station,SN)
        
        print(destFolder)
        if sku in project:
            unzipFile(eachfile,destFolder)
            logdir=os.path.join(targetFolder,"wholeLog0801",testResult,hour,project,skuName,station,SN)
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            shutil.copy(eachfile.replace(".zip",".log"),logdir)
        
        
    
    #for each in zipfileRead.namelist():
        
        #print(each)
    
        
            
        
        
if __name__=="__main__":
    
    fileList=workThroughDir("/mnt/storageDisk1/PG504/PB-21379/zip", "7z")
    total=len(fileList) 
    count=0
    for eachFile in fileList:
        count+=1
        print("finished %f.2"%(count/total))
        unzipFolder(eachFile,"G504","/mnt/storageDisk1/PG504/PB-21379/unzip")
        