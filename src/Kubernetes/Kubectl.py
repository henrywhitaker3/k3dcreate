import subprocess
import sys
from Constants.Kubectl import Kubectl as KubectlC
from Exceptions.KubectlException import KubectlException

class Kubectl:
    def __init__(self) -> None:
        self.namespace = 'default'

    def forNamespace(self, namespace: str) -> 'Kubectl':
        self.namespace = namespace

        return self

    def create(self, type: str, arguments: list) -> None:
        self.__runKubectlCommand([KubectlC.CREATE, type] + arguments)

    def __runKubectlCommand(self, arguments: list) -> None:
        defaultArgs = ['kubectl', '--namespace', self.namespace]

        process = subprocess.Popen(
            (defaultArgs + arguments), stdout=subprocess.PIPE
        )

        for line in iter(process.stdout.readline, b""):
            sys.stdout.write(line.decode("utf-8"))

        process.wait()

        if process.returncode != 0:
            raise KubectlException(
                'Something went wrong running command:' + str(defaultArgs + arguments)
            )
