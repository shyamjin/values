'''
Created on Mar 16, 2016

@author: PDINDA
'''
import logging
import traceback

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.scheduler import Scheduler
from autologging import logged


# STATIC SCHEDULER
schedulerObj = None


@logged(logging.getLogger("SchedulerService"))
class SchedulerService(object):

    def my_listener(self, event):
        global schedulerObj
        if event.exception:
            print 'The job crashed :('
        else:
            print 'The job worked :)'

    def get_scheduler_object(self):
        global schedulerObj
        try:
            return schedulerObj
        except Exception as e:  # catch *all* exceptions
            traceback.print_exc()
            return None

    def start_scheduler(self):
        global schedulerObj
        schedulerObj = Scheduler()
        schedulerObj.start()
        schedulerObj.add_listener(
            self.my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        print 'Scheduler is started.'

    def stop_scheduler(self):
        global schedulerObj
        try:
            schedulerObj.shutdown(
                wait=False, shutdown_threadpool=True, close_jobstores=True)
            print 'Scheduler is Stopped.'
        except Exception as e:  # catch *all* exceptions
            traceback.print_exc()
            return False

    def get_scheduled_jobs(self):
        global schedulerObj
        try:
            return schedulerObj.getJobs()
        except Exception as e:  # catch *all* exceptions
            traceback.print_exc()
            return None

    def schedule(self, job, obj):
        """
        # Schedules the job
        # scheduler :Scheduler object"""
        global schedulerObj
        try:
            if job:
                self.un_schedule(job, obj)
            if obj.start_service:
                if obj.service_type == "interval":
                    job = schedulerObj.add_interval_job(
                        obj.job_function, minutes=obj.interval_given, max_instances=1, coalesce=True)
                    print obj.__class__.__name__ + ' was scheduled to run every ' \
                        + str(obj.interval_given) + ' minutes.'
                elif obj.service_type == "scheduled":
                    job = schedulerObj.add_cron_job(obj.job_function, hour=int(
                        obj.hours), minute=int(obj.minutes), max_instances=1, coalesce=True)
                    print obj.__class__.__name__ + ' was scheduled to run at ' \
                        + str(obj.hours) + ':' + \
                        str(obj.minutes) + ' everyday.'
                return job
            return None
        except Exception as e:  # catch *all* exceptions
            print 'failed to start with error : :' + str(e)
            traceback.print_exc()
            raise ValueError(
                'failed to start with error :' + str(e))

    def un_schedule(self, job, obj):
        """ # UnSchedules the job"""
        global schedulerObj
        try:
            print "Trying to unschedule: " + obj.__class__.__name__ + 'was Unscheduled'
            schedulerObj.unschedule_job(job)
            print obj.__class__.__name__ + 'was Unscheduled'
        except Exception as e:  # catch *all* exceptions
            pass
