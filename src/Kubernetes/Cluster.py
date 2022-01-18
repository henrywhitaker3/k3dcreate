from Constants.Ingress import Ingress

class Cluster:
    def __init__(
        self,
        name: str,
        nodes: int = 1,
        version: str = 'default',
        ingress: str = Ingress.TRAEFIK,
        ports: list = []
    ) -> None:
        self.name = name
        self.nodes = nodes
        self.version = version
        self.ingress = ingress
        self.ports = ports

    def getName(self) -> str:
        return self.name

    def getNodes(self) -> int:
        return int(self.nodes)

    def getVersion(self) -> str:
        return self.version

    def getIngress(self) -> str:
        return self.ingress

    def useDefaultVersion(self) -> bool:
        return self.getVersion() == 'default'

    def getPorts(self) -> list:
        return self.ports
