import subprocess
from google.cloud import storage
from typing import List
from gke_sample.bash_util.utils import *


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