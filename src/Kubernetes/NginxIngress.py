from Constants.Helm import Helm as HelmC
from Kubernetes.Helm import Helm

class NginxIngress:
    def install() -> None:
        (
            Helm().forRepo('nginx-stable', 'https://helm.nginx.com/stable')
                .forNamespace('ingress-nginx')
                .install(
                    'ingress-nginx',
                    'nginx-stable/nginx-ingress',
                    [
                        HelmC.SET, 'controller.setAsDefaultIngress=true',
                        HelmC.CREATE_NAMESPACE
                    ]
                )
        )
