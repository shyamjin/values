from yapsy.IPlugin import IPlugin



class IBasePlugin(IPlugin):

    def install(self):
        pass

    def uninstall(self):
        pass
