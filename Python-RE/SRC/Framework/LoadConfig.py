import pandas as pd

class Config:
    def __init__(self,path):
        self.path=path
        self.config=self.loadConfig()
        #print("Started")
    
    def LoadExcelConfig(self):
        try:
            config=pd.ExcelFile(self.path)
            configDict={}
            for sheet in config.sheet_names:
                df=pd.read_excel(self.path,sheet)
                df=df[['Name','Value']]
                configDict.update(df.set_index('Name')['Value'].to_dict())
        except Exception as ex:
            print("Exception :"+str(ex))
            raise
        return configDict
	
    def loadConfig(self):
    	config=pd.read_csv(self.path,sep=',',error_bad_lines=False,warn_bad_lines=False)
    	config=config[config['NAME'].notna()]
    	config=config[['NAME','VALUE']]
    	configDict=config.set_index('NAME')['VALUE'].T.to_dict()
    	return configDict

    
