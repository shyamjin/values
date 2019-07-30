import json
from bson.json_util import dumps
from flasgger import swag_from, validate
from flask import Blueprint, jsonify, request
from DBUtil import Accounts, Users, SystemDetails
from Services.AppInitServices import authService
from settings import mongodb, relative_path
from flask_restplus import Resource
from modules.apimodels import AccountAPIModel
from modules.apimodels.Restplus import api,header_parser



# blueprint declaration
accountAPI = Blueprint('accountAPI', __name__)
#restplus delaration
accountAPINs = api.namespace('account', description='Account Operations') 

# get global db connection
db = mongodb
accountDB = Accounts.Accounts()
userDB = Users.Users(db)
systemDetailsDB = SystemDetails.SystemDetails(db)


@accountAPI.route('/account/all', methods=['GET'])
@authService.unauthorized
@swag_from(relative_path + '/swgger/AccountAPI/getallaccounts.yml')
def getallaccounts():
    return jsonify(json.loads(dumps({"result": "success", "data": accountDB.get_accounts()}))), 200
    


@accountAPI.route('/account/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/AccountAPI/getAccountbyID.yml')
def getAccountbyID(id):
    return jsonify(json.loads(dumps({"result": "success", "data": accountDB.get_account(id)}))), 200
    

@accountAPI.route('/account/new', methods=['POST'])
@authService.authorized
@swag_from(relative_path + '/swgger/AccountAPI/addNewAccounts.yml')
def addNewAccounts():
    data = request.json
    validate(data, 'Accounts', relative_path +
             '/swgger/AccountAPI/addNewAccounts.yml')
    newAccount = request.get_json()
    if (newAccount.get("name"))is None:
        raise Exception("Mandatory fields name to create a new account was not found.")
    if accountDB.get_account_by_name(newAccount.get("name")) is not None:
        raise Exception("Account with name " + newAccount.get("name") + " already exists")
    return jsonify(json.loads(dumps({"result": "success", "message": "The account is saved successfully", "data": {"id": accountDB.add_account(newAccount)}}))), 200
    
@accountAPINs.route('/update/name', methods=['POST'])
class updateAccountByName(Resource):
    @api.expect(header_parser,AccountAPIModel.update_account_input_model,validate=True)
    @api.marshal_with(AccountAPIModel.update_account_response_model)
    @authService.authorized
    def post(self):
        newAccount = request.get_json()
        if (newAccount.get("old_account_name"))is None:
            raise Exception("Mandatory fields old_account_name was not found.")
        if (newAccount.get("new_account_name"))is None:
            raise Exception("Mandatory fields new_account_name was not found.")
        if accountDB.get_account_by_name(newAccount.get("new_account_name")) is not None:
            raise Exception ("Account with name " + newAccount.get("new_account_name") + " already exists")
        accountDB.update_account_by_name(newAccount.get(
            "old_account_name"), newAccount.get("new_account_name"))
        userDB.update_user_account_name(newAccount.get("new_account_name"))
        systemdetails = systemDetailsDB.get_system_details_single()
        if systemdetails:
            data = {"_id": {"oid": str(systemdetails["_id"])}, "account_name": newAccount.get(
                "new_account_name")}
            systemDetailsDB.update_system_details(data)
        return {"result": "success", "message": "The account is updates successfully", "data": {"id": "1"}}, 200

@accountAPI.route('/account/delete/<string:id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/AccountAPI/deleteAccount.yml')
def deleteAccount(id):
    isDeleted = accountDB.delete_account(id)
    return jsonify(json.loads(dumps({"result": "success", "message": "Account was deleted", "data": isDeleted}))), 200
