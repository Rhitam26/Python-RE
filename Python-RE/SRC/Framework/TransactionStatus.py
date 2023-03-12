

def setTransactionStatus(obj):
    row=[obj.TransactionData1,obj.TransactionItem[2]]
    if obj.SystemException is not None:
        if obj.globalretry>= obj.config["Max Retry"]:
            obj.TransactionNumber+=1
            obj.metrics.FailedCount+=1
            row.append("FAILED :"+obj.SystemException)
        else:
            obj.globalretry= obj.globalretry+1   
    elif obj.BusinessRuleException:
        obj.metrics.InvalidCount+=1
        obj.metrics.SuccessCount+=1
        row.append(obj.BusinessRuleException)
    else:
        obj.metrics.SuccessCount+=1
        row.append("SUCCESS")
    obj.output.append(row)
        
    