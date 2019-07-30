from datetime import datetime
import json
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify
from Services.AppInitServices import authService
from settings import relative_path
import time
import os
from concurrent.futures import ThreadPoolExecutor
# blueprint declaration
generalAPI = Blueprint('generalAPI', __name__)


def MyThread ():
    time_to_restart=30
    while True:
        
        print "*******************************************************************************************************************"
        print "Server will restart in :" + str(time_to_restart) + " seconds"
        print "*******************************************************************************************************************"
        time.sleep(1)
        time_to_restart=time_to_restart-1
        if time_to_restart<=0:
            break
    os.system("pkill gunicorn")
    
    
# fix by Surendra for scheduled_date . This API provide Server Current time.
@generalAPI.route('/currenttime', methods=['GET'])
@authService.unauthorized
@swag_from(relative_path + '/swgger/GeneralAPI/CurrentServerTime.yml')
def CurrentServerTime():
    ServerCurrentTime = datetime.now()
    return jsonify(json.loads(dumps({"result": "success", "CurrentTime": ServerCurrentTime.isoformat()}))), 200


# The docker-compose file must have 'restart: always' for the dpm container configuration
@generalAPI.route('/server/restart', methods=['POST'])
@authService.authorized
def restart():
    print "*************************************************************************************************"
    print "ABOUT TO RESTART THE SERVER..........................."
    print "*************************************************************************************************"
    pool = ThreadPoolExecutor(1,__name__+".restart")
    pool.submit(MyThread)
    return jsonify(json.loads(dumps({"result": "success", "message":"server will restart in 30 seconds"}))), 200        
