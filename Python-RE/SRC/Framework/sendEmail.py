import pandas as pd
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def sendOutlookMail(obj):
    port = int(obj.config['ExchangePort'])  # For SSL
    SERVER = obj.config['ExchangeServer']
    msg=MIMEMultipart('alternative')
    frm='sender@gmail.com'
    disclamerfile= open('SIG.htm','r')    #in case  you have a sig file else comment this part
    disclamer=disclamerfile.read()
    disclamerfile.close()
    to=obj.config['ExchEmailTo'].split(";")
    cc=obj.config['ExchEmailCc'].split(";")
    msg['From']=frm
    msg['To']=','.join(to)
    msg['Cc']=','.join(cc)
    to+=cc
    BODY=''
    if obj.TransactionData is None:
        msg['Subject']="Input File is missing"
        BODY+=obj.config['ExchEmailBodyNOFILE']
    elif len(obj.TransactionData)==0:
        msg['Subject']="No Valid Data found in the Input File"
        BODY+=obj.config['ExchEmailBodyNODATA']
    elif obj.SystemException:
        msg['Subject']=obj.SystemException
    elif obj.BusinessRuleException:
        msg['Subject']="Process Failed! with :" +obj.BusinessRuleException
        BODY+=obj.config['ExchEmailBodyBRE']
    elif obj.metrics.JobStatus!=1:
        StartTime=str(obj.StartTime)
        msg['Subject']="Process Compelted Successfully "+str(StartTime)[:-7].replace("-","/")
        BODY+=obj.config['ExchEmailBodySuccess']
        TotalCount=len(obj.output)-1
        SuccessCount=0
        InvalidCount=0
        for x in obj.output:
            if x[2]=='STATUS':
                continue
            if x[2]=='SUCCESS' or x[2].startswith('BRE:'):
                if x[2].startswith('BRE:'):
                    InvalidCount+=1
                SuccessCount+=1
        FailedCount=TotalCount-SuccessCount
        STATS=obj.config['ExchEmailBodyReport'].replace('AAAAA',str(TotalCount)).replace('BBBBB',str(SuccessCount)).replace('CCCCC',str(FailedCount)).replace('DDDDD',str(InvalidCount))
        RATIO=obj.config['ExchEmailBodyTime'].replace('AAAAA',str(StartTime)[:-7].replace("-","/")).replace('BBBBB',str(obj.metrics.EndTime)[:-7].replace("-","/")).replace('CCCCC',str((SuccessCount*100)//TotalCount))
        BODY+=STATS+RATIO
        with open(obj.outputfile,'rb') as atch:
            part=MIMEApplication(atch.read(),Name=obj.outputfile)
        part['Content-Disposition']='attachment;filename="{}"'.format(obj.outputfile.split('/')[-1])
        msg.attach(part)
    BODY+=disclamer
    msg.attach(MIMEText(BODY,'plain'))
    msg.attach(MIMEText(BODY,'html'))
    try:
        context = ssl.create_default_context()
        server=smtplib.SMTP(SERVER,port)
        server.starttls(context=context)
        server.login(frm,'PASSWORD')
        server.sendmail(frm,to,msg.as_string())
    finally:
        server.quit()