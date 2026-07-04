from pathlib import Path

import yaml


class ConfigurationLoader:
    """
    Loads application configuration from config/config.yaml.
    """

    @staticmethod
    def load() -> dict:

        project_root = (
            Path(__file__).resolve().parents[2]
        )

        config_file = (
            project_root
            / "config"
            / "config.yaml"
        )

        if not config_file.exists():

            raise FileNotFoundError(
                f"Configuration file not found: {config_file}"
            )

        with open(
            config_file,
            "r",
            encoding="utf-8",
        ) as file:

            return yaml.safe_load(file)