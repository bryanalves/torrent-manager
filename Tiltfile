load('ext://secret', 'secret_create_generic')
load('ext://configmap', 'configmap_create')

default_registry('registry.my.bumbum.dance')
docker_build("registry.my.bumbum.dance/torrent-manager", ".")

allow_k8s_contexts('kubernetes-admin@bumbum')

secret_create_generic('torrent-manager-flood-auth', from_env_file='k8s/secret.env')
configmap_create('torrent-manager-config', from_env_file='k8s/config.env')
k8s_yaml(['k8s/deployment.yaml'])
k8s_resource(workload='torrent-manager', port_forwards="5001:5000")
