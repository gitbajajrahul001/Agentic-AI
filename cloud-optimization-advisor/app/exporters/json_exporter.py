import json

from pathlib import Path

from datetime import datetime


class JsonExporter:
    """
    Persists knowledge documents as JSON files.
    """

    def __init__(
        self,
        output_directory: str = "output/json",
    ):

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def export(
        self,
        knowledge_document: dict,
    ) -> Path:

        execution = knowledge_document[
            "execution"
        ]

        inventory = knowledge_document[
            "inventory"
        ]

        generated_at = datetime.fromisoformat(

            execution[
                "generated_at"
            ]

        )

        date_folder = generated_at.strftime(
            "%Y-%m-%d"
        )

        timestamp = generated_at.strftime(
            "%Y%m%dT%H%M%SZ"
        )

        resource_name = inventory[
            "resource_name"
        ]

        output_folder = (

            self.output_directory

            / date_folder

        )

        output_folder.mkdir(

            parents=True,

            exist_ok=True,

        )

        output_file = (

            output_folder

            /

            f"{timestamp}_{resource_name}.json"

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