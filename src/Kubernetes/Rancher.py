from Constants.Kubectl import Kubectl as KubectlC
from Constants.Helm import Helm as HelmC
from Kubernetes.Helm import Helm
from Kubernetes.Kubectl import Kubectl
from Kubernetes.CertManager import CertManager
from Constants.Rancher import Rancher as RancherC

class Rancher:
    def __init__(
        self,
        name: str,
        nodes: int,
        certificateType: str,
        hostname: str,
        privateKey: str = '',
        certificate: str = '',
        version: str = '',
        caCert: str = ''
    ) -> None:
        self.name = name
        self.nodes = nodes
        self.certificateType = certificateType
        self.hostname = hostname
        self.privateKey = privateKey
        self.certificate = certificate
        self.version = version
        self.caCert = caCert

    def install(self) -> None:
        self.__createNamespace()

        if self.__shouldUseCustomCert():
            self.__createCertificateSecret()
            self.__installRancherCustomCert()
        else:
            self.__installCertManager()
            self.__installRancerSelfsigned()

    def __createNamespace(self) -> None:
        Kubectl().create(KubectlC.NAMESPACE, [RancherC.NAMESPACE])
        pass

    def __createCertificateSecret(self) -> None:
        if self.__hasCaCert():
            Kubectl().forNamespace(RancherC.NAMESPACE).create(
                KubectlC.SECRET,
                [
                    KubectlC.GENERIC_SECRET,
                    RancherC.CA_SECRET_NAME,
                    '--from-file=cacerts.pem=' + self.caCert
                ]
            )

        Kubectl().forNamespace(RancherC.NAMESPACE).create(
            KubectlC.SECRET,
            [
                KubectlC.TLS_SECRET,
                RancherC.INGRESS_SECRET_NAME,
                '--cert=' + self.certificate,
                '--key=' + self.privateKey
            ]
        )

    def __installCertManager(self) -> None:
        CertManager.install()
        pass

    def __installRancerSelfsigned(self) -> None:
        self.__installRancher([])

    def __installRancherCustomCert(self) -> None:
        args = [
            HelmC.SET, 'ingress.tls.source=secret',
        ]

        if self.__hasCaCert():
            args.append(HelmC.SET)
            args.append('privateCA=true')

        self.__installRancher(args)

    def __installRancher(self, arguments: list) -> None:
        defaultArgs = [
            HelmC.SET, 'hostname=' + self.hostname,
            HelmC.SET, 'replicas=' + str(self.nodes),
            HelmC.SET, 'ingress.extraAnnotations.nginx\.org/websocket-services=rancher'
        ]

        if self.__useCustomRancherVersion():
            defaultArgs.append(
                HelmC.VERSION, self.version
            )

        (
            Helm().forRepo('rancher-latest', 'https://releases.rancher.com/server-charts/latest')
                .forNamespace('cattle-system')
                .install(
                    'rancher',
                    'rancher-latest/rancher',
                    (
                        defaultArgs + arguments
                    )
                )
        )

    def __shouldUseCustomCert(self) -> bool:
        return self.certificateType == RancherC.CUSTOM_CERT

    def __hasCaCert(self) -> bool:
        return self.caCert != ''

    def __useCustomRancherVersion(self) -> bool:
        return self.version != ''
