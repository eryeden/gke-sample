import subprocess
from google.cloud import storage
from typing import List


def execute_command(command: List[str]) -> str:
    res = subprocess.run(command, stdout=subprocess.PIPE)
    return res.stdout.decode("utf8")


def get_cluster_credentials(cluster_name: str, zone: str):
    command = [
        "gcloud",
        "container",
        "clusters",
        "get-credentials",
        cluster_name,
        "--zone={}".format(zone)
    ]
    return execute_command(command)


def create_cluster(cluster_name: str,
                   zone: str,
                   machine_type: str,
                   machine_size: int,
                   disk_size: int
                   ):
    command = [
        "gcloud",
        "container",
        "clusters",
        "create",
        cluster_name,
        "--machine-type={}".format(machine_type),
        "--num-nodes={}".format(machine_size),
        "--disk-size={}".format(disk_size),
        "--zone={}".format(zone)

    ]
    return execute_command(command)


def delete_cluster(cluster_name: str, zone: str) -> str:
    command = [
        "gcloud",
        "container",
        "clusters",
        "delete",
        cluster_name,
        "--zone={}".format(zone),
        "--quiet"
    ]
    return execute_command(command)


def main():
    cluster_name = "gke-test-cluster"
    zone = "us-central1-c"

    VOLUME_SETUP_MACHINE_TYPE = "e2-small"
    COMPUTING_MACHINE_TYPE = "e2-small"  # Use preemtive matchine
    COMPUTING_MACHINE_NODE_SIZE = 1
    DATABASE_MACHINE_TYPE = "e2-small"

    STORAGE_TYEP = "pd-standard"  # Use the standard storage as persistent volume
    STORAGE_SIZE = "30Gi"

    # cret = create_cluster(CLUSTER_NAME, ZONE, VOLUME_SETUP_MACHINE_TYPE, 1, 10)
    # print(cret)
    # cret = get_cluster_credentials(CLUSTER_NAME, ZONE)
    # print(cret)
    cret = delete_cluster(cluster_name, zone)
    print(cret)


if __name__ == '__main__':
    main()
