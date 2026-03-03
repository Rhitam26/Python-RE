import csv
import logging
import time
import getpass
import sys
from datetime import datetime
import traceback

import Framework.InitBlock as ib
import Framework.getTransaction as GT
import Framework.process as pr
import Framework.TransactionStatus as TS
import Framework.sendEmail as mail

logging.basicConfig(
    filename='ABS_PATH/LOGS/runlog.out',
    filemode='a',
    format='%(asctime)s %(levelname)-8s '+getpass.getuser()+' %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S', 
)

class Obj:
    def __init__(self,CofigPath):
        self.StartTime=datetime.now()
        self.printlog=logging
        self.TransactionNumber=1
        self.TransactionData=None
        self.TransactionRow=None
        self.TransactionItem=[]
        self.TransactionData1=None
        self.TransactionData2=None
        self.BusinessRuleException=None
        self.SystemException=None
        self.config=None
        self.InputFile=None
        self.outputfile=None
        self.prevValue=None
        self.CofigPath=CofigPath
        self.output=[['HEADER_1','HEADER_2','STATUS']]
        self.globalretry=0
    
    
def main():
    print("Process Started Successfully!")
    obj=Obj("ABS_PATH/CONFIG/Config.csv")
    ######## INIT BLOCK START
    ib.initApplications(obj)
    ######## END of INIT BLOCK
    if obj.BusinessRuleException is None and obj.SystemException is None:
        while(obj.TransactionItem is not None and obj.globalretry<= obj.config["Max Retry"]):
            obj.SystemException=None
            obj.BusinessRuleException=None
            try:
                GT.loadData(obj)
            except Exception as ex:
                obj.TransactionItem=None
                if 'BRE' in str(ex):
                    obj.BusinessRuleException=str(ex)
                    obj.printlog.INFO(ex)
                else:
                    obj.SystemException=str(ex)
                    obj.printlog.info(ex)
            if obj.TransactionItem is None:
                break
            print("Processing Transaction Item: "+str(obj.TransactionNumber))
            try:
                #pass
                pr.process(obj)
            except Exception as ex:
                obj.printlog.exception(ex)
                #obj.chromeDriver.save_screenshot(obj.config['ExceptionScreenShot']+'EXCEPTION_'+str(datetime.now()).replace("-",'_').replace(":",'_').replace(".",'_')+'.png')
                if 'BRE' in str(ex):
                    obj.BusinessRuleException=str(ex)
                else:
                    obj.SystemException=str(ex)
            finally:
                TS.setTransactionStatus(obj)
    try:
        obj.metrics.writeMetrics(obj)
        if obj.TransactionNumber>1:
            obj.outputfile=obj.metrics.createOutputFile(obj)
    finally:
        mail.sendOutlookMail(obj)
    print("Execution Completed Successfully!")

if __name__=="__main__":
    main()

