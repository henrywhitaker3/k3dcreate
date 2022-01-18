# K3DCreate

This tool is a wrapper around [k3d](https://k3s.io) to easily create cluster with some extra defaults. You can use it to automatically install nginx-ingress, rancher or provide a list of helm repos that will get installed automatically after creating the cluster.

Note: this has only been tested on Linux, but should work on Mac as well.

## Installation

### Dependencies

You must have the follwoing installed:

- kubectl
- [k3d](https://k3s.io)
- [Helm](https://helm.sh)

<!-- ### Script

To install the script with a one-line command, run:

```shell
curl https://github.com/henrywhitaker3/k3dcreate/install.sh | bash
```

This downloads a binary and places it in `/usr/local/bin` so can then just run `k3dcreate ...` from a shell. -->

### Build it yourself

You can build the tool yourself by cloning the repo and running:

```shell
pyinstaller --onefile src/main.py --name k3dcreate
```

which will output a binary to `./dist/k3dcreate`. You can then alias/use this however you prefer.

Or, you can just run it with `python3 src/main.py`

## Usage

The basic usage to create a default cluster is:

```shell
k3dcreate --name bongo
```

This will spin up a single node k3d cluster for you.

### Options

To customise the installation, you can use the following options:

| Option | Default | Description |
| --- | --- | --- |
| `--name` | `null` | This sets the name of the cluster |
| `--nodes` | `1` | This sets the number of nodes in cluster |
| `--nginx` | `False` | When this flag is present, nginx-ingress will be installed as the default ingress instead of traefik |
| `--version` | `null` | You can pass the name (and tag) of a k3s image here to use that in the cluster instead of the k3d default |
| `--delete` | `False` | When this flag is set, the cluster will be deleted |
| `--port` | `null` | Open a port for the loadbalancer in format `--port [host_port]:[container_port]` e.g. `--port 8443:443` |
| `--rancher` | `False` | When this flag is set, the Rancher UI will be installed with helm |
| `--rancher-version` | `False` | Optional option to set the rancher version e.g. `2.3.6` |
| `--rancher-hostname` | `null` | This is required when using the `--rancher` flag, and sets the hostname the UI will be available on |
| `--custom-cert` | `False` | This can be used to use a custom certificate for the Rancher ingress (default to cert-manager + self-signed certs) |
| `--certificate` | `null` | Required when using `--custom-cert` and is the path to the certificate file |
| `--private-key` | `null` | Required when using `--custom-cert` and is the path to the private key file |
