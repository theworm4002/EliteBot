import os, json
class configSetup:
    def __init__(self, runningPath, log=None):
        self.log = log
        self.configFile = f'{runningPath}/config.json'

    def readJson(self):
        if not os.path.isfile(self.configFile):
            self.log.info("'config.json' not found! Setting default settings.")
            self.config = {
                "BSERVER": "irc.address.org",
                "BPORT": "+6697",
                "BNICK": "EliteBot",
                "BIDENT": "EliteBot",
                "BNAME": "EliteBot",
                "BBINDHOST": "0.0.0.0",
                "UseSASL": False,
                "SANICK": "SASL-Username",
                "SAPASS": "SASL-Password",
                "ConsoleLogging": True
                }
            self.writeJson()
        else:
            with open(self.configFile) as file:
                self.config = json.load(file)
                return self.config

    def writeJson(self, conf=''):
        if conf != '':
            self.config = conf
        json_object = json.dumps(self.config, indent=4, sort_keys=True)
        with open(self.configFile, 'a+') as outfile:
            outfile.seek(0)
            outfile.truncate() 
            outfile.write(json_object)          
            return self.config
        
