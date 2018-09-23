def compareCmdLine(first,second):
    
    firstCmdList=first.split("-")
    secondCmdList=second.split("-")
    
    result={"added":[],"deleted":[]}
    
    for eachArg in firstCmdList:
        
        if not existArg(secondCmdList, eachArg):
            result["deleted"].append(eachArg.strip())
    for eachArg in secondCmdList:
        if not existArg(firstCmdList, eachArg):
            result["added"].append(eachArg.strip())
    
    return result
            
        
def existArg(cmdList,arg):
    
    for eachArg in cmdList:
        
        if arg.strip()==eachArg.strip():
            return True
    return False