from pathlib import Path

from app.exporters.knowledge_exporter import (
    KnowledgeExporter,
)


class KnowledgeManager:

    def __init__(
        self,
        exporter: KnowledgeExporter,
        blob_storage_connector,
        storage_config: dict,
    ):

        self.exporter = exporter
        self.blob_storage_connector = blob_storage_connector
        self.storage_config = storage_config

    def publish(
        self,
        knowledge_document: dict,
        knowledge_level: str,
    ) -> Path:

        output_file = self.exporter.export(
            knowledge_document,
            knowledge_level,
        )

        container_name = (
            self.storage_config["containers"][knowledge_level]
        )
    


        self.blob_storage_connector.upload_file(
            output_file,
            container_name,
        )

        return output_file