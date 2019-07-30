from modules.apimodels import FlexAttributesModel
from DBUtil import FlexibleAttributes, DeploymentUnit,Machine,MachineGroups
from settings import mongodb 

faDB = FlexibleAttributes.FlexibleAttributes()
DeploymentUnitDb = DeploymentUnit.DeploymentUnit()
MachineDb = Machine.Machine(mongodb)
MachineGroupsDb = MachineGroups.MachineGroups(mongodb)
def validate_fa(fa_details):
    validate_entity(fa_details['entity'])
    validate_type(fa_details)


def validate_fa_update(fa_details):
    validate_fa(fa_details)
    fa_db_values = faDB.get_by_id(fa_details.get('_id').get('oid'))
    if fa_db_values is None:
        raise Exception("Couldn't find FA with ID: " + fa_details.get('_id').get('oid'))
    if (fa_db_values.get('entity') != fa_details.get('entity')) \
        or (fa_db_values.get('name') != fa_details.get('name')) \
            or (fa_db_values.get('type') != fa_details.get('type')):
            raise Exception("Following fields can't beupdated: entity, name and type")        
    for value in fa_db_values.get("valid_values"):
        if value not in fa_details.get("valid_values"):
            if str(fa_details.get('entity')) == "DeploymentUnit" :
                for du in DeploymentUnitDb.GetDeploymentUnitByFA(fa_details.get('name')):
                    if value in du.get("flexible_attributes").get(fa_details.get('name')).split(",") :
                        raise Exception("The Valid value "+str(value)+" of FA "+str(fa_details.get('name'))+" cannot be removed/updated as it is already assigned to a deployment unit: "+str(du.get("name")))
            if str(fa_details.get('entity')) == "Machine" :
                for machine in MachineDb.GetMachineByFA(fa_details.get('name')):
                    if value in machine.get("flexible_attributes").get(fa_details.get('name')).split(",") :
                        raise Exception("The Valid value "+str(value)+" of FA "+str(fa_details.get('name'))+" cannot be removed/updated as it is already assigned to a machine: "+str(machine.get("machine_name")))
            if str(fa_details.get('entity')) == "MachineGroup" :
                for machineGroup in MachineGroupsDb.GetMachineGroupByFA(fa_details.get('name')):
                    if value in machineGroup.get("flexible_attributes").get(fa_details.get('name')).split(",") :
                        raise Exception("The Valid value "+str(value)+" of FA "+str(fa_details.get('name'))+" cannot be removed/updated as it is already assigned to a machine group: "+str(machineGroup.get("group_name")))
                


def validate_entity(entity):
    if not FlexAttributesModel.Entities.has_name(entity):
        raise Exception("Invalid entity value: " + entity)


def validate_type(fa_details):
    fa_type = fa_details['type']
    if not FlexAttributesModel.FaTypes.has_name(fa_type):
        raise Exception("Invalid type value: " + fa_type)
    if (fa_type == FlexAttributesModel.FaTypes.Select.name) or (fa_type == FlexAttributesModel.FaTypes.MultiSelect.name):
        if ('valid_values' not in fa_details) or (len(fa_details['valid_values']) == 0):
            raise Exception("Valid values is requested for this FA type")
        validate_valid_values(fa_details['valid_values'])
    else:
        if ('valid_values' in fa_details) and (len(fa_details['valid_values']) > 0):
            raise Exception("Valid values are allowed only for types: " + FlexAttributesModel.FaTypes.Select.name + " and " + FlexAttributesModel.FaTypes.MultiSelect.name)


def validate_valid_values(valid_values):
    for value in valid_values:
        if "," in value:
            raise Exception("Valid value '" + value + "' contains invalid character ','")


def validate_entity_value(entity=0, fa_details={}):
    # CHECK IF THE ENTITY PROVIDED IS VALID
    assert (FlexAttributesModel.Entities.has_name(entity)),"Invalid entity for FA"
    for fa_name in fa_details.keys():
        error_suffix = " for entity: "+entity+", attribute name: "+fa_name
        fa_db_value = faDB.get_by_name_and_entity(fa_name, entity)
        # CHECK IF ANY SUCH ENTITY EXISTS FOR GIVEN fa_name and entity
        assert (fa_db_value),"No such FA was found"+error_suffix
        
        # NEW ERROR
        error_suffix = " for entity: "+entity+", attribute title: "+fa_db_value.get("title",fa_name)
        
        # CHECK IS VALUE HAS BEEN PROVIDED FOR MANDATORY FA's
        if fa_db_value.get("is_mandatory",False): 
            assert (fa_details.get(fa_name)),"Value is mandatory"+error_suffix
        # CHECK IF GIVEN VALUE IS COMMA SEPERATED.IF SO THEN SPLIT IT TO LIST
        # CHECK IF THERE ARE ANY RECORDS IN FIRST LIST WHICH ARE NOT PRESENT IN SECOND
        if fa_db_value.get("is_mandatory",False) and fa_db_value.get("valid_values"):
            assert (len(set(fa_details.get(fa_name).split(",")) - set(fa_db_value.get("valid_values"))) < 1),\
                    "Invalid input value was found "+error_suffix 


def is_fa_exists(fa_details):
    fa_db_value = faDB.get_by_name_and_entity(fa_details.get('name'), fa_details.get('entity'))
    return not (fa_db_value is None)
