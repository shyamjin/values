from DBUtil import DeploymentUnitApprovalStatus
from pymongo.errors import DuplicateKeyError

deploymentUnitApprovalStatusDB = DeploymentUnitApprovalStatus.DeploymentUnitApprovalStatus()

def add_approval_status(data):
    if deploymentUnitApprovalStatusDB.GetDeploymentUnitApprovalStatusByName(data.get("name")):
        raise Exception("The status with name : "+data.get("name")+" already exists")
    return deploymentUnitApprovalStatusDB.AddDeploymentUnitApprovalStatus(data)


def update_approval_status(data):
    if not deploymentUnitApprovalStatusDB.GetDeploymentUnitApprovalStatusById(data.get("_id").get("oid")):
        raise Exception("The status exists with the object id : "+ data.get("_id").get("oid"))
    try:
        return deploymentUnitApprovalStatusDB.UpdateDeploymentUnitApprovalStatus(data)
    except DuplicateKeyError as e:
        raise DuplicateKeyError("The status exists with same name")
    
def delete_approval_status(object_id):
    approval_status=deploymentUnitApprovalStatusDB.GetDeploymentUnitApprovalStatusById(object_id)
    if not approval_status:
        raise Exception("The status does not exists with the object id : "+ object_id)
    if approval_status.get("name").lower()=="created":
        raise Exception("The status with name 'Created' is not allowed to be removed")
    return deploymentUnitApprovalStatusDB.DeleteDeploymentUnitApprovalStatus(object_id)
    