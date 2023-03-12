import pandas as pd
import os
from Framework import metrics

def loadData(obj):
    if obj.TransactionData is None:
        try:
            obj.TransactionData=pd.read_csv(obj.InputFile,skip_blank_lines=True)
            obj.TransactionData=obj.TransactionData.values.tolist()
        except Exception as ex:
            obj.printlog.exception(ex)
            if 'No such' in str(ex):
                raise Exception("BRE : File is not Present")
            else:
                raise
    if obj.TransactionNumber<=len(obj.TransactionData):
        obj.TransactionItem=obj.TransactionData[obj.TransactionNumber-1]
        obj.TransactionData1=obj.TransactionItem[1]
        if obj.TransactionNumber==1:
            obj.prevValue=obj.TransactionItem[2]
        if obj.TransactionItem[2]!=obj.prevValue:
            obj.prevValue=obj.TransactionItem[2]
    else:
        obj.TransactionItem=None
