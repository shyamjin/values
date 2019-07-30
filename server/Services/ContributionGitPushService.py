#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################
# ContributionGitPushService Scheduler
###############################

'''
Created on Mar 16, 2016

@author: PDINDA
'''

from datetime import datetime
import json
import logging
import os
from os.path import join
import subprocess
import time
import traceback
from urlparse import urlparse

from autologging import logged
from git import Repo
import git
import requests
from requests.exceptions import ConnectionError, ReadTimeout

from DBUtil import Config, Tool, Versions, ContributionGitPushLogs, \
    SystemDetails
import Mailer
from Services import SchedulerService, ConfigHelperService



job = None


@logged(logging.getLogger("ContributionGitPushService"))
class ContributionGitPushService(object):

    # Init's Data

    def __init__(self, db):
        '''
           General description :
           This function initializes the database variables and \
           index to refer in functions.
        '''

        self.configdb = Config.Config(db)
        self.toolDb = Tool.Tool(db)
        self.versionsDb = Versions.Versions(db)
        self.contributionGitPushLogsDb = \
            ContributionGitPushLogs.ContributionGitPushLogs(db)
        self.mailer = Mailer.Mailer()
        self.systemDetailsDb = SystemDetails.SystemDetails(db)
        self.config_id = 14
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()

    def load_configuration(self):
        '''
        General description:This method configures the load
        Args:
            none
        Returns:none

        '''
        ConfigHelperService.load_common_configuration(self)
        if not self.result.get('git_path'):
            raise Exception('git_path not found for  config'
                            )
        else:
            self.git_path = self.result['git_path']
        self.systemDetail = \
            self.systemDetailsDb.get_system_details_single()
        if not self.systemDetail:
            raise Exception('systemDeatils not found')
        self.account_name = self.systemDetail.get('account_name')
        result = self.configdb.getConfigByName("CloneAccountServiceDetails")
        if not result.get('gitlab_token'):
            raise Exception('gitlab_token not found for  config'
                            )
        else:
            self.gitlab_token = result['gitlab_token']  # PRIVATE TOKEN
        if not result.get('git_lab_rest_api_url'):
            raise Exception('git_lab_rest_api_url not found for  config'
                            )
        else:
            self.git_lab_rest_api_url = \
                result['git_lab_rest_api_url']

    # Checks no of pending requests
    # Creates sub threads to handle this requests # Minimum Threads is 1
    # The no of threads is configurable from main.py
    # (DeploymentService.DeploymentService(db).schedule(schedulerObj,1,1))
    @ConfigHelperService.run
    def job_function(self):
        '''
        General description:This method initiates Git contribution service for all tools
        Args:
            none
        Returns:none

        '''
        print ' started running at ' \
            + time.ctime(time.time())
        self.load_configuration()
        # stuti
        list = {}
        for tool in self.toolDb.get_tools_all(['active', 'indevelopment'
                                               ]):
            versionsInTool = \
                self.versionsDb.get_all_tool_versions(str(tool['_id']),
                                                   True
                                                   )
            for version in versionsInTool:
                print ' Checking version_id :' \
                    + str(version['_id'])
                if version.get('status') == '1':
                    rec = {}
                    rec['start_time'] = datetime.now()
                    rec['status'] = 'Started'
                    try:
                        if version.get('gitlab_repo'):

                            # CHECK IF THE TOOL FOLDER HAS A GIT REPO

                            if str('.git') \
                                in str(version.get('gitlab_repo'
                                                   )).lower():
                                tool_git_folder_name = \
                                    (version['gitlab_repo'].split('/'
                                                                  )[-1])[:-4]
                                # ENDS WITH .git
                            else:

                                # ends with a folder name

                                tool_git_folder_name = \
                                    version['gitlab_repo']

                            rec['directory'] = join(self.git_path,
                                                    tool_git_folder_name)
                            print ' Trying to look over path ' \
                                + rec['directory']
                            rec['status_message'] = \
                                'Trying to look over path ' \
                                + rec['directory']

                            # DIRECTORY DOES NOT EXISTS .CREATING IT

                            if not os.path.isdir(rec['directory']):
                                raise ValueError('No such repository found:'
                                                 + rec['directory'])

                            # CONNECTING TO REPO

                            print ' Trying to connect path ' \
                                + rec['directory']
                            repo = Repo(str(rec['directory']))
                            print ' Connected to Repo'
                            rec['status_message'] = ' Connected to Repo'

                            # IF TRUE THIS IS A NEW REPO AND NEEDS TO HAVE A
                            # NEW ORIGIN

                            if len(repo.remotes) == 0:  # HAS ACTIVE BANCHES
                                print ' This is a Bare Repo'
                                rec['status_message'] = \
                                    ' This is a Bare Repo'
                                url = self.git_lab_rest_api_url \
                                    + 'users/'

                                headers = \
                                    {'Content-Type': 'application/json',
                                     'PRIVATE-TOKEN': self.gitlab_token}
                                print ' Trying to call :' \
                                    + url
                                rec['status_message'] = \
                                    ' Trying to call :' + url
                                response = requests.get(url,
                                                        headers=headers, timeout=600,
                                                        verify=False)
                                if response.status_code != 200:
                                    raise ValueError(str(response.status_code)
                                                     + ' ' + response.reason + '. '
                                                     + str(response._content).translate(None,
                                                                                        '{"}') + '. ' + url)
                                gitlab_account_users = \
                                    json.loads(response.text)
                                print 'Called url :' + url \
                                    + ' Response:' \
                                    + str(gitlab_account_users)
                                user_id = None
                                for user in gitlab_account_users:
                                    if str(user.get('name')).lower() \
                                            == str(self.account_name + '_admin').lower():
                                        user_id = str(user.get('id'))
                                        break
                                if not user_id:
                                    raise 'Could not find in Git User:' \
                                        + str(self.account_name +
                                              '_admin').lower()
                                url = self.git_lab_rest_api_url \
                                    + 'projects/' + 'user/' \
                                    + str(user_id)
                                payload = \
                                    {'name': os.path.basename(rec['directory'
                                                                  ])}
                                payload_json = json.dumps(payload)
                                headers = \
                                    {'Content-Type': 'application/json',
                                     'PRIVATE-TOKEN': self.gitlab_token}
                                print ' Trying to call :' \
                                    + url + ' with payload :' \
                                    + str(payload)
                                rec['status_message'] = \
                                    ' Trying to call :' + url \
                                    + ' with payload :' + str(payload)
                                response = requests.post(url,
                                                         data=payload_json,
                                                         headers=headers, timeout=600,
                                                         verify=False)
                                if response.status_code != 201:
                                    raise ValueError(str(response.status_code)
                                                     + ' ' + response.reason + '. '
                                                     + str(response._content).translate(None,
                                                                                        '{"}') + '. ' + url)
                                project_details = \
                                    json.loads(response.text)
                                print 'Called url :' + url \
                                    + ' Response:' \
                                    + str(project_details)

                                # FETCHING DATA FROM RESPONSE DATA

                                git_repo_url = \
                                    project_details['http_url_to_repo']

                                # REPLACE THE HOST NAME

                                git_repo_url = \
                                    git_repo_url.replace(urlparse(project_details['http_url_to_repo'
                                                                                  ]).hostname,
                                                         urlparse(self.
                                                                  git_lab_rest_api_url).
                                                         hostname)

                                # REPLACE THE USERNAME AND PASSWORD

                                git_repo_url = \
                                    git_repo_url.replace('://', '://'
                                                         + self.account_name + ':'
                                                         + 'vpadmin123' + '@', 1)

                                # CREATE REMOTE ORIGIN

                                rec['status_message'] = \
                                    'Trying to Create Origin: ' \
                                    + git_repo_url
                                print ' Trying to Create Origin: ' \
                                    + git_repo_url
                                repo.create_remote('origin',
                                                   url=git_repo_url)
                            else:

                                # SWITCH TO MASTER
                                # WE ASSUME THAT USER HAS PUSHED SOME CODE
                                # IF USER HAS NEVER PUSHED CODE THEN THIS IS 0

                                if len(repo.branches) != 0:
                                    repo.git.checkout('master')
                                    print ' ' + \
                                        'Trying to find repo.working_tree_dir'
                                    if repo.working_tree_dir is None:
                                        print 'New Repo.No files to Push'
                                        raise ValueError('New Repo.No files to Push'
                                                         )
                                    rec['status_message'] = \
                                        'working_tree_dir was found'
                                    print '' + \
                                        'Trying to find repo.is_dirty()'
                                    if repo.is_dirty():
                                        print '' + \
                                            'Untracked Files found'
                                        raise ValueError('' +
                                                         'Untracked Files found'
                                                         )
                                    print ' Trying to push'
                                    rec['status_message'] = \
                                        'Trying to push'
                                    logs = \
                                        str(subprocess.check_output('git push --all origin',
                                                                    cwd=rec['directory'], shell=True))
                                    print logs
                                    rec['push_logs'] = logs
                                    repo.git.checkout('dummy')
                            rec['status'] = 'Success'
                            rec['status_message'] = \
                                'Completed for this version'
                            rec['end_time'] = datetime.now()
                        else:
                            rec['status'] = 'Success'
                            rec['status_message'] = \
                                'Repo does not have a gitlab_repo'
                            rec['end_time'] = datetime.now()
                    except Exception, e:

                                            # catch *all* exceptions

                        traceback.print_exc()
                        rec['status'] = 'Failed'
                        rec['last_status_message'] = \
                            rec.get('status_message')
                        rec['status_message'] = 'Error :' + str(e)
                        if type(e) in [ConnectionError, ReadTimeout]:
                            rec['status_message'] = 'Error :' \
                                + 'Unable to connect to ' \
                                + self.git_lab_rest_api_url
                        rec['end_time'] = datetime.now()
                    finally:
                        list[str(version['_id'])] = rec
                        print ' version_id :' \
                            + str(version['_id']) + ' was handled'
        self.contributionGitPushLogsDb.AddContributionGitPushLogs(list)
        self.notify(list)
        print ' ended running at ' \
            + time.ctime(time.time())

    def notify(self, user_list):
        '''
        General description:This method notifies the owner of TOOL / DU about any code changes made.
        Args:
            param1:user_list(list):list of user
        Returns:none

        '''
        try:
            if self.result.get('distribution_list'):
                self.mailer. \
                    send_html_notification(self.result.get
                                           ('distribution_list'),
                                           None, None, 9, {'name': 'User',
                                                           'log': str(user_list)})
        except Exception, e:

                                # catch *all* exceptions

            print 'Failed to save email' + str(e)

    def schedule(self):
        '''
        General description: # Schedules the job
        # scheduler :Scheduler object
        # interval_given:Time interval for job to rerun
        Args:
            none
        Returns:none

        '''
        global job
        self.load_configuration()
        job = self.schedulerService.schedule(job, self)
