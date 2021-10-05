import pulumi
import pulumi_kubernetes as k8s
import pulumi_gcp as gcp


def main():
    # Create a GCP resource (Storage Bucket)
    bucket = gcp.storage.Bucket('my-bucket')

    # Export the DNS name of the bucket
    pulumi.export('bucket_name',  bucket.url)


if __name__ == '__main__':
    main()
