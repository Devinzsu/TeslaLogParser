import re
regexCompile={}
regexCompileMult={}
#regexCompile["SN"]=[re.compile("Prod\s+Ser\.\s+No\.\s+:\s+(?P<data>\d+)\s+ ")]
#regexCompile["ateSpeedo"]=[re.compile("AteSpeedo\s+:\s+(?P<data>\d+)")]
#regexCompile["ecid"]=[re.compile("ECID\s+:\s+(?P<data>.+-.+\w)\s+")]
#regexCompile["initNvvdd"]=[re.compile("NVVDD\s+:\s+(?P<data>\d+)\s+mV")]
#regexCompile["exitErroCode"]=[re.compile("Error\s+Code\s+=\s+(?P<data>\d+)\s+")]
# gpuTempReg="TSOSC_OFFSET_MAX:\s+\[\s+(?P<data>.+)\s+\]"
# ECID           : PFTB88-10_x03_y03
# hbmCmbTempReg="HBM2_COMBINED_MAX:\s+\[\s+(?P<data>.+)\s+\]"
# 
# hbm0TempReg="HBM2_DEFAULT\s+\(siteIdx\s+=\s+0\):\s+\[\s+(?P<data>.+)\s+\]"
# hbm1TempReg="HBM2_DEFAULT\s+\(siteIdx\s+=\s+1\):\s+\[\s+(?P<data>.+)\s+\]"
# hbm2TempReg="HBM2_DEFAULT\s+\(siteIdx\s+=\s+2\):\s+\[\s+(?P<data>.+)\s+\]"
# hbm3TempReg="HBM2_DEFAULT\s+\(siteIdx\s+=\s+3\):\s+\[\s+(?P<data>.+)\s+\]"
# totalPowerReg="Power\s+\(INPUT_TOTAL_BOARD\):\s+\[\s+(?P<data>.+)\s+\]"




regexCompileMult["station"]=[
                            re.compile("Running\s+(?P<data>.+)\s+sequence",re.IGNORECASE),
                            re.compile("-spec\s+(?P<data>\w+Spec)\s+",re.IGNORECASE),
                            re.compile("Start\s+Testing\s+(?P<data>\w+)"),
                            re.compile("Command Line\s+:\s+.+-readspec\s+(?P<data>.+)\.spc.+"),
                            re.compile("(?P<data>hw_row_repair)"),
                            
                            #re.compile("bick\s+ver(?P<data>.+)")
                             ]

regexCompileMult["subStation"]=[re.compile("Start\s+(?P<data>.+)\s+timestamp", re.IGNORECASE)]
regexCompileMult["subStation"].append(re.compile("Switched\s+to\s+PState\s+(\d)\s+\((?P<data>.+)\)", re.IGNORECASE))
#regexCompileMult["pstate"]=[re.compile("Switched\s+to\s+PState\s+(\d)\s+\((?P<data>.+)\)", re.IGNORECASE)]
#regexCompileMult["nvvdd"]=[re.compile("NVVDD\s+=\s+(?P<data>.+)\s+mV")]
#regexCompileMult["ClkGpc"]=[re.compile("ClkGpc\s+=\s+(?P<data>.+)\s+MHz")]
#regexCompileMult["exitErroCode"]=[re.compile("Error\s+Code\s+=\s+(?P<data>\d+)\s+")]

'''
regexCompileMult["gpuMax"]=[re.compile("TSOSC_OFFSET_MAX:\s+\[\s+(?P<data>.+)\s+\]")]
regexCompileMult["hbm2_COMBINED_MAX"]=[re.compile("HBM2_COMBINED_MAX:\s+\[\s+(?P<data>.+)\s+\]")]
regexCompileMult["hbm0Temp"]=[re.compile("HBM2_DEFAULT\s+\(siteIdx\s+=\s+0\):\s+\[\s+(?P<data>.+)\s+\]")]

regexCompileMult["hbm1Temp"]=[re.compile("HBM2_DEFAULT\s+\(siteIdx\s+=\s+1\):\s+\[\s+(?P<data>.+)\s+\]")]
regexCompileMult["hbm2Temp"]=[re.compile("HBM2_DEFAULT\s+\(siteIdx\s+=\s+2\):\s+\[\s+(?P<data>.+)\s+\]")]
regexCompileMult["hbm3Temp"]=[re.compile("HBM2_DEFAULT\s+\(siteIdx\s+=\s+3\):\s+\[\s+(?P<data>.+)\s+\]")]
regexCompileMult["totalPowerReg"]=[re.compile("Power\s+\(INPUT_TOTAL_BOARD\):\s+\[\s+(?P<data>.+)\s+\]")]
'''

