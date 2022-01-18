from Constants.Ingress import Ingress
from Kubernetes.Cluster import Cluster
from Constants.K3d import K3d as K3dC
import subprocess
import sys

class K3d:
    def __init__(self, cluster: Cluster) -> None:
        self.cluster = cluster

    def create(self) -> None:
        K3d.run(action=K3dC.CREATE, arguments=self.__buildCreateArguments())

        return None

    def delete(self) -> None:
        K3d.run(K3dC.DELETE, [self.cluster.name])

        return None

    def __buildCreateArguments(self) -> list:
        args = []

        args.append(self.cluster.getName())

        if self.cluster.getNodes() > 1:
            args.append(K3dC.NODES)
            args.append(str(self.cluster.getNodes()))

        if not self.cluster.useDefaultVersion():
            args.append(K3dC.VERSION)
            args.append(self.cluster.getVersion())

        if self.cluster.getIngress() == Ingress.NGINX:
            args.append(K3dC.ARG)
            args.append(K3dC.DISABLE_TRAEFIK)

        if self.cluster.getPorts():
            for port in self.cluster.getPorts():
                args.append(K3dC.PORT)
                args.append(port + K3dC.LOADBALANCER)

        # print(args)
        # exit(0)
        return args

    def run(action: str, arguments: list) -> None:
        process = subprocess.Popen(
            (['k3d', K3dC.CLUSTER, action] + arguments), stdout=subprocess.PIPE
        )

        for line in iter(process.stdout.readline, b""):
            sys.stdout.write(line.decode('utf-8'))
