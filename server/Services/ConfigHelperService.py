'''
Created on Jun 30, 2017

@author: PDINDA
'''

from DBUtil import Config
from settings import mongodb


configdb = Config.Config(mongodb)


def load_common_configuration(obj):
    try:
        """Loads configuration required to run service using config_id"""
        obj.result = configdb.getConfigByConfigId(obj.config_id)
        if obj.result:
            # CHECK IF NEED TO SCHEDULE THIS SERVICE
            if str(obj.result.get("enable").lower()) == "true":
                obj.start_service = True
            else:
                obj.start_service = False
            obj.service_type = str(obj.result.get("type")).lower()
            if obj.service_type not in ["interval", "scheduled"]:
                raise ValueError(
                    'Invalid scheduler type found.Valid values are "interval","scheduled"')
            if obj.service_type in ["scheduled"]:
                obj.hours = str(obj.result.get("hrs"))
                obj.minutes = str(obj.result.get("min"))
                if not obj.hours and not int(obj.minutes):
                    raise ValueError('The given hrs,min is invalid')
            elif obj.service_type in ["interval"]:
                obj.interval_given = float(obj.result['intervalGiven'])
                if (obj.interval_given <= 0):
                    raise ValueError(
                        ' Run interval cannot be less than 1')
        else:
            raise ValueError(
                'Configuration to run this service was found')
    except Exception as exp:
        raise Exception("Failed to load Configuration with error: " + str(exp))


def run(function):
    def wrapper(self, *args, **kwargs):
        try:
            configdb.UpdateStartTime(
                int(self.config_id), "Running", "Job Started")
            function(self, *args, **kwargs)  # RUN THE METHOD
            configdb.UpdateEndTime(int(self.config_id),
                                   'Success', "Job Completed")
        except Exception as e_value:
            configdb.UpdateEndTime(
                int(self.config_id), 'Failed', "Job Failed with error: " + str(e_value))
    return wrapper
