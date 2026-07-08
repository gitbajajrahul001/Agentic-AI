from pathlib import Path

from app.exporters.knowledge_exporter import (
    KnowledgeExporter,
)


class KnowledgeManager:

    def __init__(
        self,
        exporter: KnowledgeExporter,
        blob_storage_connector,
    ):

        self.exporter = exporter
        self.blob_storage_connector = blob_storage_connector

    def publish(
        self,
        knowledge_document: dict,
        knowledge_level: str,
    ) -> Path:

        output_file = self.exporter.export(
            knowledge_document,
            knowledge_level,
        )

        self.blob_storage_connector.upload_file(
            output_file,
            knowledge_level,
        )

        return output_file