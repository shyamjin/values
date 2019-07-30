#!/bin/bash


HOME=/home/dpm
SERVER_HOME=$HOME/server
LOG=$HOME/init.log
SSL=$SERVER_HOME/ssl
echo " " > $LOG
echo "ENV VARIABLES TO BE USED" | tee -a $LOG
echo "USE SSL: $USE_SSL" | tee -a $LOG
echo $HOME,$SERVER_HOME,$SSL,$DEV_MODE| tee -a $LOG
env | grep -e DPM -e DOCKER -e BUILD -e HOST -e IP -e ACCOUNT | sort | tee -a $LOG
if [ ! -f "$SERVER_HOME/upgradeScript.pyc" ]
then
    echo "File '$SERVER_HOME/upgradeScript.pyc' not found.Exiting" | tee -a $LOG
  	exit 1
else
	echo "File '$SERVER_HOME/upgradeScript.pyc' was found." | tee -a $LOG
fi

echo "############################################" | tee -a $LOG
echo "Trying to run MongoRunningScript.pyc" | tee -a $LOG
echo "############################################" | tee -a $LOG
python $SERVER_HOME/MongoRunningScript.pyc 

if [ $? -eq 0 ]; then
  echo "Good News!! Now we can start with system upgrade." | tee -a $LOG
else
	echo "Bad News!! We were not able to validate Mongo Db connection." | tee -a $LOG
  exit 1
fi



echo "############################################" | tee -a $LOG
echo "Trying to run upgradeScript.pyc" | tee -a $LOG
echo "############################################" | tee -a $LOG
python $SERVER_HOME/upgradeScript.pyc 
if [ $? -eq 0 ]; then
  echo "UpgradeScript worked fine.Starting project" | tee -a $LOG
else
	echo "UpgradeScript failed.Exiting as its not safe to start project" | tee -a $LOG
  exit 1
fi

echo "############################################" | tee -a $LOG
echo "Trying to copy /home/dpm/wiki/*.md to /home/dpm/gollum" | tee -a $LOG
echo "############################################" | tee -a $LOG
/usr/bin/rm -rf /home/dpm/gollum/*.md /home/dpm/gollum/.git && /usr/bin/unzip -q /home/dpm/wiki/wiki.zip -d /home/dpm/gollum

echo "#################DONE###########################" | tee -a $LOG

if [ "$WEBSERVER" == "nginx" ] ; then
	echo "###### NGNIX & UWSGI HOSTING ENABLED ######" | tee -a $LOG
	if [ -z "$USE_SSL" ] || [ "$USE_SSL" = true ] ; then
	    echo "######HTTPS MODE######" | tee -a $LOG
	    uwsgi uwsgi_https.ini | tee -a $LOG  #--stats 127.0.0.1:9191
	else
		echo "######HTTP MODE######" | tee -a $LOG
	    uwsgi uwsgi_http.ini | tee -a $LOG  #--stats 127.0.0.1:9191
	fi

else
	echo "###### GUNICORN & GEVENT HOSTING  ENABLED ######" | tee -a $LOG
	if [ -z "$USE_SSL" ] || [ "$USE_SSL" = true ] ; then
	    echo "######HTTPS MODE######" | tee -a $LOG
	    cd $SERVER_HOME && gunicorn -b 0.0.0.0:8000 --certfile=$SSL/server.cer --keyfile=$SSL/server.key main -k gevent --worker-connections 1001 --timeout 600 | tee -a $LOG #--workers=4 --threads=12
	else
		echo "######HTTP MODE######" | tee -a $LOG
	    cd $SERVER_HOME && gunicorn -b 0.0.0.0:8000 main -k gevent --worker-connections 1001 --timeout 600 --log-level=critical | tee -a $LOG  #--workers=4 --threads=12
	fi
	
fi