##Exit 020000310282 : CudaLinpackHMMAgemm.Run (test 310)
regexCompileMultTest={}

regexCompileMultTest["ExitCode"]=[re.compile("Exit\s+(?P<errorCode>\d+)\s+:\s+(?P<testName>.+)\s+\(test\s+(?P<testNumber>.+)\)\s+(?P<errorDescript>.+)\s+\[(?P<exitTime>\d+\.\d+)\s+seconds\]")
                                  ]

regexCompileMultTest["ErrorCode"]=[re.compile("Exit\s+(?P<errorCode>\d+)\s+:\s+(?P<testName>.+)\s+\(test\s+(?P<testNumber>.+)\)\s+(?P<errorDescript>.+)\s+\[(?P<exitTime>\d+\.\d+)\s+seconds\]")
                                  ]
regexCompileMultTest["ErrorCode"].append(re.compile("Error\s+(?P<errorCode>\d+)\s+:\s*(?P<testName>.+)\s*(?P<exitReason>.+?)\s*\[(?P<exitTime>\d+\.\d+)\s+seconds\]"))

regex={}
regex["nvlink"]=[re.compile("GPU\s+0\s+\[02:00\.0\]\s+:\s+(?P<nvlinkNum>.+)\s+Physical\s+Lane\(0-7\)\s+(?P<radias>.+)\s+=\s+(?P<data>.+)"),
                 re.compile("GPU\s+0\s+\[02:00\.0\]\s+:\s+(?P<nvlinkNum>.+)\s+Lane\(0-7\)\s+(?P<radias>.+)\s+=\s+(?P<data>.+)")
                 ]

regex["pexLane"]=[re.compile("GPU\s+0\s+\[02:00\.0\]\s+:\s+PEX\s+Lane\(0-15\)\s+(?P<radias>.+)\s+=\s+(?P<data>.+)")]


'''Enter CudaXbar.Run (test 220) Tue Oct 24 03:44:44 2017'''


'''
Local Correctable (allowed) = 4008 (111)
  Host Correctable (allowed) = 178 (111)
  Local Non-Fatal (allowed) = 0 (0)
  Host Non-Fatal (allowed) = 0 (0)
  Local Fatal (allowed) = 0 (0)
  Host Fatal (allowed) = 0 (0)
  Local Unsupported Request (allowed) = 0 (0)
  Host Unsupported Request (allowed) = 0 (0)
  Local LineErrors (allowed) = 0 (28)
  Local CRCErrors (allowed) = 2 (28)
  Local NAKs Received (allowed) = 0 (28)
  Local FailedL0sExits (allowed) = 0 (28)
  Local NAKs Sent (allowed) = 98 (28)

'''
regex_pex={}
regex_pex["local_Correctable"]=[re.compile("Local\s+Correctable\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]

regex_pex["host_Correctable"]=[re.compile("Host\s+Correctable\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]
regex_pex["local_none_fatal"]=[re.compile("Local\s+Non-Fatal\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]
regex_pex["host_none_fatal"]=[re.compile("Host\s+Non-Fatal\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]
regex_pex["local_fatal"]=[re.compile("Local\s+Fatal\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]
regex_pex["host_fatal"]=[re.compile("Host\s+Fatal\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]
regex_pex["local_unsupported_request"]=[re.compile("Local\s+Unsupported\s+Request\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]
regex_pex["host_unsupported_request"]=[re.compile("Host\s+Unsupported\s+Request\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]

regex_pex["local_lineErrors"]=[re.compile("Local\s+LineErrors\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]
regex_pex["local_CRCErrors"]=[re.compile("Local\s+CRCErrors\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]

regex_pex["local_NAKs_received"]=[re.compile("Local\s+NAKs\s+Received\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]
regex_pex["local_NAKs_received"]=[re.compile("Local\s+NAKs\s+Received\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]

regex_pex["local_failedL0sExits"]=[re.compile("Local\s+FailedL0sExits\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]
regex_pex["local_NAKs_sent"]=[re.compile("Local\s+NAKs\s+Sent\s+\(allowed\)\s+=\s+(?P<errorCount>\d+)\s+\((?P<allowedCount>\d+)\)")]

#regex["lastEnterTest"]=[re.compile("Enter\s+(?P<testName>\w+\.\w+)\s+\(test\s+(?P<testNum>)\)\s+(?P<testEnterTime>.+))")]
