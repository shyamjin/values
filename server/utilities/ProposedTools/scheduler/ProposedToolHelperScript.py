'''
Created on Mar 21, 2018

@author: PDINDA
'''

'''
****PLEASE LOGIN AS ROOT USER****

TO USE:
####STEPS####
Copy this file to /home/valuepack/dpm/utilities/ProposedToolHelperScript.py
touch /home/valuepack/dpm/utilities/UsersListForAutoCreation.txt
(crontab -l ; echo "* * * * * /usr/bin/python /home/valuepack/dpm/utilities/ProposedTools/ProposedToolHelperScript.py  >> /home/valuepack/dpm/utilities/ProposedTools/UserCreation.log") | sort - | uniq - | crontab -

'''
import os,subprocess
from datetime import datetime

print "Script Started at: "+str(datetime.now())
BASE_PATH="/home/valuepack"

file_of_users_list=BASE_PATH+"/dpm/utilities/ProposedTools/UsersListForAutoCreation.txt"
if os.path.exists(file_of_users_list):    
    f=open(file_of_users_list, "r+")
    d = f.readlines()
    if d:
        f.seek(0)
        f.truncate()
        f.close()
        for rec in d:
            try:
                if rec:
                    user=rec.split(":")[0] 
                    directory=rec.split(":")[1]
                    proc = subprocess.Popen("useradd -d "+BASE_PATH+"/git -s /bin/bash -g vpdevgroup "+user, stdout=subprocess.PIPE, shell=True)
                    (out, err) = proc.communicate()
                    proc = subprocess.Popen('echo "unix11" | passwd --stdin '+user, stdout=subprocess.PIPE, shell=True)
                    (out, err) = proc.communicate()                    
                    proc = subprocess.Popen("chown -R "+user+":vpdevgroup "+BASE_PATH+"/git/"+directory, stdout=subprocess.PIPE, shell=True)
                    (out, err) = proc.communicate()
                    print rec+" was handled"
            except Exception as e:
                print str(e)
                print user+ " was not created"
                pass
        os.chdir(BASE_PATH+"/")
        print subprocess.Popen("/usr/local/bin/docker-compose  restart jenkins_server", stdout=subprocess.PIPE, shell=True)
        print "Jenkins was restarted"
    else:
        print "The file is empty.Nothing to do "    
else:
    print "Nothing to do"
    
print "Script Started at: "+str(datetime.now())        