import re
import subprocess
import sys
from Constants.Helm import Helm as HelmC
from Exceptions.HelmException import HelmException

class Helm:
    def forRepo(self, name: str, url: str) -> 'Helm':
        self.__addRepo(name, url)

        return self

    def forNamespace(self, namespace: str = 'default') -> 'Helm':
        self.namespace = namespace

        return self

    def install(self, name: str, chart: str, flags: list = []) -> 'Helm':
        self.__runHelmCommand(
            [HelmC.NAMESPACE, self.namespace, HelmC.INSTALL, name, chart] + flags
        )

    def __addRepo(self, name: str, url: str) -> None:
        if not self.__repoExists(name):
            self.__runHelmCommand([
                HelmC.REPO, HelmC.ADD, name, url
            ])

        self.__runHelmCommand([HelmC.REPO, HelmC.UPDATE])

    def __runHelmCommand(self, arguments: list) -> None:
        process = subprocess.Popen(
            (['helm'] + arguments), stdout=subprocess.PIPE
        )

        for line in iter(process.stdout.readline, b""):
            sys.stdout.write(line.decode("utf-8"))

        process.wait()

        if process.returncode != 0:
            raise HelmException(
                'Something went wrong running command:' + str(arguments)
            )

    def __repoExists(self, name: str) -> bool:
        repos = subprocess.run(
            ['helm', HelmC.REPO, HelmC.LIST],
            capture_output=True
        ).stdout.decode("utf-8")

        if re.search(name, repos):
            return True
        else:
            return False
