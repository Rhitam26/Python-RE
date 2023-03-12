import datetime
import csv
import getpass  #to get the current UserId
import os
import shutil
class Metrics:
    def __init__(self,ProcessID):
        self.TotalCount=0
        self.SuccessCount=0
        self.FailedCount=0
        self.InvalidCount=0
        self.ProcessID=ProcessID
        self.StartTime=datetime.datetime.now()
        self.EndTime=None
        self.UserID=getpass.getuser()

    def writeMetrics(self,obj):
        self.EndTime=datetime.datetime.now()
        self.TotalCount=self.SuccessCount+self.FailedCount
        
    def createOutputFile(self,obj):
        outputfile='ABS_PATH/OUT/OUTPUT_FILE'+' '+str(self.StartTime)[:-7].replace(':','_')+'.csv'
        with open(outputfile,'w',newline="") as out:
            writer=csv.writer(out)
            for row in obj.output:
                writer.writerow(row)
            out.close()
        print("Output File Created")
        return outputfile
    
    

