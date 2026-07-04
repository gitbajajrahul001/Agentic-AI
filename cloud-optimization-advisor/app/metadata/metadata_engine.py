from importlib.metadata import metadata


class MetadataEngine:
    """
    Extracts configured business metadata
    from Azure resource tags.
    """

    def __init__(
        self,
        configuration: dict,
    ):

        self.configuration = configuration

    ####################################################################
    # Public API
    ####################################################################

    def extract_metadata(
        self,
        tags: dict[str, str],
    ) -> dict[str, str]:

        metadata = {}

        configured_tags = (
            self.configuration.get(
                "resource_metadata",
                {},
            )
        )

        for metadata_key, configuration in configured_tags.items():

            azure_tag = configuration.get(
                "tag",
                "",
            )

            metadata[metadata_key] = tags.get(
                azure_tag,
                "",
            )

        return metadata