from rich.console import Console

from app.core.config_loader import ConfigLoader
from app.connectors.azure.authentication_connector import (
    AzureAuthenticationConnector,
)
from app.connectors.azure.subscription_connector import (
    SubscriptionConnector,
)

console = Console()


def main():

    console.rule("[bold blue]Cloud Optimization Advisor[/bold blue]")

    #
    # Load Configuration
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

    console.print()

    for subscription_id in subscription_ids:
        console.print(f"• {subscription_id}")


if __name__ == "__main__":
    main()