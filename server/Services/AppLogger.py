'''
Created on Apr 20, 2016
In docker WE NEED TO GET LOG FILES FROM COMMAND 'docker logs'.Online logs are not written

tail -f /home/valuepack/dpm/logs/applicationLogs

@author: PDINDA
'''
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import StreamToLogger
from DBUtil import Config
from settings import mongodb, log_full_path


class AppLogger(object):

    def __init__(self):
        '''
        LOGS THE APPLICATION        
        '''
        try:
            self.configdb = Config.Config(mongodb).getConfigByName("AppLogger")
            if self.configdb:
                self.enable_logging = str(self.configdb["enable"]).lower() == "true"
                self.log_to_console = str(self.configdb["log_to_console"]).lower() == "true"
                self.loggingLevel = self.configdb['loggingLevel'].upper()
                self.logFormat = self.configdb.get("logFormat")
                self.logDateFmt = self.configdb.get("dateFormat")
                self.backupCount = self.configdb.get("backupCount")
            else:             
                self.enable_logging = True
                self.log_to_console = False
                self.loggingLevel = "TRACE"
                self.logFormat = "%(asctime)s[%(levelname)-5.5s]%(message)s"
                self.logDateFmt = "%d-%m-%Y %H:%M:%S"
                self.backupCount = 0

                 
            if self.enable_logging:
                print "enable was found to be true. 'applicationLogs' will be created everyday"
                rootLogger = logging.getLogger()  # Get logger
                rootLogger.setLevel(self.loggingLevel)
                self.configdb = Config.Config(mongodb)
                logFormatter = logging.Formatter(self.logFormat,datefmt=self.logDateFmt)
                # TO PRINT LOGGER TO FILE
                fileHandler = TimedRotatingFileHandler(
                    "{0}/{1}".format(log_full_path, "applicationLogs"), when = 'midnight', interval= 1,backupCount = self.backupCount )  # FileName #EveryMidnight #Interval=1Day
                fileHandler.setFormatter(logFormatter)
                rootLogger.addHandler(fileHandler)
                if self.log_to_console:
                    # TO PRINT LOGGER ON SCREEN
                    consoleHandler = logging.StreamHandler()  # Stream all logs to sys.stdout
                    consoleHandler.setFormatter(logFormatter)
                    rootLogger.addHandler(consoleHandler)
                # All print will get written in rootLogger
                sys.stdout = StreamToLogger.StreamToLogger(rootLogger, logging.INFO)  # Hook of sys.stdout
                # All exceptions will get written in rootLogger
                sys.stderr = StreamToLogger.StreamToLogger(rootLogger, logging.ERROR)  # Hook of sys.stderr
#             else:
#                 print "enable was found to be false. " + current_path + "/log/out_logs.log' and " + current_path + "/log/err_logs.log' will be created  "
#                 sys.stdout = open(os.path.join(log_full_path,"out_logs.log"), 'a', 0)
#                 sys.stderr = open(os.path.join(log_full_path,"err_logs.log"), 'a', 0)
        except Exception as e:  # catch *all* exceptions
            print "Unable to start Logger.Reason :" + str(e)
            raise Exception("Unable to start Logger.Reason :" + str(e))