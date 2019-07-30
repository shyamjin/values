#usr/bin/bash

echo "Hi $(id -u -n),We need some information from you.."
read -p "Enter Your DPM_DB_HOST: "  DPM_DB_HOST
read -p "Enter Your DPM_BUILD_NUMBER: "  DPM_BUILD_NUMBER
read -p "Enter Your DPM_PIPELINE_NUMBER: "  DPM_PIPELINE_NUMBER
read -p "Enter Your DPM_VERSION: "  DPM_VERSION

echo "ThankYou!!"

export DEV_MODE="False"
export DOCKER_IND="False"
export DPM_BUILD_NUMBER=$DPM_BUILD_NUMBER
export DPM_DB_HOST=$DPM_DB_HOST
export DPM_DB_PORT="27018"
export DPM_PIPELINE_NUMBER=$DPM_PIPELINE_NUMBER
export DPM_PORT="8000"
export DPM_TYPE="dpm_master"
export DPM_VERSION=$DPM_VERSION
export MONGO_SECURED="True"
export BUILD_DATE=$BUILD_DATE
HOME='/home/CLservices/DeploymentManger'

echo #######################
printenv | grep DPM
echo #######################
cd $HOME
if [ ! -e $HOME/log/ ]
then
    mkdir log
fi
if [ -e $HOME/log/dp.log ]
then
    mv $HOME/log/dp.log $HOME/log/dp.log_`date +"%Y%m%d_%H%M%S"`
fi

ps axf | grep 'gunicorn' | grep -v grep | awk '{print "kill -9 " $1}' | sh

nohup gunicorn -b 0.0.0.0:8000 --certfile=ssl/server.cer --keyfile=ssl/server.key main --timeout 5000  -k gevent --worker-connections 1001 --timeout 600 --access-logfile $HOME/log/dp.log > $HOME/log/dp.log 2>&1 &

