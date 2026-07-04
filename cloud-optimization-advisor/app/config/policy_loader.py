from pathlib import Path

import yaml


class PolicyLoader:
    """
    Loads recommendation policies.
    """

    @staticmethod
    def load(policy_name: str) -> dict:

        policy_file = (
            Path("policies")
            / f"{policy_name}.yaml"
        )

        with open(
            policy_file,
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file)