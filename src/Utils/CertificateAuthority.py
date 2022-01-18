import datetime
import uuid

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from pathlib import Path

class CertificateAuthority:
    KEY_NAME = 'ca.key'
    CERT_NAME = 'ca.crt'

    def __init__(self) -> None:
        self.oneDay = datetime.timedelta(1, 0, 0)
        self.oneYear = datetime.timedelta(365, 0, 0)

    def create(self, directory: str) -> None:
        self.__createDirectory(directory)
        self.__createPrivateKey()
        self.__getPublicKey()
        self.__createBuilder()
        self.__getCertificate()

        self.__writeCertificateToFile()
        self.__writeKeyToFile()
        return None

    def __createDirectory(self, directory):
        self.directory = directory
        Path(self.directory).mkdir(parents=True, exist_ok=True)

    def __writeKeyToFile(self) -> None:
        with open(self.directory + self.KEY_NAME, "wb") as f:
            f.write(
                self.privateKey.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

    def __writeCertificateToFile(self) -> None:
        with open(self.directory + self.CERT_NAME, "wb") as f:
            f.write(
                self.certificate.public_bytes(
                    encoding=serialization.Encoding.PEM,
                )
            )

    def __getCertificate(self) -> x509.Certificate:
        self.certificate = self.builder.sign(
            private_key=self.privateKey,
            algorithm=hashes.SHA256(),
            backend=default_backend()
        )

        return self.certificate

    def __createBuilder(self) -> x509.CertificateBuilder:
        self.builder = x509.CertificateBuilder()
        self.builder = self.builder.subject_name(
            x509.Name(
                [
                    x509.NameAttribute(NameOID.COMMON_NAME, u'K3DCreate CA'),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'K3DCreate CA'),
                    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'K3DCreate CA'),
                ]
            )
        )
        self.builder = self.builder.issuer_name(
            x509.Name(
                [
                    x509.NameAttribute(NameOID.COMMON_NAME, u'K3DCreate CA'),
                ]
            )
        )
        self.builder = self.builder.not_valid_before(datetime.datetime.today() - self.oneDay)
        self.builder = self.builder.not_valid_after(datetime.datetime.today() + self.oneYear)
        self.builder = self.builder.serial_number(int(uuid.uuid4()))
        self.builder = self.builder.public_key(self.publicKey)
        self.builder = self.builder.add_extension(
            x509.BasicConstraints(
                ca=True,
                path_length=None
            ),
            critical=True,
        )

        return self.builder

    def __getPublicKey(self) -> rsa.RSAPublicKey:
        self.publicKey = self.privateKey.public_key()

        return self.publicKey

    def __createPrivateKey(self) -> rsa.RSAPrivateKeyWithSerialization:
        self.privateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        return self.privateKey
