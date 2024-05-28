import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Configuration
LOG_DIRECTORY = "/path/to/log/directory"  # Directory where logs are stored
AZURE_STORAGE_CONNECTION_STRING = "your_connection_string"
CONTAINER_NAME = "your_container_name"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(
    AZURE_STORAGE_CONNECTION_STRING)


def upload_logs_to_blob(file_path, container_name):
    # Create a BlobClient
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=os.path.basename(file_path))

    print(
        f"Uploading {file_path} to Azure Blob Storage as {os.path.basename(file_path)}")

    # Upload the file
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)


def collect_and_upload_logs(log_directory, container_name):
    for root, dirs, files in os.walk(log_directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                upload_logs_to_blob(file_path, container_name)
            except Exception as e:
                print(f"Failed to upload {file_path}: {str(e)}")


if __name__ == '__main__':
    collect_and_upload_logs(LOG_DIRECTORY, CONTAINER_NAME)
