from kubernetes import client, config
from kubernetes.client.rest import ApiException

import logging

logger = logging.getLogger(__name__)


def register_storage_class(name: str, gke_storage_type: str, reclaim_policy: str) -> bool:
    """ Register new storage class of k8s.

    :param name: name of storage class
    :param gke_storage_type: type of storage class, See https://cloud.google.com/compute/docs/disks#disk-types
    :param reclaim_policy: reclaim policy of k8s
    :return: API success=>True, fail=>False
    """
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    api = client.ApiClient()
    api_instance = client.StorageV1Api(api)
    meta_data = client.V1ObjectMeta(name=name)
    body = client.V1StorageClass(api_version="storage.k8s.io/v1", provisioner="pd.csi.storage.gke.io",
                                 kind="StorageClass",
                                 volume_binding_mode="WaitForFirstConsumer",
                                 allow_volume_expansion=True,
                                 parameters={
                                     "type": gke_storage_type
                                 },
                                 reclaim_policy=reclaim_policy,
                                 metadata=meta_data)
    try:
        api_response = api_instance.create_storage_class(body, field_manager="field_manager")
        logger.debug("storage class response:\n{}".format(api_response))
    except ApiException as e:
        logger.error("Exception when calling StorageV1Api->create_storage_class: {}\n".format(e))
        return False

    return True


def create_persistent_volume_claim(name: str, storage_class_name: str, access_modes: str, storage_size_gibibyte: int,
                                   namespace="default"):
    """Create the persistent volume claim.

    :param name: name of persistent volume
    :param storage_class_name: name of storage class
    :param access_modes: type of access mode in k8s
    :param storage_size_gibibyte: size of storage, the size should be larger than 10GiB.
    :param namespace: k8s namespace, it will be set "default" by default.
    :return: API success=>True, fail=>False
    """

    # Note: I have heavily referred to https://github.com/IBM/wc-devops-utilities/blob/master/scripts/kube/kube_pvc.py

    config.load_kube_config()
    meta_data = client.V1ObjectMeta(name=name)
    pvc_resource = client.V1ResourceRequirements(requests={"storage": "{}Gi".format(storage_size_gibibyte)})
    pvc_spec = client.V1PersistentVolumeClaimSpec(storage_class_name=storage_class_name,
                                                  access_modes=[access_modes],
                                                  resources=pvc_resource)
    body = client.V1PersistentVolumeClaim(
        api_version='v1',
        kind='PersistentVolumeClaim',
        metadata=meta_data,
        spec=pvc_spec
    )
    try:
        api_response = client.CoreV1Api().create_namespaced_persistent_volume_claim(namespace, body)
        logger.debug("persistence volume claim response:\n{}".format(api_response))
    except ApiException as e:
        logger.error("Exception create_persistent_volume: {}\n".format(e))
        return False

    return True


def delete_persistent_volume_claim(name: str, namespace="default"):
    """Delete PCV by specified PCV name.

    :param name: name of pvc
    :param namespace: k8s namespace, it will be set "default" by default.
    :return: API success=>True, fail=>False
    """

    # Note: I have heavily referred to https://github.com/IBM/wc-devops-utilities/blob/master/scripts/kube/kube_pvc.py

    config.load_kube_config()
    body = client.V1DeleteOptions()
    try:
        api_response = client.CoreV1Api().delete_namespaced_persistent_volume_claim(name, namespace, body=body)
        logger.debug("persistence volume claim response:\n{}".format(api_response))
    except ApiException as e:
        logger.error("Exception delete_persistent_volume_claim: {}\n".format(e))
        return False

    return True
