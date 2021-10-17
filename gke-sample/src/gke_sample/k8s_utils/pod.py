from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import List

import logging

logger = logging.getLogger(__name__)


def list_pod(namespace="default"):
    config.load_kube_config()
    pos_list = client.CoreV1Api.list_namespaced_pod(namespace)
    return pos_list


def create_pod(name: str,
               container_name: str,
               container_image_name: str,
               persistent_volume_claim_name: str,
               path_to_mount_persistent_volume: str,
               start_up_command: str,
               namespace="default"):
    internal_pv_name = "my-awesome-pvc"
    config.load_kube_config()

    meta_data = client.V1ObjectMeta(name=name)
    pod_spec = client.V1PodSpec(
        containers=[
            client.V1Container(
                name=container_name,
                image=container_image_name,
                command=["sh", "-c", start_up_command],
                volume_mounts=[
                    client.V1VolumeMount(mount_path=path_to_mount_persistent_volume,
                                         name=internal_pv_name)
                ]
            )
        ],
        volumes=[
            client.V1Volume(
                name=internal_pv_name,
                persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                    claim_name=persistent_volume_claim_name,
                )
            )
        ]
    )
    body = client.V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=meta_data,
        spec=pod_spec
    )

    api_instance = client.CoreV1Api()
    try:
        api_response = api_instance.create_namespaced_pod(namespace, body)
        logger.debug("create_namespaced_pod response:\n{}".format(api_response))
    except ApiException as e:
        logger.error("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)
        return False
    return True
