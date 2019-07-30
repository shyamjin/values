FROM illin4489.corp.amdocs.com:10005/vp_base:4

ARG TEST_HOST=10.234.124.35

#Set ARG Dynamic
ARG DPM_TYPE
ARG DPM_VERSION
ARG DPM_PIPELINE_NUMBER
ARG DPM_BUILD_NUMBER
ARG BUILD_DATE
USER root
ENV http_proxy=http://genproxy.amdocs.com:8080 https_proxy=http://genproxy.amdocs.com:8080 no_proxy=localhost,127.0.0.1,.corp.amdocs.com
COPY server/requirements.txt /requirements.txt
COPY init.sh /usr/bin/init.sh
COPY / /home/dpm
RUN  mkdir -p /tmp/download \
    && curl -L -k https://get.docker.com/builds/Linux/x86_64/docker-1.9.1.tgz | tar -xz -C /tmp/download \
    && mv /tmp/download/usr/local/bin/docker* /usr/local/bin/ \
    && rm -rf /tmp/download \
    && chmod +x requirements.txt && pip install --upgrade pip &&  pip install --no-cache-dir -r requirements.txt \
    && echo "vpadmin        ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers \
    && rm -rf /home/dpm/.g* /home/dpm/client/Gruntfile.js /home/dpm/server/Testing \
    && useradd -ms /bin/bash vpadmin && mkdir -p /home/dpm/temp \
    && chown vpadmin /home/dpm/temp \
    && chmod 777 /home/dpm/temp \
    && chmod +x /usr/bin/init.sh \
    && yes|cp -fv /home/dpm/server/Services/docker/jenkins_v1.651.3/settings.xml /usr/local/apache-maven/apache-maven-3.3.9/conf/ \
    && ln -s /home/dpm/server/static/files /home/dpm/client/static/files \
    && ln -s /home/dpm/server/static/DPMDataUpdates /home/dpm/client/static/DPMDataUpdates \
    && ln -s /home/dpm/server/static/DPMDistributionCenter /home/dpm/client/static/DPMDistributionCenter \
    && ln -s /home/dpm/server/archives /home/dpm/client/static/archives \
    && ln -s /home/dpm/server/Plugins /home/dpm/client/static/Plugins \
    && cd /etc/postfix && sed -i -- 's/#relayhost = uucphost/relayhost = umg.corp.amdocs.com/g' main.cf \
    && rm -rf /home/dpm/installations && yum clean all && rm -rf /var/cache/yum && rm -rf /var/tmp/yum-* && rm -rf /root/.composer/cache && rm -rf /home/*/.composer/cache \
    && git clone http://gollum:gollum123@illin4467.corp.amdocs.com/GSSPSO/DeploymentManger.wiki.git /home/dpm/wiki \
    && cd /home/dpm/wiki && zip -r  wiki.zip .git * \
    && find . ! -name 'wiki.zip' -type f -exec rm -f {} +
EXPOSE 8000
ENV http_proxy="" https_proxy="" no_proxy="" M2_HOME="/usr/local/apache-maven/apache-maven-3.3.9" M2="/usr/local/apache-maven/apache-maven-3.3.9/bin" JAVA_HOME="/usr/local/java/jdk1.8.0_05" PATH="$PATH:/usr/local/apache-maven/apache-maven-3.3.9/bin:/usr/local/java/jdk1.8.0_05" KUBE_MODE=$KUBE_MODE TEST_HOST=$TEST_HOST DPM_TYPE=$DPM_TYPE DPM_VERSION=$DPM_VERSION DPM_PIPELINE_NUMBER=$DPM_PIPELINE_NUMBER DPM_BUILD_NUMBER=$DPM_BUILD_NUMBER BUILD_DATE=$BUILD_DATE
WORKDIR /home/dpm
CMD ["/usr/bin/init.sh"]