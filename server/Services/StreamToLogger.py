'''
Created on Apr 11, 2016

@author: PDINDA
'''

import inspect
import logging
import os


class StreamToLogger(object):

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        func = inspect.currentframe().f_back.f_code
        pre_text = "[" + os.path.basename(func.co_filename).split(".")[
            0] + ":" + func.co_name + "()]: "
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, pre_text + line.rstrip())

    def flush(self):
        pass
