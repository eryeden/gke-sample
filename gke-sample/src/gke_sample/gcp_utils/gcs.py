from os import environ
from google.cloud import storage
import logging

logger = logging.getLogger(__name__)


def check_gcp_credential() -> bool:
    """Check the existence of env variable `GOOGLE_APPLICATION_CREDENTIALS` which is needed for python client of GCS."""
    if environ.get("GOOGLE_APPLICATION_CREDENTIALS") is not None:
        return True
    else:
        logger.error("Environment variable GOOGLE_APPLICATION_CREDENTIALS is not found."
                     "Please run `source source_env.sh` before execution.")
        return False


def create_bucket(bucket_name: str, location: str):
    """Create a new bucket on the specified location. ex) `location`='US-CENTRAL1'"""
    assert check_gcp_credential()
    client = storage.Client()
    bucket = client.create_bucket(bucket_name, location=location)
    client.create_bucket(bucket)
    return bucket


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"
    assert check_gcp_credential()
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
    assert check_gcp_credential()
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
    assert check_gcp_credential()
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Blob {} deleted.".format(blob_name))
