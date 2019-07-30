import logging
from flask import Blueprint
from flask_restplus import Api, apidoc
from autologging import logged


log = logging.getLogger(__name__)

api_v1 = Blueprint('api', __name__)
api = Api(api_v1, version='1.0', title='eDPM APIs', description='eDPM API documentation', doc='/doc/'
)
header_parser = api.parser()
header_parser.add_argument('token', '', required=False, help="Either token or access-token is required", location='headers')
header_parser.add_argument('access-token', '', required=False, help="Either token or access-token is required", location='headers')

@logged(logging.getLogger(__name__))
@api.documentation
def swagger_ui():
    return apidoc.ui_for(api)

@logged(logging.getLogger(__name__))
@api.errorhandler(Exception)
def handle_custom_exception(error):
    return {"result": "failed", "message": str(error)}, 404

@logged(logging.getLogger(__name__))
@api.errorhandler
def default_error_handler(e):
    return {"result": "failed", "message": str(e)}, 404
