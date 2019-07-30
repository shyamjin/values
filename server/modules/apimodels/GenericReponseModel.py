from modules.apimodels.Restplus import api
from flask_restplus import fields
import time,json
from bson.json_util import dumps

genericId_response_model = api.model('DB ID', {
    '_id': fields.String(required=True, description='DB ID')
})

generic_response_model = api.model('Generic response', {
    'message': fields.String(required=True, description='Response message'),
    'result': fields.String(required=True, description='Response result (success/failed)')
})

oid_model = api.model('DB OID', {
    'oid': fields.String(required=True, description='DB ID')
})

class response_data_model(fields.Raw):
    def format(self, value):
        return json.loads(dumps(value))

class input_id_oid_model(fields.Raw):
    def format(self, value):
        return {"oid":str(value)}
    
class response_id_oid_model(fields.Raw):
    def format(self, value):
        return {"$oid":str(value)}
    
class response_date_model(fields.Raw):
    def format(self, value):
        if value:
            return {"$date":int(time.mktime(value.timetuple()))}
        else:
            return None
    
generic_post_response_model = api.inherit('Generic POST response', generic_response_model, {
    'data': fields.Nested(genericId_response_model, required=True, description='response data model'),
})

generic_date_model = api.model('date inner $date', {
    '$date' : fields.Integer(required=True, description='Update date with long format')
})

generic_update_date_model = api.model('Update date', {
    'update_date' : fields.Nested(generic_date_model, required=True, description='Update date')
})

dynamic_response_model = api.model('Generic Data response', {
    'message': fields.String(required=True, description='Response message'),
    'result': fields.String(required=True, description='Response result (success/failed)'),
    'data': response_data_model(attribute='data',required=True, description='')
})
