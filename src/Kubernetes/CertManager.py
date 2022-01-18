from Constants.Helm import Helm as HelmC
from Kubernetes.Helm import Helm

class CertManager:
    VERSION = 'v1.5.4'

    def install() -> None:
        (
            Helm().forRepo('jetstack', 'https://charts.jetstack.io')
                .forNamespace('cert-manager')
                .install(
                    'cert-manager',
                    'jetstack/cert-manager',
                    [
                        HelmC.SET, 'installCRDs=true',
                        HelmC.VERSION, CertManager.VERSION,
                        HelmC.CREATE_NAMESPACE
                    ]
                )
        )
