from rich.console import Console

from app.core.config_loader import ConfigLoader
from app.connectors.azure.authentication_connector import (
    AzureAuthenticationConnector,
)
from app.connectors.azure.subscription_connector import (
    SubscriptionConnector,
)
from app.connectors.azure.resource_graph_connector import (
    ResourceGraphConnector,
)

console = Console()


def main():

    console.rule("[bold blue]Cloud Optimization Advisor[/bold blue]")

    #
    # Load configuration
    #
    config = ConfigLoader.load()

    console.print(
        "✓ Configuration loaded successfully.",
        style="green"
    )

    #
    # Authenticate
    #
    authentication_connector = AzureAuthenticationConnector(
        config["azure"]
    )

    credential = authentication_connector.authenticate()

    console.print(
        "✓ Successfully authenticated to Azure.",
        style="green"
    )

    #
    # Discover subscriptions
    #
    subscription_connector = SubscriptionConnector(
        credential
    )

    subscription_ids = (
        subscription_connector.get_subscription_ids()
    )

    console.print(
        f"✓ Found {len(subscription_ids)} subscription(s).",
        style="green"
    )

    #
    # Discover virtual machines
    #
    resource_graph_connector = ResourceGraphConnector(
        credential,
        subscription_ids
    )

    virtual_machines = (
        resource_graph_connector.get_virtual_machines()
    )

    console.print(
        f"✓ Found {len(virtual_machines)} virtual machine(s).",
        style="green"
    )

    console.print()

    for vm in virtual_machines:

        console.print(
            f"{vm.name:30} {vm.vm_size:25} {vm.location}"
        )


if __name__ == "__main__":
    main()