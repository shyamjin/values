
'''
###################################################START##################################################################################
****PLEASE LOGIN AS ROOT USER****

HOW IT RUNS:
INPUT AS python backupScript.py backup
INPUT AS python backupScript.py restore 16012017171234 all ####Options are:[all,dpm,git,nexus,nexus3,jenkins,mongoDump]

HOW TO SCHEDULE:
Copy this file to /home/valuepack/dpm/utilities/backupScript.py
(crontab -l ; echo "0 0 * * * python /home/valuepack/dpm/utilities/backupScript.py backup >> /home/valuepack/dpm/utilities/backupScript.log") | sort - | uniq - | crontab - 


'''

import datetime
from os import listdir, sep, path, mkdir, path
import os
import shutil
import subprocess
import sys
import tarfile
import time



base_dir = sep + 'home' + sep + 'valuepack' + sep
mongo_container_name = 'valuepack_mongo_1'

# Set your global settings here
config_tool = {'baseDir': base_dir,
               'destDir': base_dir + 'Backup',
               'BackuplogDir': base_dir + 'Backup' + sep + 'logs' + sep,
               "mongoDumpPath": base_dir + 'mongoDump',
               'sourceDir': [
                   base_dir + 'dpm',
                   base_dir + 'nexus',
                   base_dir + 'nexus3',
                   base_dir + 'jenkins',
                   base_dir + 'git',
                   base_dir + 'mongo',
                   base_dir + 'mongo_sec',
                   base_dir + 'slamdata',
                   base_dir + 'wiki'
               ],
               'excludelist': [base_dir + 'jenkins' + sep + 'workspace', base_dir + 'dpm' + sep + 'static' + sep + 'utilities'],
               'backupFolder': base_dir + 'ValuePackBackup',
               'backupDays' : 15}

curr_date = datetime.datetime.today().strftime("%d%m%Y%H%M%S")


class ValuePackBackUpRestore(object):
    def __init__(self, sourDir=None, destDir=None, folder_name_to_restore=None, tar_to_consider=None):
        self.sourDir = sourDir
        self.destDir = destDir
        self.baseDir = config_tool['baseDir']
        self.backupfolder = config_tool['backupFolder']
        if not path.exists(self.backupfolder):
            mkdir(self.backupfolder)
        if folder_name_to_restore and tar_to_consider:
            self.extracttargz(folder_name_to_restore, tar_to_consider)
        else:
            self.compress2targz()

    def compress2targz(self):
        self.backupfolder = path.join(self.backupfolder, curr_date)
        if not path.exists(self.backupfolder):
            mkdir(self.backupfolder)
        file_name = path.join(
            self.backupfolder, path.basename(self.sourDir)) + '.tar.gz'
        print "Creating file:" + file_name
        self.make_tarfile(file_name, self.sourDir, self.backupfolder)
        print "File created:" + file_name + ". Backup Size: ~" + str(int(path.getsize(file_name)) / 1048576) + " MB"

    def exclude_function(self, folder_name):
        print "Working on:" + folder_name
        for folder in config_tool['excludelist']:
            if folder in folder_name:
                print "Excluding Directory:" + folder_name
                return True
        return False

    def extracttargz(self, folder_name_to_restore, tar_to_consider):
        folderNameWithPathToRestore = path.join(
            self.backupfolder, folder_name_to_restore)
        if not path.isdir(folderNameWithPathToRestore):
            raise ValueError('No such directory:' + path.basename(folderNameWithPathToRestore) +
                             ' was found at:' + path.dirname(folderNameWithPathToRestore))
        files = [f for f in listdir(folderNameWithPathToRestore) if path.isfile(
            os.path.join(folderNameWithPathToRestore, f))]
        for f in files:
            if tar_to_consider.lower() == "all":
                pass
            elif tar_to_consider.lower() in f.lower():
                pass
            else:
                continue
            # FILE TO BE USER
            file = path.join(self.backupfolder, os.path.join(
                folderNameWithPathToRestore, f))
            # PATH TO EXTRACT TO
            backupFolderPath = path.join(
                self.backupfolder, folderNameWithPathToRestore)
            # PATH OF EXTRACTEED FOLDER
            sourceFolder = path.join(self.backupfolder, os.path.join(
                folderNameWithPathToRestore, f).replace(".tar.gz", ""))
            # NAME OF EXTRACTED FOLDER
            sourcefolderName = path.basename(sourceFolder)
            # NAME OF TARGET FOLDER TO EXTRACT TO
            targetFolder = path.join(base_dir, sourcefolderName)

            tar = tarfile.open(file)
            print "Extracting file:" + file + " " + "to:" + backupFolderPath
            tar.extractall(backupFolderPath)
            tar.close()
            print "File Extracted:" + file + " " + "to:" + sourceFolder
            if not path.exists(sourceFolder):
                raise ValueError("Unpack Failed for: " + file)
            else:
                print "Running: rsync -avzh --delete " + sourceFolder + os.sep + " " + targetFolder
                print subprocess.check_output("rsync -avzh --delete " + sourceFolder + os.sep + " " + targetFolder, shell=True)
                if path.exists(sourceFolder):
                    shutil.rmtree(sourceFolder)

    def make_tarfile(self, output_filename, source_dir, dest_dir):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=path.basename(
                source_dir), exclude=self.exclude_function)

def CleanBackup(backupFolder,backupDays):
    for f in os.listdir(backupFolder):
        if os.stat(os.path.join(backupFolder,f)).st_mtime < time.time() - backupDays * 86400:
            shutil.rmtree(os.path.join(backupFolder,f))
        

def TakeBackup():
    global config_tool
    CleanBackup(config_tool['backupFolder'],config_tool['backupDays'])
    for sourceDir in config_tool['sourceDir']:
        if path.exists(sourceDir):
            ValuePackBackUpRestore(sourceDir, config_tool['destDir'], None)
        else:
            print " Directory: " + sourceDir + " was not found.Skipping.."


def RestoreBackup(folder_name_to_restore, to_consider):
    global config_tool
    ValuePackBackUpRestore(
        None, config_tool['destDir'], folder_name_to_restore, tar_to_consider)



if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ["backup"]:
        TakeBackup()
    elif len(sys.argv) == 4 and sys.argv[1] in ["restore"]:
        folder_name_to_restore = sys.argv[2]
        tar_to_consider = sys.argv[3]
        if tar_to_consider not in ["all", "dpm", "git", "nexus", "jenkins", "nexus3" , "mongo" , "mongo_sec" , "slamdata" , "wiki"]:
            raise Exception(
                "Invalid Input. Example Input : '13012017171904 all' or '13012017171904 dpm'. Valid values are all, dpm, git, nexus, jenkins, nexus3, mongo, mongo_sec, slamdata, wiki")
        print "We will try to restore:" + tar_to_consider + " from:" + str(folder_name_to_restore)
        RestoreBackup(folder_name_to_restore, tar_to_consider)
    else:
        raise Exception("Invalid Input. Example Input : 'python backupScript.py backup' or 'python backupScript.py restore 13012017171904 all'. Valid values are all, dpm, git, nexus, jenkins, nexus3, mongo, mongo_sec, slamdata, wiki")
print 'Done...!'
