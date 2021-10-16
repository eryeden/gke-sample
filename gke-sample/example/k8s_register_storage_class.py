from gke_sample.k8s_utils.persistent_volume import *


def main():
    storage_class_name = "pd-python-test2"
    storage_type = "pd-standard"
    reclaim_policy = "Retain"

    status = register_storage_class(storage_class_name, storage_type, reclaim_policy)
    print(status)


if __name__ == '__main__':
    main()
