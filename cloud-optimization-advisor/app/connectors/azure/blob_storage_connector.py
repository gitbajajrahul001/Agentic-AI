from pathlib import Path

from azure.storage.blob import (
    BlobServiceClient,
)


class BlobStorageConnector:
    """
    Uploads knowledge documents
    to Azure Blob Storage.
    """

    def __init__(
        self,
        credential,
        account_name: str,
    ):

        self.account_name = (
            account_name
        )

        self.blob_service_client = (
            BlobServiceClient(
                account_url=(
                    f"https://{account_name}.blob.core.windows.net"
                ),
                credential=credential,
            )
        )
        
    def ensure_container_exists(
        self,
        container_name: str,
    ):
        """
        Create the container if it does not already exist.
        """

        container_client = (
            self.blob_service_client.get_container_client(
                container_name
            )
        )

        if not container_client.exists():

            container_client.create_container()



    def upload_file(
        self,
        file_path: Path,
        knowledge_level: str,
    ) -> str:
        """
        Upload a local knowledge document
        to Azure Blob Storage.
        """

        container_name = (
            f"{knowledge_level}-knowledge"
        )
        
        self.ensure_container_exists(
            container_name,
        )
            
        blob_name = (
            f"{file_path.parent.name}/"
            f"{file_path.name}"
        )

        blob_client = (
            self.blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_name,
            )
        )

        with open(
            file_path,
            "rb",
        ) as file:

            blob_client.upload_blob(
                file,
                overwrite=True,
            )

        return blob_name