import subprocess
from google.cloud import storage


def create_bucket(bucket_name: str, location: str):
    client = storage.Client()
    bucket = client.create_bucket(bucket_name, location=location)
    client.create_bucket(bucket)
    return bucket


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        print(blob.name)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    print(blob)


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Blob {} deleted.".format(blob_name))


# Before the execution, please see the following page and prepare the credential.
# https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python

def main():
    path_to_upload = "/home/ery/Devel/gke-sample/gke-sample/asset/kitten2.png"
    blob_name = "kitten2.png"
    bucket_name = "eryeden-test1"
    list_blobs(bucket_name)
    upload_blob(bucket_name, path_to_upload, blob_name)
    list_blobs(bucket_name)
    delete_blob(bucket_name, blob_name)
    list_blobs(bucket_name)


if __name__ == '__main__':
    main()