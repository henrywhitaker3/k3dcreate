#!/usr/bin/env python3

from time import sleep
from Constants.Ingress import Ingress
from Constants.Rancher import Rancher as RancherC
from Exceptions.InvalidInputException import InvalidInputException
from Kubernetes.Kubectl import Kubectl
from Kubernetes.NginxIngress import NginxIngress
from Kubernetes.Rancher import Rancher
from Utils.Argparser import Argparser
from Kubernetes.Cluster import Cluster
from Kubernetes.K3d import K3d

VERSION='1.0.0'

def rollback(k3d: K3d) -> None:
    k3d.delete()
    print('Something went wrong, the cluster has been deleted')

if __name__ == "__main__":
    try:
        args = Argparser().parse()
    except InvalidInputException as e:
        print(e)
        exit(1)

    cluster = Cluster(
        name=args.getName(),
        nodes=args.getNodes(),
        version=('default' if args.useDefaultVersion() else args.getVersion()),
        ingress=args.getIngress(),
        ports=args.getPorts()
    )

    k3d = K3d(cluster)

    if not args.create():
        k3d.delete()
    else:
        k3d.create()

        try:
            if cluster.getIngress() == Ingress.NGINX:
                NginxIngress.install()

            if args.shouldInstallRancher():
                if args.shouldUseCustomCert():
                    rancher = Rancher(
                        name=cluster.getName(),
                        nodes=cluster.getNodes(),
                        certificateType=RancherC.CUSTOM_CERT,
                        hostname=args.getRancherHostname(),
                        privateKey=args.getPrivateKey(),
                        certificate=args.getCertificate(),
                        version=args.getRancherVersion(),
                        caCert=args.getCACert()
                    )
                else:
                    rancher = Rancher(
                        name=cluster.getName(),
                        nodes=cluster.getNodes(),
                        certificateType=RancherC.SELF_SIGNED,
                        hostname=args.getRancherHostname(),
                        version=args.getRancherVersion()
                    )
                rancher.install()
        except:
            rollback(k3d)

