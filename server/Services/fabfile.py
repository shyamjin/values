from contextlib import contextmanager
import os,time,traceback
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures._base import TimeoutError
from invoke import UnexpectedExit
from DBUtil import Config
from settings import remote_base_path,mongodb
from paramiko.ssh_exception import SSHException

from paramiko.ssh_exception import SSHException, AuthenticationException

configdb = Config.Config(mongodb)
if configdb.getConfigByName("FabricService") is None:
    raise Exception ("Config for FabricService was not found in DB")
default_timeout = 600


# DEFINE A DUMMY EXCEPTION
class FabricException(Exception):
    print str(Exception)
    pass


def exceptionHandler(f):
    '''
        General description:This method handles the exception.
        Args:
        param1:f
        Returns:none

    '''
    def newFunction(*args, **kw):
        try:
            result = f(*args, **kw)  # VALUES SHOULD BE NEVER RETURND AS STRING
            if result:
                return result
        except (Exception, ValueError) as e:  # catch *all* exceptions
            print 'CustomExceptionHandler handled exception %s' % e
            traceback.print_exc()
            status_message = str(e)
            status_message = status_message.replace("'", "")
            status_message = status_message.replace('"', "")
            raise Exception(status_message)
        except FabricException as e:
            raise Exception(
                "Fabric exception was received while perform given task")
        except SystemExit as e:
            raise Exception("SystemExit was received while perform given task")
    return newFunction


@contextmanager
def change_directory(path):
    '''
    context manger that generates the string for replacing fabric 1 with cd
    '''
    try:
        yield 'cd {};'.format(path)
    finally:
        pass


