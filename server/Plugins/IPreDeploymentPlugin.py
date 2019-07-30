from Plugins.IBasePlugin import IBasePlugin


class IPreDeploymentPlugin(IBasePlugin):

    def print_name(self):
        '''
           General description:prints the name of plugin
           Args:  none

            Returns:
                   None
       '''

    print "This is plugin PreDeploymentBasePLugin"
