

import logging
import threading
import time
import traceback

from autologging import logged
from concurrent.futures import ThreadPoolExecutor, wait

from DBUtil import CloneRequest, Config
from Services import CloneAccountService
from Services import SchedulerService, ConfigHelperService



job = None


@logged(logging.getLogger("CloneRequestService"))
class CloneRequestService(object):

    # Init's Data
    def __init__(self, db):
        # Need to add code for Clone

        self.CloneRequestDB = CloneRequest.CloneRequest(db)
        self.noOfThreads = 1  # Minimum Threads is 1
        self.configdb = Config.Config(db)
        self.config_id = 4
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()

    def load_configuration(self):
        ConfigHelperService.load_common_configuration(self)
        self.noOfThreads = int(self.result['noOfThreads'])
        if self.noOfThreads <= 0:
            raise ValueError(
                'CloneRequestService : No of parallel threads cannot be less than 1')

    # Checks no of pending requests
    # Creates sub threads to handle this requests # Minimum Threads is 1
    # The no of threads is configurable from main.py
    @ConfigHelperService.run
    def job_function(self):
        # NEED TO HAVE THIS AS WHILE UPDATING CONFIG NEED TO RELOAD THIS
        # VARIABLE FOR RESCHEDULING
        self.load_configuration()
        print ' started running at ' + time.ctime(time.time()) + \
            ' with ' + str(self.noOfThreads) + ' parallel threads'
        pool = ThreadPoolExecutor(self.noOfThreads,__name__+".job_function")
        futures = []
        cursor = self.CloneRequestDB.GetNewPendingCloneRequests()
        for document in cursor:
            futures.append(pool.submit(self.do_stuff, str(document['_id'])))
        wait(futures)
        print ' ended running at ' + time.ctime(time.time())

    # Actual Implementation

    def do_stuff(self, task):
        try:
            cloneService = CloneAccountService.CloneDeployment()
            print ' ' + threading.currentThread().getName(), \
                'working on _id :' + str(task)
            ######################
            #  PERFORM ACTUAL task
            ######################
            cloneService.runClone(task)
            print ' ' + threading.currentThread().getName(), \
                'Ended for _id :' + str(task)
        except Exception as e:  # catch *all* exceptions
            print ' ' + threading.currentThread().getName(), \
                '_id :' + str(task) + ' failed with Error :' + str(e)
            traceback.print_exc()

    def schedule(self):
        """
        # Schedules the job
        # scheduler :Scheduler object
        # interval_given:Time interval for job to rerun"""
        global job
        self.load_configuration()
        job = self.schedulerService.schedule(job, self)
