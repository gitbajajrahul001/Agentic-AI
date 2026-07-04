import pprint

from rich.console import Console
from app.config.configuration_loader import ConfigurationLoader
from app.config.policy_loader import PolicyLoader
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

from app.models.vm_optimization_report import (
    VMOptimizationReport,
)

from app.connectors.azure.vm_sku_connector import (
    VmSkuConnector,
)

from app.models.azure_vm_sku import (
    AzureVmSku,
)

from app.config.supported_vm_sizes_loader import (
    SupportedVmSizesLoader,
)

from app.sizing.vm_sizing_engine import (
    VmSizingEngine,
)

from app.validation.validation_engine import (
    ValidationEngine,
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
    config = ConfigurationLoader.load()
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
    # Azure VM SKUs
    ####################################################################

    #sku_connector = VmSkuConnector(
     #   credential,
      #  subscription_ids[0],
    #)

    #vm_skus = sku_connector.get_vm_skus()

    #from pprint import pprint

    #print(type(vm_skus[0]))
    #print("=" * 80)

    #pprint(vm_skus[0].as_dict())

    #return

    #console.print(
     #   f"✓ Retrieved {len(vm_skus)} Azure VM SKUs.",
      #  style="green"
    #)


    ####################################################################
    # Supported VM Sizes
    ####################################################################

    supported_vm_sizes = (
        SupportedVmSizesLoader.load()
    )

    ####################################################################
    # Azure VM SKUs
    ####################################################################

    sku_connector = VmSkuConnector(
        credential,
        subscription_ids[0],
    )

    vm_skus = sku_connector.get_vm_skus()

    console.print(
        f"✓ Retrieved {len(vm_skus)} Azure VM SKUs.",
        style="green",
    )

    ####################################################################
    # Organization Supported SKUs
    ####################################################################

    sku_lookup = {
        sku.name: sku
        for sku in vm_skus
    }

    supported_skus = [
        sku_lookup[vm_size]
        for vm_size in supported_vm_sizes
        if vm_size in sku_lookup
    ]

    console.print(
        f"✓ Loaded {len(supported_skus)} supported VM SKUs.",
        style="green",
    )



    ####################################################################
    # VM Sizing Engine
    ####################################################################

    vm_sizing_engine = (
        VmSizingEngine(
            supported_skus
        )
    )
    validation_engine = (
        ValidationEngine()
    )













    # --------------------------------------------------------
    # TEMPORARY DEBUG
    # --------------------------------------------------------

    #print(vm_skus[0])

    #print(vm_skus[0].capability_int("vCPUs"))
    #print(vm_skus[0].capability_int("MemoryGB"))
    #print(vm_skus[0].capability_bool("PremiumIO"))
    #print(vm_skus[0].capability_int("MaxDataDiskCount"))

    #return

    # --------------------------------------------------------
    # END DEBUG
    # --------------------------------------------------------

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
    #print(virtual_machines[0].storage_profile)
    #print(virtual_machines[0].network_profile)
    #print(virtual_machines[0].security_profile)
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
    #renderer.render_virtual_machines(
     #   virtual_machines
    #)
    
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
    #vm = virtual_machines[0]
    #metrics = metrics_connector.get_virtual_machine_metrics(
     #   vm
    #)    
    #renderer.render_vm_metrics(
     #   metrics
    #)
    #
    #analysis = recommendation_engine.analyze(
    #    vm,
    #    metrics,
    #)
    
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
    
    #renderer.render_vm_analysis(
    #analysis
#)
####################################################################
# Optimization Reports
####################################################################

    reports = []

    for vm in virtual_machines:

        metrics = (
            metrics_connector.get_virtual_machine_metrics(
                vm
            )
        )

        analysis = (
            recommendation_engine.analyze(
                vm,
                metrics,
            )
        )
        #analysis.recommended_vm_size = (
            #vm_sizing_engine.recommend_size(
             #   vm.vm_size,
              #  analysis.recommendation,
            #)
        #)
        candidate = (
            vm_sizing_engine.recommend_size(
                vm.vm_size,
                analysis.recommendation,
            )   
        )
        #print(type(candidate))
        #print(candidate)

        if (
            candidate
            and
            validation_engine.validate(
            vm,
            candidate,
            )
        ):
            analysis.recommended_vm_size = (
                candidate.name
        )

        reports.append(
            VMOptimizationReport(
                virtual_machine=vm,
                metrics=metrics,
                analysis=analysis,
            )
        )
    

    renderer.render_summary(
        reports
    )

    renderer.render_dashboard(
        reports
    )
    

if __name__ == "__main__":
    main()