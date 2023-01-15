import json
import uuid
from google.oauth2.service_account import Credentials
from google.cloud import storage


class GCPBucketClient:
    def __init__(self):

        # Load the credentials from file.
        credentials = Credentials.from_service_account_file(
            "config/sturdy-chimera-374511-73f24a51a3e4.json"
        )
        # Initialize a client
        client = storage.Client(project="Pinterest Pipeline", credentials=credentials)
        self.client = client

    def create_bucket(self, bucket_name):
        if self.client.exists(bucket_name):
            print(f"Bucket {bucket_name} already exists")
            return self.client.bucket(bucket_name)
        else:
            bucket_id = f"{bucket_name}_{str(uuid.uuid4())}"
            bucket = self.client.bucket(bucket_id)
            bucket.storage_class = "STANDARD"
            new_bucket = self.client.create_bucket(bucket, location="europe-west2")
            print(
                f"Created bucket {new_bucket.name} in {new_bucket.location} with storage class {new_bucket.storage_class}"
            )
            return new_bucket

    def write_to_bucket(self, bucket, file_name, data):
        # Get the bucket
        bucket = self.client.bucket(bucket)

        # Create a new blob
        blob = bucket.blob(file_name)

        # Convert data to json
        json_data = json.dumps(data)

        # Upload the json data to the blob
        blob.upload_from_string(json_data, content_type="application/json")
