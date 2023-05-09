import datetime
class logger(object): 
    def __init__(self, exePath, LogFileName, logLvl=0):
        self.logLvl = logLvl
        dateNow = datetime.datetime.now()
        dateNowDay = dateNow.strftime('%d')
        dateNowMonth = dateNow.strftime('%m')
        self.logname = '{}/{}_{}.log'.format(exePath, LogFileName, dateNowMonth)
        if str(dateNowDay) == '01':
            with open(self.logname, 'a+') as fp:
                fp.seek(0)
                fp.truncate()  

    def writeLog(self, logMsg):
        with open(self.logname, 'a+') as fp:
            fp.write(logMsg)

    def debug(self, txt, prt=False):
        logTime = datetime.datetime.now()
        logMsg = '{} [DEBUG]: {}\n'.format(logTime, txt)
        if self.logLvl >= 3 or prt:
            self.writeLog(logMsg)
            print(logMsg, end='')

    def info(self, txt, prt=False):
        logTime = datetime.datetime.now()
        logMsg = '{} [INFO]: {}\n'.format(logTime, txt)
        if self.logLvl >= 2 or prt:
            self.writeLog(logMsg)
            print(logMsg, end='')

    def warning(self, txt, prt=False):
        logTime = datetime.datetime.now()
        logMsg = '{} [WARNING]: {}\n'.format(logTime, txt)
        if self.logLvl >= 1 or prt:
            self.writeLog(logMsg)
            print(logMsg, end='')

    def error(self, txt, prt=False):
        logTime = datetime.datetime.now()
        logMsg = '{} [ERROR]: {}\n'.format(logTime, txt)
        if self.logLvl >= 0:
            self.writeLog(logMsg)
            print(logMsg, end='')

    def critical(self, txt, prt=False):
        logTime = datetime.datetime.now()
        logMsg = '{} [CRITICAL]: {}\n'.format(logTime, txt)
        if self.logLvl >= 0:
            self.writeLog(logMsg)
            print(logMsg, end='')   

