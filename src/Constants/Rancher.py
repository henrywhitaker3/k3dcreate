class Rancher:
    # values.yaml keys
    HOSTNAME = 'hostname'
    INGRESS_SOURCE_SECRET = 'ingress.tls.source=secret'

    NAMESPACE = 'cattle-system'

    # Misc options
    INGRESS_SECRET_NAME = 'tls-rancher-ingress'
    CA_SECRET_NAME='tls-ca'

    SELF_SIGNED = 'self-signed'
    CUSTOM_CERT = 'custom-cert'
