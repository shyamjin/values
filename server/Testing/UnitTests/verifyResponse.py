import json
def PositiveTesting(response):
    if(response.status_code!=200):
        print "FAILURE"
        raise Exception(str(response.text))
    print "SUCCESS"    

def NegativeTesting(response,message):
    if(response.status_code==200):
        print "FAILURE"
        raise Exception(str(response.text))
    json_data = json.loads(response.text)
    if message is not None:
        if(message not in json_data.get("message")):
            print "FAILURE"
            raise Exception(str(response.text))
    print "SUCCESS"