@exceptionHandler
def createUser(username, **kwargs):
    try:
        result = runCommand('useradd ' + username,
                            warn=True, timeout=default_timeout, **kwargs)
        if result.return_code == 9:
            print 'User username already exists '
        elif result.return_code != 0:
            raise ValueError(result.stdout)
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def grantSudo(username, **kwargs):
    try:
        result = runCommand('sudo usermod -a -G sudo ' + username,
                            warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def cloneRepository(dir, repository, **kwargs):
    try:
        result = runCommand('cd {}; git clone '.format(dir) + repository,
                            warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def checkoutRepositoryByBranch(dir, branchName, **kwargs):
    try:
        result = runCommand('cd {}; git checkout -b '.format(dir) + branchName +
                            ' upstream/' + branchName, warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def getDockerVersion(**kwargs):
    return runCommand("docker -v", warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def dockerDeamonReload(**kwargs):
    return runCommand("systemctl daemon-reload", warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def dockerRestart(**kwargs):
    return runCommand("systemctl restart docker", warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def dockerAddPermission(**kwargs):
    return runCommand("cd /etc/sysconfig/ && chmod 644 docker".format(), warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def dockerCreateFile(**kwargs):
    return runCommand("mkdir -p /etc/systemd/system/docker.service.d/", warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def nexusAddPermission(remote_nexus_home_path, **kwargs):
    return runCommand('chmod -R 777 ' + remote_nexus_home_path,
               warn=True, timeout=default_timeout, **kwargs)    


@exceptionHandler
def unzipNexus(remote_repo_folder, **kwargs):
    return runCommand('cd {} ; unzip -u nexus.zip -d ./../ ; rm -f nexus.zip'.format(
        remote_repo_folder), warn=True, timeout=default_timeout, **kwargs)
    

@exceptionHandler
def dockerComposeRestart(**kwargs):
    return runCommand('cd {} ; docker-compose restart'.format("/home/valuepack"), warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def restart_docker_jenkins(**kwargs):
    return runCommand('cd {};docker-compose restart jenkins_server'.format("/home/valuepack"), warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def gitCredentialStore(path, **kwargs):
    runCommand("cd {};git config credential.helper store".format(
        path), warn=True, timeout=default_timeout, **kwargs)
    runCommand("cd {};git checkout -b dummy".format(path),
               warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def scheduleCleaner(**kwargs):
    runCommand('(crontab -l ; echo "0 0 * * * ' + remote_base_path + 'docker-cleaner.sh  > ' +
               remote_base_path + 'cleaner.log") | sort - | uniq - | crontab -', warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def dockerLoginNexus(host, username, password, **kwargs):
    runCommand("docker login -p " + username + " -u " + password +
               host + ":10005", warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def jenkinsUpdateJobLastStep(job_folder, **kwargs):
    return runCommand('echo 1 > ' + job_folder + 'nextBuildNumber', warn=True, timeout=default_timeout, **kwargs)


def handleResult(result):
    result.stdout = result.stdout.encode('ascii', 'ignore').decode('ascii')
    result.stderr = result.stderr.encode('ascii', 'ignore').decode('ascii')
    return result


def handlemessage(message):
    return message.encode('ascii', 'ignore').decode('ascii')



@exceptionHandler
def runCommand(command, warn=False, timeout=default_timeout, **kwargs):
    connect = kwargs['connect']
    command = command.strip()
    shell = kwargs.get("shell_type", "/bin/bash -c")
    fabric_settings = configdb.getConfigByName("FabricService")
    if fabric_settings:
        timeout = int(fabric_settings.get("command_timeout",600))
    connect.connect_timeout = timeout
    try:
        retryLeft=3
        while (retryLeft > 0):
            print "fabric2:runCommand: '" + str(shell) + " " + str(command) + "' is being executed on: "\
                                 + str(connect.user) + "@" + str(connect.host) + ":" + str(connect.port)+".Retries Left: "+str(retryLeft)
            try:
                with ThreadPoolExecutor(1,__name__+".runCommand") as p:
                    if kwargs.get("use_sudo",False):
                        f = p.submit(connect.sudo,str(command), warn=warn, shell=shell, pty=kwargs.get("use_pty",False))
                        return handleResult(f.result(timeout=timeout))
                    else:
                        f = p.submit(connect.run,str(command), warn=warn, shell=shell, pty=kwargs.get("use_pty",False))
                        return handleResult(f.result(timeout=timeout))
                break;
            except SSHException as e:
                retryLeft = retryLeft-1
                if type(e) in [AuthenticationException]  or retryLeft == 0:
                    raise e
                time.sleep(10) # SLEEP 10 SEC
                exp_message= "" # KEEP BLANK
                if hasattr(e, 'message') and e.message:
                    exp_message = handlemessage(e.message)                    
                elif hasattr(e, 'strerror') and e.strerror:
                    exp_message = handlemessage(e.strerror)
                else:
                    exp_message=str(e)
                if "Error reading SSH protocol banner".upper() not in  exp_message.upper():
                    raise e
    except TimeoutError as e:
        print 'Error :' + "Command timed out maximum wait time :"+str(timeout)+" sec"
        raise ValueError("Command timed out maximum wait time :"+str(timeout)+" sec")
    except UnexpectedExit as e:
        if hasattr(e.result, 'stderr') and e.result.stderr:
            print 'Error :' + str(handlemessage(e.result.stderr))
            raise ValueError(str(handlemessage(e.result.stderr)))
        if hasattr(e.result, 'stdout') and e.result.stdout:
            print 'Error :' + str(handlemessage(e.result.stdout))
            raise ValueError(str(handlemessage(e.result.stdout)))
        print 'Error :' + str(e.result)
        raise ValueError(str(e.result))
    except Exception as e:
        if hasattr(e, 'message') and e.message:
            e.message = handlemessage(e.message)
            raise ValueError(str(e.message))
        elif hasattr(e, 'strerror') and e.strerror:
            e.strerror = handlemessage(e.strerror)
            raise ValueError(str(e.strerror))
        else:
            raise ValueError(str(e))        

        
@exceptionHandler
def pushUpstreamtoGitOrigin(dir, branchName, **kwargs):
    try:
        result = runCommand('cd {}; git push -u origin '.format(dir) + branchName,
                            warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def checkoutRepositoryByTag(dir, tagName, **kwargs):
    try:
        result = runCommand('cd {}; git checkout -b '.format(dir) + tagName + ' ' +
                            tagName, warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def createUpstream(dir, repository, **kwargs):
    try:
        result = runCommand('cd {}; git remote add upstream '.format(
            dir) + repository, warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def fetchUpstream(dir, **kwargs):
    try:
        result = runCommand('cd {}; git fetch upstream '.format(dir),
                            warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def createFolder(folder, **kwargs):
    try:
        print 'Trying to create dir : ' + str(folder)
        result = runCommand('mkdir -p -m 777 ' + folder,
                            warn=True, timeout=default_timeout, **kwargs)
        print 'Dir : ' + str(folder) + ' was created'
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def move(fromDir, toDir, filename="", **kwargs):
    try:
        print 'Trying to move to dir : ' + str(toDir) + " from: " + str(fromDir)
        result = runCommand("cd {}; mkdir -p ".format(fromDir) + toDir + " ; mv -f " +
                            filename + " " + toDir + "/ 2>/dev/null", warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def copy_dir_to_remote(RequestId, From, To, current_path, **kwargs):
    connect = kwargs['connect']
    connect.connect_timeout = default_timeout
    # handle folder copy for fabric2
    assert os.path.isdir(
        From) == True, "the path you provided is not a directory"
    for root, dirs, files in os.walk(From, topdown=True):
        for name in dirs:
            print "create dir"
            print os.path.join(root, name).replace(current_path, To).replace('\\', '/')
            runCommand('mkdir -p ' + os.path.join(root, name).replace(current_path,
                                                                      To).replace('\\', '/'), warn=True, timeout=default_timeout, **kwargs)
        for name in files:
            connect.put(os.path.join(root, name), os.path.join(root, name).replace(
                current_path, To).replace('\\', '/'), preserve_mode=False)
        runCommand('chmod -R +x {}'.format(To + '/' +
                                                   RequestId), warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def getSize(RequestId, To, **kwargs):
    try:
        result = runCommand("du -Psk {} | cut -f1".format(To +
                                                               '/' + RequestId), warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def copyDirectorywithNewName(From, To, **kwargs):
    try:
        print 'copyDirectorywithNewName : ' + str(To)
        result = runCommand('cp -R ' + str(From) + "/ " +
                            str(To) + "/", warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def getExecutables(**kwargs):
    result = runCommand("compgen -c", warn=True, timeout=default_timeout, **kwargs)
    return result.stdout


@exceptionHandler
def getExecutablesversion(Name, Command, **kwargs):
    result = runCommand(Name + " " + Command + " 2>&1 | head -1",
                        warn=True, timeout=default_timeout, **kwargs)
    return result.stdout


@exceptionHandler
def getExecutables_rpm(**kwargs):
    result = runCommand("rpm -qa ", warn=True, timeout=default_timeout, **kwargs)
    return result.stdout


@exceptionHandler
def getExecutablesParversion(Command, **kwargs):
    result = runCommand(Command, warn=True, timeout=default_timeout, **kwargs)
    return result.stdout


@exceptionHandler
def cre_hostname_external_ip(**kwargs):
    logs = []
    logs.append(runCommand(
        'echo export HOSTNAME_EXTERNAL_IP=`hostname -i` >> ~/.profile', warn=True, timeout=default_timeout, **kwargs))
    logs.append(runCommand(
        'echo export HOSTNAME_EXTERNAL_IP=`hostname -i` >> ~/.bash_profile', warn=True, timeout=default_timeout, **kwargs))
    logs.append(runCommand(
        'echo export HOSTNAME_EXTERNAL_IP=`hostname -i` >> ~/.bashrc', warn=True, timeout=default_timeout, **kwargs))
    logs.append(
        runCommand('echo export HOSTNAME_EXTERNAL_IP=`hostname -i` >> ~/.cshrc', warn=True, timeout=default_timeout, **kwargs))
    logs.append(runCommand(
        'echo export HOSTNAME_EXTERNAL_IP=`hostname -i` >> ~/.tcshrc', warn=True, timeout=default_timeout, **kwargs))
    logs.append(
        runCommand('echo export HOSTNAME_EXTERNAL_IP=`hostname -i` >> ~/.kshrc', warn=True, timeout=default_timeout, **kwargs))
    logs.append(
        runCommand('export HOSTNAME_EXTERNAL_IP=`hostname -i`', warn=True, timeout=default_timeout, **kwargs))
    return logs


# END Region test
@exceptionHandler
def OSDetails(**kwargs):
    release = runCommand("lsb_release -r", warn=True,
                         timeout=default_timeout, **kwargs)
    description = runCommand(
        "lsb_release -i", warn=True, timeout=default_timeout, **kwargs)
    return {"release": release.stdout.split(':\t')[1], "destribution": description.stdout.split(':\t')[1]}


@exceptionHandler
def PingMachine(machineDetails, **kwargs):
    try:
        result = runCommand("hostname", True, 10, **kwargs)
        if result.return_code != 0:
            raise Exception(
                "Unable to connect machine with host:" + machineDetails["host"])
    except Exception as e:  # catch *all* exceptions
        raise Exception("Unable to connect machine with host:" +
                        machineDetails["host"] + " Error:" + str(e))


@exceptionHandler
def getOSDetails(env, **kwargs):
    if env:
        osdetails = {}
        try:
            alldetails = runCommand(
                "lsb_release -r", warn=True, timeout=default_timeout, **kwargs)
            description = runCommand(
                "lsb_release -i", warn=True, timeout=default_timeout, **kwargs)
            osdetails["release"] = alldetails.split(':\t')[1]
            osdetails["description"] = description.split(':\t')[1]
            return osdetails
        except Exception as e:  # catch *all* exceptions
            print 'Error :' + str(e)
            # raise Exception("Unable to get OS details for host:"+real_host  )
            return None
    else:
        return None


@exceptionHandler
def copyToRemote(source, remote, **kwargs):
    connect = kwargs['connect']
    try:
        if os.path.isdir(source):
            for root, dirs, files in os.walk(source, topdown=True):
                for name in dirs:
                    print "create dir"
                    print os.path.join(root, name).replace(source, remote).replace('\\', '/')
                    connect.run('mkdir -p ' + os.path.join(root,
                                                           name).replace(source, remote).replace('\\', '/'))
                for name in files:
                    print "*** bulk copy file from :" + str(os.path.join(root, name)) + " to " + str(os.path.join(root, name).replace(source, remote).replace('\\', '/'))
                    try:
                        connect.put(os.path.join(root, name), os.path.join(root, name).replace(source, remote).replace('\\', '/'),
                                    preserve_mode=False)
                    except Exception as e:  # catch *all* exceptions
                        print "Failed to copy with error: " + str(e)
        else:
            splited_source = source.replace('\\', '/').rsplit('/', 1)
            file_name = splited_source[1]
            splited_remote = remote.replace('\\', '/').rsplit('/', 1)
            remote_path_without_file_name = splited_remote[0]
            if '.' in remote:
                connect.run('mkdir -p ' + remote_path_without_file_name)
                return connect.put(source, remote)
            else:
                connect.run('mkdir -p ' + remote)
                return connect.put(source, remote + '/' + file_name)
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def copyFromRemote(remote, target, **kwargs):
    try:
        connect = kwargs['connect']
        result = runCommand("cd {}".format(os.path.dirname(
            remote)), warn=True, timeout=default_timeout, **kwargs)
        if result and result.return_code == 0:
            result = connect.get(remote, target)
            return result
        raise ValueError("Directory : " + remote + " not found in remote host")
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def install_docker_containers(vp_home_path, **kwargs):
    try:
        with change_directory(vp_home_path) as cd:
            result = runCommand(cd + 'docker-compose up -d',
                                warn=True, timeout=default_timeout, **kwargs)
            if "ERROR: Error:" in str(result) and  "not found" in  str(result):
                raise Exception("Something went wrong.Please check system logs")
            return result
    except Exception as e:  # catch *all* exceptions
        if result.return_code != 0:
            raise ValueError(result.stdout)
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def unzip(file_name, **kwargs):
    try:
        result = runCommand('unzip -u ' + file_name,
                            warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def zip(zip_name, files_list, **kwargs):
    try:
        result = runCommand(' zip -9 ' + zip_name +
                            ' '.join(files_list), warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def deleteFile(file_name, **kwargs):
    try:
        result = runCommand('rm -f ' + file_name, warn=True,
                            timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def deleteFolder(folder, **kwargs):
    try:
        result = runCommand('rm -r -f ' + folder, warn=True,
                            timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def replaceTextInFile(fileName, oldText, newText, **kwargs):
    try:
        print "FileName: " + str(fileName)
        print "oldText: " + str(oldText).replace('/', '\/')
        print "newText: " + str(newText).replace('/', '\/')
        result = runCommand("sed -i 's/" + str(oldText).replace('/', '\/') + "/" + str(
            newText).replace('/', '\/') + "/g' {}".format(fileName), warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def grantFolderPermissions(perm, folder, **kwargs):
    try:
        result = runCommand('chmod -R ' + str(perm) + ' ' +
                            folder, warn=True, timeout=default_timeout, **kwargs)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))


@exceptionHandler
def grantWritePermissions(folder, **kwargs):
    try:
        result = runCommand('chgrp -R vpdevgroup ' + folder,
                            warn=True, timeout=default_timeout, **kwargs)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))

@exceptionHandler
def give_access_to_vpadmin(folder, **kwargs):
    try:
        result = runCommand('chown vpadmin:vpdevgroup ' + folder,
                            warn=True, timeout=default_timeout, **kwargs)
        return result
    except Exception as e:  # catch *all* exceptions
        print 'Error :' + str(e)
        raise ValueError(str(e))