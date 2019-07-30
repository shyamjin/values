chkconfig docker on

groupadd vpdevgroup
groupadd vpadmingroup


useradd -d /home/valuepack/git -s /bin/bash -g vpdevgroup vpdev
usermod --password Unix11! vpdev

useradd -d /home/valuepack -s /bin/bash -g vpadmingroup vpadmin
usermod --password Vpadmin33! vpadmin


groupadd docker
usermod -g docker vpadmin

echo "%docker ALL=/usr/bin/docker,/usr/local/bin/docker-compose" >> /etc/sudoers

chmod g+r /home/valuepack/docker-compose.yml
chmod g+w /home/valuepack/docker-compose.yml


export VP_HOME="/home/valuepack"
################ ALIAS ################

#### GENERAL ####
alias ll='ls -ltrh --color=auto'


#### CD's ####
alias cdvp='cd /home/valuepack'
alias cddpm='cd /home/valuepack/dpm'
alias cdgit='cd /home/valuepack/git'
alias cdjenkins='cd /home/valuepack/jenkins'
alias cdnexus='cd /home/valuepack/nexus'

#### LOG's ####
alias dpmlog='docker logs valuepack_dpm_1 > /tmp/dpm.log;less /tmp/dpm.log'
alias jenkinslog='docker logs valuepack_jenkins_server_1 > /tmp/jenkins.log;less /tmp/jenkins.log'

#### DOCKER's ####
alias dockerstart='systemctl restart docker'
alias dockeru='cd $VP_HOME;docker-compose up -d'
alias dockers='cd $VP_HOME;docker-compose stop'
alias dockerr='cd $VP_HOME;docker-compose restart'

PATH=$PATH:$VP_HOME

export PATH