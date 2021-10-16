from gke_sample.k8s_utils.persistent_volume import *


def main():

    persistent_volume_name = "pv-test1"
    storage_class_name = "pd-python-test2"
    access_mode = "ReadWriteOnce"
    storage_size_gibibyte = 30
    status = create_persistent_volume(persistent_volume_name, storage_class_name, access_mode, storage_size_gibibyte)
    print(status)


if __name__ == '__main__':
    main()
