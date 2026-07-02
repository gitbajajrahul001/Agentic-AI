from rich.console import Console
from app.core.config_loader import ConfigLoader
from app.core.policy_loader import PolicyLoader
from app.connectors.azure.authentication_connector import (
    AzureAuthenticationConnector,
)
from app.connectors.azure.subscription_connector import (
    SubscriptionConnector,
)
from app.connectors.azure.resource_graph_connector import (
    ResourceGraphConnector,
)
from app.connectors.azure.virtual_machine_metrics_connector import (
    VirtualMachineMetricsConnector,
)
from app.renderers.console_renderer import (
    ConsoleRenderer,
)
from app.recommendation.recommendation_engine import (
    RecommendationEngine,
)

console = Console()

def main():
    """
    Cloud Optimization Advisor
    Application Entry Point
    """
    console.rule(
        "[bold blue]Cloud Optimization Advisor[/bold blue]"
    )
    
    ####################################################################
    # Configuration
    ####################################################################
    config = ConfigLoader.load()
    console.print(
        "✓ Configuration loaded successfully.",
        style="green"
    )
    
    ####################################################################
    # Recommendation Policies
    ####################################################################
    recommendation_policy = PolicyLoader.load(
        "recommendation_policy"
    )
    console.print(
        "✓ Recommendation policy loaded.",
        style="green"
    )
    
    ####################################################################
    # Authentication
    ####################################################################
    authentication_connector = (
        AzureAuthenticationConnector(
            config["azure"]
        )
    )
    credential = (
        authentication_connector.authenticate()
    )
    console.print(
        "✓ Successfully authenticated to Azure.",
        style="green"
    )
    
    ####################################################################
    # Subscriptions
    ####################################################################
    subscription_connector = (
        SubscriptionConnector(
            credential
        )
    )
    subscription_ids = (
        subscription_connector.get_subscription_ids()
    )
    console.print(
        f"✓ Found {len(subscription_ids)} subscription(s).",
        style="green"
    )
    
    ####################################################################
    # Virtual Machine Inventory
    ####################################################################
    resource_graph_connector = (
        ResourceGraphConnector(
            credential,
            subscription_ids,
        )
    )
    virtual_machines = (
        resource_graph_connector.get_virtual_machines()
    )
    console.print(
        f"✓ Found {len(virtual_machines)} virtual machine(s).",
        style="green"
    )
    
    if not virtual_machines:
        console.print(
            "[yellow]No Azure Virtual Machines found.[/yellow]"
        )
        return
        
    ####################################################################
    # Metrics Collection
    ####################################################################
    metrics_connector = (
        VirtualMachineMetricsConnector(
            credential,
            config["observation_window"],
            config["log_analytics"]["workspace_id"],
        )
    )
    
    ####################################################################
    # Presentation
    ####################################################################
    renderer = ConsoleRenderer()
    renderer.render_virtual_machines(
        virtual_machines
    )
    
    ####################################################################
    # Recommendation Engine
    ####################################################################
    recommendation_engine = RecommendationEngine(
        recommendation_policy
    )
    
    ####################################################################
    # MVP
    #
    # Process the first VM only.
    ####################################################################
    vm = virtual_machines[0]
    metrics = metrics_connector.get_virtual_machine_metrics(
        vm
    )    
    renderer.render_vm_metrics(
        metrics
    )
    
    analysis = recommendation_engine.analyze(
        vm,
        metrics,
    )
    
    #print()
    #print("Recommendation")
    #print("----------------")
    #print(analysis.recommendation)
    #print()
    #print("Confidence")
    #print("----------")
    #print(analysis.confidence)
    #print()
    #print("Observations")
    #print("------------")
    #for observation in analysis.observations:
        #print(f"- {observation}")
    
    renderer.render_vm_analysis(
    analysis
)
if __name__ == "__main__":
    main()