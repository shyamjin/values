'''
Created on Mar 28, 2018

@author: PDINDA
'''
import logging,os,subprocess
from autologging import logged
import requests,json
from settings import mongodb
from Services import NexusHelperService


''' DEFAULT URL FOR NEXUS is
# DEFAULT URL FOR NEXUS 3 is http://default_nexus_container_name:8081/repository
'''


@logged(logging.getLogger(__name__))
class Nexus3RepositoryServiceHandler(object):
    
    def __init__(self,nexus_details):
        self.db = mongodb
        self.nexus_details =  nexus_details
        self.base_url=nexus_details.get("base_url") #Expected http://default_nexus_container_name:8081/repository
        self.nexus_user=nexus_details.get("repo_user")
        self.nexus_pass=nexus_details.get("repo_pass")
        self.upload_protocol=nexus_details.get("upload_protocol")
        self.mvn_url=nexus_details.get("mvn_url") #+ repo  Expected http://illin4489:8091/repository/
        self.create_repo_url=nexus_details.get("create_repo_url") # Expected : http://vpdev:8081/repository/service/local/repositories
        self.list_all_repositories_url = nexus_details.get("list_all_repositories_url") # Expected : http://illin4489:8091/service/rest/beta/repositories
        self.add_script_url = nexus_details.get("add_script_url") # Expected : http://illin4489:8091/service/rest/v1/script
        self.run_script_url = nexus_details.get("run_script_url")# Expected : http://illin4489:8091/service/rest/v1/script/~/run
        self.remove_script_url = nexus_details.get("remove_script_url")# Expected : http://illin4489:8091/service/rest/v1/script/~
        
        
    def execute_request(self,command,file_to_upload):
        dir_to_switch_to=os.path.dirname(file_to_upload)
        print "execute_request:Execute :" + command + " at: " + os.path.normpath(dir_to_switch_to)
        os.chdir(dir_to_switch_to)
        print "execute_request:Changed Directory to: " + dir_to_switch_to
        print subprocess.check_output(command, shell=True)
        
    def list_all_repositories(self):
        '''
        curl -X GET "http://illin4489:8081/service/rest/beta/repositories" -H "accept: application/json"
        '''    
        headers = {'Content-Type': 'application/json',"Accept":"application/json"}
        # Expected : Expected : http://illin4489:8091/service/rest/beta/repositories
        print " Calling API :"+self.list_all_repositories_url
        response = requests.get(self.list_all_repositories_url, headers=headers, timeout=60, verify=False,auth=\
                                 (self.nexus_user,self.nexus_pass))
        if response.status_code != 200:
            raise Exception("Response " + str(response.status_code) + ' ' + response.reason + '. ' + str(response._content).translate(None, '{"}'))
        print "API Response:"+ str(response._content)
        return json.loads(response._content)
        
    def check_if_repository_exists(self,repo_name):
        all_repos = self.list_all_repositories()
        if type(all_repos) is list and len(all_repos) > 0 :
            for repo in all_repos:
                if repo.get("name") == repo_name: return True
        return False 
    
    def create_repository(self,repo_name):
        '''
        curl -X POST --header 'Content-Type: application/json' http://illin4489:8091/service/rest/v1/script -d '{"name":"testRepo","type":"groovy","content":"repository.createMavenHosted('\''test'\'')"}'
        curl -X DELETE -u admin:admin123 "http://illin4489:8091/service/rest/v1/script/testRepo" -H "accept: application/json"  
        curl -X DELETE "http://illin4489:8091/service/rest/v1/script/testRepo" -H "accept: application/json"
        '''        
        if not self.check_if_repository_exists(repo_name):
            add_script_url=self.add_script_url # Expected : http://illin4489:8091/service/rest/v1/script
            run_script_url=self.run_script_url.replace("~",repo_name) # Expected : http://illin4489:8091/service/rest/v1/script/testRepo/run
            remove_script_url=self.remove_script_url.replace("~",repo_name) # Expected : http://illin4489:8091/service/rest/v1/script/testRepo
            
            print " Calling API :"+add_script_url
            payload={
                        "name": repo_name,
                        "type": "groovy",
                        "content": "import org.sonatype.nexus.repository.storage.WritePolicy; import org.sonatype.nexus.blobstore.api.BlobStoreManager; import org.sonatype.nexus.repository.maven.VersionPolicy; import org.sonatype.nexus.repository.maven.LayoutPolicy; repository.createMavenHosted('"+repo_name+"',BlobStoreManager.DEFAULT_BLOBSTORE_NAME, true, VersionPolicy.RELEASE,WritePolicy.ALLOW, LayoutPolicy.PERMISSIVE)"
                    }
            headers = {'Content-Type': 'application/json',"Accept":"application/json"}
            response = requests.post(add_script_url, headers=headers, data=json.dumps(payload), timeout=60, verify=False,auth=\
                                     (self.nexus_user,self.nexus_pass))
            if response.status_code != 204:
                raise Exception("Response " + str(response.status_code) + ' ' + response.reason + '. ' + str(response._content).translate(None, '{"}'))
            print " Calling API :"+run_script_url
            payload={}
            headers = {'Content-Type': 'text/plain',"Accept":"application/json"}
            response = requests.post(run_script_url, headers=headers,data=json.dumps(payload), timeout=60, verify=False,auth=\
                                     (self.nexus_user,self.nexus_pass))
            if response.status_code != 200:
                raise Exception("Response " + str(response.status_code) + ' ' + response.reason + '. ' + str(response._content).translate(None, '{"}'))
            print " Calling API :"+remove_script_url
            headers = {'Content-Type': 'application/json',"Accept":"application/json"}
            response = requests.delete(remove_script_url, headers=headers, timeout=60, verify=False,auth=\
                                     (self.nexus_user,self.nexus_pass))
            if response.status_code != 204:
                raise Exception("Response " + str(response.status_code) + ' ' + response.reason + '. ' + str(response._content).translate(None, '{"}'))
            print "API Response:"+ str(response._content)
            print repo_name+" Created..."  
        else:
            print repo_name+" already exists.Skipping..."           

    def upload_using_http(self,data_details,file_to_upload):
        '''
        Upload  Url:
        FROM:http://illin4490:8081/repository
        ACTUAL :http://illin4489:8091/repository/vp_builds/fgh/fgh/fgh/fgh-fgh-2.png
        '''

        self.create_repository(data_details.get("repo"))
        
        command = "curl -v -u " + \
                self.nexus_user + ":" + self.nexus_pass + \
                " --upload-file " + os.path.basename(file_to_upload) + \
                " " + data_details.get("file_path")
        self.execute_request(command, file_to_upload)
        
    
    #NOT CALLED FROM CLONE    
    def upload_using_mvn(self,data_details,file_to_upload):
        '''
        Assuming :IF CONNECTING TO NEXUS OF machine VPTEST01
        WE REQUIRE MAVEN PLUGIN TO DO THIS :)
        DOWNLOAD URL:https://maven.apache.org/download.cgi
        HOW TO INSTALL:https://maven.apache.org/install.html
        SET PATH :https://www.cyberciti.biz/faq/unix-linux-adding-path/

        and settings.xml as:
        <?xml version="1.0" encoding="UTF-8"?>
        <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
            <proxies>
                <!-- proxy
             | Specification for one proxy, to be used in connecting to the network.
             |
            <proxy>
              <id>optional</id>
              <active>true</active>
              <protocol>http</protocol>
              <username>proxyuser</username>
              <password>proxypass</password>
              <host>proxy.host.net</host>
              <port>80</port>
              <nonProxyHosts>local.net|some.host.com</nonProxyHosts>
            </proxy>
             -->
                <proxy>
                    <active>true</active>
                    <protocol>http</protocol>
                    <host>genproxy.corp.amdocs.com</host>
                    <port>8080</port>
                    <nonProxyHosts>localhost|127.0.0.1|*.corp.amdocs.com|vptest01</nonProxyHosts>
                </proxy>

            </proxies>

            <profiles>
                <profile>
                    <id>repositories</id>

                    <repositories>
                        <repository>
                            <id>remote-repo</id>
                            <name>remote-repo</name>
                            <url>http://vptest01:8081/nexus/content/repositories/vp_builds</url>
                            <releases>
                                <enabled>true</enabled>
                            </releases>
                            <snapshots>
                                <enabled>true</enabled>
                            </snapshots>
                        </repository>
                    </repositories>
                </profile>
            </profiles>
            <activeProfiles>
                <activeProfile>repositories</activeProfile>
            </activeProfiles>
            <servers>
                <server>
                    <id>releases</id>
                    <username>admin</username>
                    <password>admin123</password>
                </server>
                <server>
                    <id>snapshots</id>
                    <username>admin</username>
                    <password>admin123</password>
                </server>
            </servers>
        </settings>
        
        Upload  Url:
        FROM:http://illin4490:8081/repository
        TO:http://illin4490:8081/repository/vp_builds # WE NEED REPO NAME ALSO IN MVN
        '''
        command ="mvn deploy:deploy-file -DgroupId=" + data_details.get("groupId") \
                + " -DartifactId=" + data_details.get("artifactId") + " -Dversion=" \
                + data_details.get("version") + " -DgeneratePom=true -Dpackaging=" + \
                data_details.get("package") + " -Dclassifier=" + data_details.get("classifier")\
                 + " -DrepositoryId=releases -Durl=" + \
                self.mvn_url + data_details.get("repo") + " -Dfile=" + os.path.basename(file_to_upload)
        self.execute_request(command, file_to_upload)
 
    def upload(self,**keyargs):
        file_to_upload = keyargs.get("file_to_upload",None) # MANDATORY
        if not file_to_upload : raise Exception("Please provide value for key: file_to_upload")
        if not os.path.exists(file_to_upload): raise Exception("Provided value for key:file_to_upload value:"+file_to_upload+" does not exists")
        build_details = keyargs.get("build_details")  # MANDATORY
        if not build_details : raise Exception("Please provide value for key: build_details") 
        NexusHelperService.validate_mandatory_fields(build_details, file_to_upload)
        if self.upload_protocol.lower()  == "http":
            self.upload_using_http(build_details, file_to_upload)
        elif self.upload_protocol.lower()  == "mvn":
            self.upload_using_mvn(build_details, file_to_upload)      
        
    def validate_build_structure(self,**keyargs):
        NexusHelperService.validate_build_data_structure(keyargs.get("build_details"))    
        
    def delete(self,**keyargs):
        print subprocess.check_output("curl --request DELETE --user '"
                                      + self.nexus_user
                                      + ':'
                                      + self.nexus_pass
                                      + "' " + keyargs.get("build_details").get('file_path'), shell=True)
    def download(self,**keyargs):
        # In Deployment we dont want the relative_path dir structure created . It will send False
        NexusHelperService.download_build(keyargs.get("build_details"),keyargs.get("directory_to_export_to"),keyargs.get("create_inside_relative_path",True))
