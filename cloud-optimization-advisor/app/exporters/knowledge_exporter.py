import json

from pathlib import Path

from datetime import datetime

from app.core.constants import (
    KnowledgeLevels,
)


class KnowledgeExporter:
    """
    Persists knowledge documents as JSON files.
    """

    def __init__(
        self,
        output_root: str = "output",
    ):

        self.output_root = Path(
            output_root
        )

        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    
    def _get_file_name(
        self,
        knowledge_document: dict,
        knowledge_level: str,
    ) -> str:

        if knowledge_level == KnowledgeLevels.VM:

            return (
                knowledge_document["inventory"]["resource_name"]
            )

        if knowledge_level == KnowledgeLevels.RESOURCE_GROUP:

            return (
                knowledge_document["resource_group"]["name"]
            )
        
        if knowledge_level == KnowledgeLevels.SUBSCRIPTION:

            return (
                knowledge_document["subscription"]["subscription_id"]
            )

        raise ValueError(
            f"Unsupported knowledge level: {knowledge_level}"
        )
    
    
    
    
    def export(
        self,
        knowledge_document: dict,
        knowledge_level: str,
    ) -> Path:

        execution = knowledge_document[
            "execution"
        ]

        
        ##### REMOVED TIMESTAMP AND DATE FOLDER GENERATION #####

        # generated_at = datetime.fromisoformat(

        #     execution[
        #         "generated_at"
        #     ]

        # )

        # date_folder = generated_at.strftime(
        #     "%Y-%m-%d"
        # )

        # timestamp = generated_at.strftime(
        #     "%Y%m%dT%H%M%SZ"
        # )


        resource_name = self._get_file_name(
            knowledge_document,
            knowledge_level,
        )
        
        
        knowledge_folder = (
            self.output_root
            /
            f"{knowledge_level}-knowledge"
        )
        knowledge_folder.mkdir(
            parents=True,
            exist_ok=True,
        )
        
        #### REMOVED DATE FOLDER GENERATION ####

        # output_folder = (

        #     knowledge_folder


        #     / date_folder

        # )

        output_folder = knowledge_folder
        
        output_folder.mkdir(

            parents=True,

            exist_ok=True,

        )

        output_file = (

            output_folder

            /

            f"{resource_name}.json"

        )

        with open(

            output_file,

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                knowledge_document,

                file,

                indent=4,

                ensure_ascii=False,

            )

        return output_file