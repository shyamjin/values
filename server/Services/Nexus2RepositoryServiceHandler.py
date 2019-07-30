'''
Created on Mar 28, 2018

@author: PDINDA
'''
import logging,os,subprocess,requests,json,shutil
from autologging import logged
from lxml import etree as ET
from settings import mongodb, temp_files_full_path
from Services import NexusHelperService

''' DEFAULT URL FOR NEXUS is
# DEFAULT URL FOR NEXUS 2 is http://default_nexus_container_name:8081/nexus/repository
 '''

@logged(logging.getLogger(__name__))
class Nexus2RepositoryServiceHandler(object):
    
    def __init__(self,nexus_details):
        self.db = mongodb
        self.nexus_details =  nexus_details
        self.base_url=nexus_details.get("base_url") #Expected http://default_nexus_container_name:8081/nexus/repository
        self.nexus_user=nexus_details.get("repo_user")
        self.nexus_pass=nexus_details.get("repo_pass")
        self.nexus_repo_path=nexus_details.get("repo_path") #Expected /home/valuepack/nexus/storage
        self.upload_protocol=nexus_details.get("upload_protocol") #Expected  "http", "mvn","filesystem"
        self.http_url=nexus_details.get("http_url") # Expected :  http://vptestind01:8081/nexus/service/local/artifact/maven/content
        self.mvn_url=nexus_details.get("mvn_url") # Expected : http://"+default_nexus_container_name+":8081/nexus/content/repositories/"
        self.create_repo_url=nexus_details.get("create_repo_url") # Expected : http://vpdev:8081/nexus/repository/service/local/repositories
        self.list_all_repositories_url = nexus_details.get("list_all_repositories_url")# Expected :  http://vptestind01:8081/nexus/service/local/repositories
    
    def execute_request(self,command,file_to_upload):
        dir_to_switch_to=os.path.dirname(file_to_upload)
        print " execute_request:Execute :" + command + " at: " + os.path.normpath(dir_to_switch_to)
        os.chdir(dir_to_switch_to)
        print " execute_request:Changed Directory to: " + dir_to_switch_to
        print subprocess.check_output(command, shell=True)
    
    def list_all_repositories(self):
        '''
        curl -i -v --silent GET -u admin:admin123 http://vptestind01:8081/nexus/service/local/repositories -H "accept: application/json" 2>&1
        list_all_repositories_url = http://vptestind01:8081/nexus/service/local/repositories
        '''    
        headers = {'Content-Type': 'application/json',"Accept":"application/json"}
        
        # Expected :  http://vptestind01:8081/nexus/service/local/repositories
        print " Calling API :"+self.list_all_repositories_url
        response = requests.get(self.list_all_repositories_url,headers=headers, timeout=60, verify=False,auth=\
                                 (self.nexus_user,self.nexus_pass))
        if response.status_code != 200:
            raise Exception("Response " + str(response.status_code) + ' ' + response.reason + '. ' + str(response._content).translate(None, '{"}'))
        print "API Response:"+ str(response._content)
        return json.loads(response._content)
        
    def check_if_repository_exists(self,repo_name):
        all_repos = self.list_all_repositories()
        if all_repos.get("data") and type(all_repos.get("data")) is list and len(all_repos.get("data")) > 0 :
            for repo in all_repos.get("data"):
                if repo.get("name") == repo_name: return True
        return False    
    
    def create_repository(self,repo_name):
        '''
        #base_url = http://default_nexus_container_name:8081/nexus/repository
        '''
        nexus_url='-u '+self.nexus_user+ \
                    ':'+self.nexus_pass+ \
                    ' '+(self.create_repo_url+" 2>&1").replace("\\","/")
        
        print " Calling API :"+nexus_url
        if not self.check_if_repository_exists(repo_name):            
            file_path=temp_files_full_path+repo_name+'.xml'
            root = ET.Element('repository')
            data = ET.SubElement(root, 'data')
            id = ET.SubElement(data, 'id')                            
            id.text = repo_name
            name = ET.SubElement(data, 'name')
            name.text = repo_name
            repoType = ET.SubElement(data, 'repoType')
            repoType.text = 'hosted'
            repoPolicy = ET.SubElement(data, 'repoPolicy')
            repoPolicy.text = 'RELEASE'
            providerRole = ET.SubElement(data, 'providerRole')
            providerRole.text = 'org.sonatype.nexus.proxy.repository.Repository'
            provider = ET.SubElement(data, 'provider')
            provider.text = 'maven2'
            format = ET.SubElement(data, 'format')
            format.text = 'maven2'
            writePolicy = ET.SubElement(data, 'writePolicy')
            writePolicy.text = 'ALLOW_WRITE'
            browseable = ET.SubElement(data, 'browseable')
            browseable.text = 'true'
            exposed = ET.SubElement(data, 'exposed')
            exposed.text = 'true'
            indexable = ET.SubElement(data, 'indexable')
            indexable.text = 'true'
            notFoundCacheTTL = ET.SubElement(data, 'notFoundCacheTTL')
            notFoundCacheTTL.text = '1440'
            downloadRemoteIndexes = ET.SubElement(data, 'downloadRemoteIndexes')
            downloadRemoteIndexes.text = 'false'
            print ET.tostring(root, pretty_print=True, xml_declaration=True)
            tree = ET.ElementTree(root)
            print "Creating file : "+file_path
            tree.write(file_path, pretty_print=True, xml_declaration=True)
            new_repo_url = 'curl -i -H "Accept: application/xml" -H "Content-Type: application/xml" -f -X POST -v -d "@'+file_path+'" '+nexus_url                            
            print "Execute : "+new_repo_url
            print "Output subprocess - "+str(subprocess.check_output(new_repo_url, shell=True))
            print "Removing file : "+file_path
            os.remove(file_path)
        else:
            print repo_name+" already exists.Skipping..."       
    
                          
    def upload_using_http(self,data_details,file_to_upload):
        '''
        Upload  Url:
        FROM:http://illin4490:8081/nexus/repository
        TO:http://illin4490:8081/nexus/service/local/artifact/maven/content
        '''
        
        command = "curl -v -F r=" + data_details.get("repo") + " -F hasPom=false -F e=" + \
            data_details.get("extension") + " -F g=" + data_details.get("groupId") + " -F a=" + \
            data_details.get("artifactId") + " -F v=" + data_details.get("version") + " -F p=" + \
            data_details.get("package") + " -F c=" + data_details.get("classifier") \
            + "  -F file=@" + os.path.basename(file_to_upload) + \
            " -u " + self.nexus_user \
            + ":" + self.nexus_pass \
            + " " + self.http_url
        
        self.create_repository(data_details.get("repo"))
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
        FROM:http://illin4490:8081/nexus/repository
        TO:http://illin4490:8081/nexus/content/repositories/vp_builds # WE NEED REPO NAME ALSO IN MVN
        '''
        command = "mvn deploy:deploy-file -DgroupId=" + data_details.get("groupId") \
            + " -DartifactId=" + data_details.get("artifactId") + " -Dversion=" + data_details.get("version")\
             + " -DgeneratePom=true -Dpackaging=" + data_details.get("package") + \
            " -Dclassifier=" + data_details.get("classifier") + " -DrepositoryId=releases -Durl=" \
            + self.mvn_url + data_details.get("repo") + " -Dfile=" + os.path.basename(file_to_upload)
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
        elif self.upload_protocol.lower()  == "filesystem":
            self.copy_artifact(build_details, file_to_upload)
        
    def copy_artifact(self,build_details,file_to_copy):
        file_name=os.path.basename(file_to_copy)
        print "copy_artifact: Need to copy file to FileSystem"
        nexus_path = os.path.normpath(os.path.join(self.nexus_repo_path, build_details.get("relative_path")))
        print "copy_artifact: Trying to create directories :" + nexus_path
        if not os.path.exists(nexus_path):os.makedirs(nexus_path)
        print "copy_artifact: Copying file :" + file_name
        shutil.copy(file_to_copy, nexus_path)
        print "copy_artifact: Copying file completed for :" + file_name + " at path :" + nexus_path
     
    def validate_build_structure(self,**keyargs):
        NexusHelperService.validate_build_data_structure(keyargs.get("build_details"))
        
    def delete(self,**keyargs):
        print "curl --request DELETE --user '"+ self.nexus_user+ ':'+ self.nexus_pass\
                                    + "' " + keyargs.get("build_details").get('file_path')
        print subprocess.check_output("curl --request DELETE --user '"
                                      + self.nexus_user
                                      + ':'
                                      + self.nexus_pass
                                      + "' " + keyargs.get("build_details").get('file_path'), shell=True)
        print "{} was removed from nexus..".format(keyargs.get("build_details").get('file_path'))    
        
    def download(self,**keyargs):
        # In Deployment we dont want the relative_path dir structure created . It will send False
        NexusHelperService.download_build(keyargs.get("build_details"),keyargs.get("directory_to_export_to"),keyargs.get("create_inside_relative_path",True))
