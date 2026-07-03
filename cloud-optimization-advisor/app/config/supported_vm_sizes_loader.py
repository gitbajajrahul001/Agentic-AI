import yaml


class SupportedVmSizesLoader:
    """
    Loads the list of Azure VM sizes supported
    by the organization.
    """

    @staticmethod
    def load(
        path: str = "config/supported_vm_sizes.yaml",
    ) -> list[str]:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            data = yaml.safe_load(file)

        return data["vm_sizes"]