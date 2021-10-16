from kubernetes import client, config
from kubernetes.client.rest import ApiException

from pprint import pprint


def main():
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CoreV1Api()
    api = client.CustomObjectsApi()
    api2 = client.ApiClient()
    k8s_apps_v1 = client.AppsV1Api()


    # apiVersion: storage.k8s.io/v1
    # kind: StorageClassc
    # metadata:
    #   name: pd-example
    # provisioner: pd.csi.storage.gke.io
    # volumeBindingMode: WaitForFirstConsumer
    # allowVolumeExpansion: true
    # parameters:
    #   type: pd-standard
    # reclaimPolicy: Retain

    test_storage_class = {
        "apiVersion": "storage.k8s.io/v1",
        "kind": "StorageClass",
        "name": "pd-test",
        "provisioner": "pd.csi.storage.gke.io",
        "volumeBindingMode": "WaitForFirstConsumer",
        "allowVolumeExpansion": True,
        "parameters": {
            "type": "pd-standard"
        },
        "reclaimPolicy": "Retain"
    }

    api_instance = client.StorageV1Api(api2)
    meta_data = client.V1ObjectMeta(name="pd-python-test")
    body = client.V1StorageClass(api_version="storage.k8s.io/v1", provisioner="pd.csi.storage.gke.io",
                                 kind="StorageClass",
                                 volume_binding_mode="WaitForFirstConsumer",
                                 allow_volume_expansion=True,
                                 parameters={
                                     "type": "pd-standard"
                                 },
                                 reclaim_policy="Retain",
                                 metadata=meta_data)
    try:
        api_response = api_instance.create_storage_class(body, field_manager="field_manager")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StorageV1Api->create_storage_class: %s\n" % e)



if __name__ == '__main__':
    main()
