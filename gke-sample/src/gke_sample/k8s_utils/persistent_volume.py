from kubernetes import client, config
from kubernetes.client.rest import ApiException

import logging

logger = logging.getLogger(__name__)


def register_storage_class(name: str, gke_storage_type: str, reclaim_policy: str):
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


