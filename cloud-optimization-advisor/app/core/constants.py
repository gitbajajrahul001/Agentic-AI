
class AzureMetricNames:
    """
    Azure Monitor metric names.

    These are the official metric names exposed by
    Azure Monitor Metrics API.
    """

    CPU_PERCENTAGE = "Percentage CPU"

    NETWORK_IN_TOTAL = "Network In Total"

    NETWORK_OUT_TOTAL = "Network Out Total"

    DISK_READ_BYTES = "Disk Read Bytes"

    DISK_WRITE_BYTES = "Disk Write Bytes"

    AVAILABLE_MEMORY_PERCENTAGE = "Available Memory Percentage"

    AVAILABLE_MEMORY_BYTES = "Available Memory Bytes"


class AzureScopes:
    """
    Azure authentication scopes.
    """

    MANAGEMENT = "https://management.azure.com/.default"


class AzureApiVersions:
    """
    Azure REST API versions.
    """

    RESOURCE_GRAPH = "2022-10-01"

    METRIC_DEFINITIONS = "2023-10-01"

    METRICS = "2023-10-01"
    
class KnowledgeLevels:
    """
    Supported knowledge hierarchy levels.
    """

    VM = "vm"

    RESOURCE_GROUP = "resource_group"

    SUBSCRIPTION = "subscription"

    MANAGEMENT_GROUP = "management-group"

    ENTERPRISE = "enterprise"