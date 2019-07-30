import ntpath,json
from bson import ObjectId
from datetime import datetime
from bson.errors import InvalidId


def get_file_name_from_path(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if type(o) in [ObjectId,datetime] :
            return str(o)        
        return json.JSONEncoder.default(self, o)

def is_valid_obj_id(oid):
    try:
        ObjectId(oid)
        return True
    except (InvalidId, TypeError):
        return False 