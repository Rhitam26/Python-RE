import logging
import sys
import getpass
from Framework.metrics import Metrics
from Framework.LoadConfig import Config
import Framework.PortalLogin as lg
import Framework.CDriveLogin as cdl

def initApplications(obj):
    if not obj.config: 
        try:
            config=Config(obj.CofigPath)
            obj.config=config.config
        except Exception as ex:
            obj.printlog.exception(ex)
            if 'BRE:' in str(ex):
                obj.BusinessRuleException=str(ex)
            else:
                obj.SystemException=str(ex)
