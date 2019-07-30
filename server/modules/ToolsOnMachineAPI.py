from flask import Blueprint
from DBUtil import ToolsOnMachine
from Services.AppInitServices import authService
from settings import mongodb
from modules.apimodels import ToolsOnMachineAPIModel
from flask_restplus import Resource,marshal_with
from modules.apimodels.Restplus import api, header_parser
from functools import wraps

# blueprint declaration
toolsOnMachineAPI = Blueprint('toolsOnMachineAPI', __name__)
toolsOnMachineAPINs = api.namespace('deployed', description='Deployed Tools Operations')


# get global db connection
db = mongodb
toolsOnMachineDB = ToolsOnMachine.ToolsOnMachine(db)

def selective_marshal_with(responseModel, noneResponseModel):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func2 = marshal_with(responseModel)(func)
            response=func2(*args, **kwargs)
            res= response[0];
            if res.get("data").get("create_date"):
                return response
            else:
                lst = list(response)
                lst[0]["data"] = None
                return tuple(lst)
        return wrapper
    return decorator

@toolsOnMachineAPINs.route('/view/machine_id/<machine_id>/parent_entity_id/<parent_entity_id>/build_id/<build_id>', methods=['GET'])
@api.doc(params={'machine_id':'machine_id','parent_entity_id':'parent_entity_id','build_id':'build_id'})
class getToolsOnMachineByMachineIdParentEntityIdAndBuildId(Resource):
    @api.expect(header_parser, validate=True)
    @selective_marshal_with(ToolsOnMachineAPIModel.getDeployedtoolResponseModel,ToolsOnMachineAPIModel.getDeployedtoolResponseModelNone)
    @authService.authorized
    def get(self, machine_id, parent_entity_id, build_id):
        data = toolsOnMachineDB.get_tools_on_machine_by_filter(machine_id, parent_entity_id, build_id)
        return {"result": "success", "data": data},200
