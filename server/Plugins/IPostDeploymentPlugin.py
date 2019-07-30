from Plugins.IBasePlugin import IBasePlugin


class IPostDeploymentPlugin(IBasePlugin):

    def print_name(self):
        '''
        General description:
        Args:  none

         Returns:
                None
        '''
        print "This is plugin IPostDeploymentPlugin"
