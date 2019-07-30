'''
Created on Apr 27, 2018

@author: PDINDA
'''
import base64
import hashlib
import inspect
import os
from Crypto.Cipher import AES
from pymongo import MongoClient
import time

cuttentPath = os.path.dirname(os.path.abspath(__file__))

def decrypt(enc):
    global key
    key1=hashlib.sha256(key.encode()).digest()
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key1, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

# Password Key
myvars = {}
with open(os.path.join(cuttentPath, 'secret.p')) as myfile:
    for line in myfile:
        name, var = line.partition("=")[::2]
        myvars[name.strip()] = str(var)
if not myvars.get("key"):
    raise ValueError("Key used to encrypt/decrypt password was not found")
key = myvars["key"]    


mongo_cred_path = os.path.join(cuttentPath, 'credentials.txt')
# CONNECT MONGO
client = MongoClient(
    str(os.environ.get("DPM_DB_HOST","mongo_sec")), int(os.environ.get("DPM_DB_PORT","64254")))

count = 1
while True:
    print "DPM : Hello Mongo Db, Are you awake ?"
    try:
        myvars = {}
        if str(os.environ.get("MONGO_SECURED","true")).lower() == 'true':
            if os.environ.get("MONGO_USER") and os.environ.get("MONGO_PASS"):
                client.admin.authenticate(
                decrypt(str(os.environ.get("MONGO_USER")).strip()),decrypt(str(os.environ.get("MONGO_PASS")).strip()))
            else:
                with open(mongo_cred_path) as myfile:
                    for line in myfile:
                        name, var = line.partition("=")[::2]
                        myvars[name.strip()] = str(var)
                    if not myvars.get("mongo_user") or not myvars.get("mongo_pass"):
                        raise ValueError("Key used to encrypt/decrypt mongo was not found")
                    client.admin.authenticate(
                        decrypt(str(myvars["mongo_user"]).strip()),decrypt(str(myvars["mongo_pass"]).strip()))
        
        db = client.DeploymentManager
        db.collection_names()
        print "Mongo Db :Yes I am awake !! How can i help you ? "
        print "DPM : ahhhh.. I was asked to check if you were awake:D :D :D :D. Check Passed.. "
        break
    except Exception:
        print "DPM: Mongo Db is still sleeping .... Can you plz ask the gentleman to wake up ?"
        print "DPM: I will try "+str(5-count)+" more times..."
        if count == 5 : raise Exception("DPM: Am done trying!! Lets Fail this !!!")
        time.sleep(10)
        pass 
    count+=1   

''' MONGO END'''