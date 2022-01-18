import argparse
from Constants.Ingress import Ingress
from Exceptions.InvalidInputException import InvalidInputException

class Argparser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser('k3d create')
        self.registerArguments()

    def registerArguments(self) -> None:
        self.parser.add_argument(
            '--nodes',
            metavar='Nodes',
            type=int,
            help='The number of nodes in the cluster',
            default=1,
            required=False
        )
        self.parser.add_argument(
            '--name',
            metavar='Name',
            type=str,
            help='The name of the cluster',
            required=True
        )
        self.parser.add_argument(
            '--nginx',
            help='If enabled, then the cluster will use nginx instead of traefik for the ingress',
            default=False,
            action='store_true'
        )
        self.parser.add_argument(
            '--version',
            metavar='Kubernetes Version',
            help='The version of kubernetes to use. Skip to use k3d default, or provide a k3s image',
            default=None
        )
        self.parser.add_argument(
            '--delete',
            help='An optional flag that when present, will delete the cluster and any related files.',
            default=False,
            action='store_true'
        )
        self.parser.add_argument(
            '--port',
            help='Open a port for the loadbalancer in format --port [host_port]:[container_port] e.g. --port 8443:443',
            default=[],
            action='append',
            required=False
        )
        self.parser.add_argument(
            '--rancher',
            help='An optional flag that when present, will install the Rancher UI in the cluster.',
            default=False,
            action='store_true'
        )
        self.parser.add_argument(
            '--rancher-hostname',
            help='An optional flag that when present, will install the Rancher UI in the cluster.',
            default=None
        )
        self.parser.add_argument(
            '--rancher-version',
            type=str,
            help='An optional flag that when present, will install a specific version of the Rancher UI in the cluster.',
            default=''
        )
        self.parser.add_argument(
            '--custom-cert',
            help='An optional flag that when present, will use a custom certificate. If this is not set, it will use cert-manager to self-sign certs.',
            default=False,
            action='store_true'
        )
        self.parser.add_argument(
            '--certificate',
            metavar='Certificate',
            type=str,
            help='The absolute path to the certificate to use for rancher ingress',
            default=''
        )
        self.parser.add_argument(
            '--private-key',
            metavar='Private Key',
            type=str,
            help='The absolute path to the private key to use for rancher ingress',
            default=''
        )
        self.parser.add_argument(
            '--ca-cert',
            metavar='CA Cert',
            type=str,
            help='The absolute path to the CA certificate for the rancher ingress',
            default=''
        )

    def parse(self) -> 'Argparser':
        self.args = self.parser.parse_args()

        self.requiredWith(
            {
                'name': 'rancher',
                'value': self.shouldInstallRancher()
            },
            {
                'name': 'hostname',
                'value': self.getRancherHostname()
            }
        )
        self.requiredWith(
            {
                'name': 'custom-cert',
                'value': self.shouldUseCustomCert()
            },
            {
                'name': 'certificate',
                'value': self.getCertificate()
            }
        )
        self.requiredWith(
            {
                'name': 'custom-cert',
                'value': self.shouldUseCustomCert()
            },
            {
                'name': 'private-key',
                'value': self.getPrivateKey()
            }
        )

        return self

    def getNodes(self) -> int:
        return self.args.nodes

    def getName(self) -> str:
        return self.args.name

    def getIngress(self) -> str:
        return Ingress.NGINX if self.args.nginx else Ingress.TRAEFIK

    def useDefaultVersion(self) -> bool:
        return self.args.version == None;

    def getVersion(self) -> str:
        return self.args.version

    def shouldInstallRancher(self) -> bool:
        return bool(self.args.rancher)

    def getRancherHostname(self):
        return self.args.rancher_hostname

    def getPorts(self) -> list:
        return self.args.port

    def shouldUseCustomCert(self) -> bool:
        return self.args.custom_cert

    def getCertificate(self) -> str:
        return self.args.certificate

    def getPrivateKey(self) -> str:
        return self.args.private_key

    def getCACert(self) -> str:
        return self.args.ca_cert

    def create(self) -> bool:
        return not self.args.delete

    def getRancherVersion(self) -> str:
        return self.args.rancher_version

    def requiredWith(self, whenPresent: dict, requires: dict) -> None:
        if (whenPresent['value'] != False) and (whenPresent['value'] != None):
            if requires['value'] == None:
                raise InvalidInputException(
                    'Error: The ' + requires['name'] + ' parameter is required when using ' + whenPresent['name']
                )

        return None
