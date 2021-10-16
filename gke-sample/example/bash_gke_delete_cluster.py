import subprocess
from google.cloud import storage
from typing import List
from gke_sample.gcp_utils.gke import *


def main():
    cluster_name = "gke-test-cluster"
    zone = "us-central1-c"

    volume_setup_machine_type = "e2-small"
    COMPUTING_MACHINE_TYPE = "e2-small"  # Use preemtive matchine
    COMPUTING_MACHINE_NODE_SIZE = 1
    DATABASE_MACHINE_TYPE = "e2-small"

    STORAGE_TYEP = "pd-standard"  # Use the standard storage as persistent volume
    STORAGE_SIZE = "30Gi"

    # cret = create_cluster(cluster_name, zone, volume_setup_machine_type, 1, 10)
    # print(cret)
    # cret = get_cluster_credentials(cluster_name, zone)
    # print(cret)
    cret = delete_cluster(cluster_name, zone)
    print(cret)


if __name__ == '__main__':
    main()
