from gke_sample.k8s_utils.pod import *


def main():
    pod_name = "pd-feeder-pod"
    pvc_name = "pv-test1"

    container_name = "cloud-sdk"
    image_name = "google/cloud-sdk:slim"
    start_up_command = "gsutil cp gs://eryeden-test1/kitten.png /volume/; sleep 3600"
    path_to_mount_volume = "/volume"

    status = create_pod(name=pod_name,
                        container_name=container_name,
                        container_image_name=image_name,
                        persistent_volume_claim_name=pvc_name,
                        path_to_mount_persistent_volume=path_to_mount_volume,
                        start_up_command=start_up_command)
    print(status)


if __name__ == '__main__':
    main()
