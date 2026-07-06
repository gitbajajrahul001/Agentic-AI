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
        container_name: str,
    ):

        self.account_name = (
            account_name
        )

        self.container_name = (
            container_name
        )

        self.blob_service_client = (
            BlobServiceClient(
                account_url=(
                    f"https://{account_name}.blob.core.windows.net"
                ),
                credential=credential,
            )
        )

    def upload_file(
        self,
        file_path: Path,
    ) -> str:
        """
        Upload a local knowledge document
        to Azure Blob Storage.
        """

        blob_name = (
            f"json/"
            f"{file_path.parent.name}/"
            f"{file_path.name}"
        )

        blob_client = (
            self.blob_service_client.get_blob_client(
                container=self.container_name,
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