import os

from mwr.droidhg.modules.common import file_system, shell

class BusyBox(shell.Shell):
    """
    Mercury Client Library: provides utility methods for interacting with Mercury-
    installed Busybox on the Agent.
    """

    def __agentPath(self):
        """
        Get the path to which Busybox is installed on the Agent.
        """

        return self.workingDir() + "/bin/busybox"

    def _localPath(self):
        """
        Get the path to the Busybox binary on the local system.
        """

        return os.path.join(os.path.dirname(__file__) , "..", "tools", "setup", "busybox")

    def busyBoxExec(self, command):
        """
        Execute a command using Busybox.
        """

        return self.shellExec("%s %s" % (self.__agentPath(), command))

    def isBusyBoxInstalled(self):
        """
        Test whether Busybox is installed on the Agent.
        """

        return self.exists(self.__agentPath())

    def installBusyBox(self):
        """
        Install Busybox on the Agent.
        """

        if self.ensureDirectory(self.__agentPath()[0:self.__agentPath().rindex("/")]):
            bytes_copied = self.uploadFile(self._localPath(), self.__agentPath())
    
            if bytes_copied != os.path.getsize(self._localPath()):
                return False
            else:
                self.shellExec("chmod 775 " + self.__agentPath())
                
                return True
        else:
            return False
