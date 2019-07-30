'''
Created on Mar 16, 2016

@author: PDINDA
'''
import logging
import time

from autologging import logged

from DBUtil import Emails, Config
from Services import Mailer
from Services import SchedulerService, ConfigHelperService
from settings import mongodb



job = None


@logged(logging.getLogger("MailerService"))
class MailerService():
    """search for new or pending mails in database and
    send it to receipents"""

    def str_to_bool(self, s):
        """# Converter Function"""
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False

    def __init__(self):
        """
        # Init's Data
        ###############
        # Db instance
        ##############"""
        ###############
        # Collection
        ##############
        self.emaildb = Emails.Emails(mongodb)
        self.configdb = Config.Config(mongodb)
        self.interinterval = 7  # Time to sleep after every email
        self.config_id = 2
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()

    def load_configuration(self):
        ConfigHelperService.load_common_configuration(self)

    @ConfigHelperService.run
    def job_function(self):
        """
        # Actual Implementation
        ###LOGIC###
        # Search for email's in 'pending' status
        # Try to send those mails
        # if successful then mar them as successful else +1 retry count
        # mark failed if retry count>3"""
        self.load_configuration()
        print ' Checking for pending emails..'
        cursor = self.emaildb.GetPendingEmail()
        print ' No of Pending Emails :' + str(cursor.count())
        for document in cursor:
            Mailer.Mailer().handle_pending_notification(
                str(document['_id']))
            print ' Waiting for ' + str(self.interinterval) \
                + ' secs to send next email.'
            # Server is not able to send email's continuously
            time.sleep(self.interinterval)
        print ' Sleeping....'

    def schedule(self):
        """
        # Schedules the job
        # scheduler :Scheduler object
        # interval_given:Time interval for job to rerun"""
        global job
        self.load_configuration()
        job = self.schedulerService.schedule(job, self)
