from gke_sample.gcp_utils.gcs import *
import json


def main():

    configs = {}
    with open("../asset/gcp_config.json") as f:
        configs = json.load(f)

    path_to_upload = "../asset/kitten2.png"
    blob_name = "kitten2.png"
    bucket_name = configs["bucket_name"]
    list_blobs(bucket_name)
    upload_blob(bucket_name, path_to_upload, blob_name)
    list_blobs(bucket_name)
    delete_blob(bucket_name, blob_name)
    list_blobs(bucket_name)


if __name__ == '__main__':
    main()
