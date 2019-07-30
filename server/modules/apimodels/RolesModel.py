from modules.apimodels.Restplus import api
from flask_restplus import fields


role_model = api.model('Roles Model', {
     'role_id': fields.String(required=True, description='Role ID',default="ga")
    ,'permissiongroup': fields.List(fields.String,required=True, description='Permission Group ids')    
})


update_model = api.model('Roles Update Model', {
    'roles': fields.List(fields.Nested(role_model),required=True, description='Role Details')    
})
