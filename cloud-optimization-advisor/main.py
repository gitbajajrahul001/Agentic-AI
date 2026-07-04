import pprint
import warnings

warnings.simplefilter("error", UserWarning)

warnings.filterwarnings("error")

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

from app.models.candidate_evaluation import (
    CandidateEvaluation,
)

from app.connectors.azure.pricing_connector import (
    PricingConnector,
)
from app.metadata.metadata_engine import (
    MetadataEngine,
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
    # Metadata Configuration
    ####################################################################

    metadata_configuration = ConfigurationLoader.load(
        "metadata_configuration"
    )

    console.print(
        "✓ Metadata configuration loaded.",
        style="green",
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
    
    ####################################################################
    # Recommendation Engine
    ####################################################################
    recommendation_engine = RecommendationEngine(
        recommendation_policy
    )
    ####################################################################
    # Pricing Engine
    ####################################################################
    pricing_connector = PricingConnector()
    
    HOURS_PER_MONTH = 730

    ####################################################################
    # Metadata Engine
    ####################################################################
    metadata_configuration = ConfigurationLoader.load(
        "metadata_configuration"
    )
    metadata_engine = MetadataEngine(
        metadata_configuration,
    )

    ####################################################################
    # Optimization Reports
    ####################################################################

    reports = []

    for vm in virtual_machines:

        ###############################################################
        # Metrics
        ###############################################################

        metrics = (
            metrics_connector.get_virtual_machine_metrics(
                vm
            )
        )

        ###############################################################
        # Initial Recommendation
        ###############################################################

        analysis = (
            recommendation_engine.analyze(
                vm,
                metrics,
            )
        )

        ###############################################################
        # Report
        ###############################################################

        report = VMOptimizationReport(

            virtual_machine=vm,

            metrics=metrics,

            analysis=analysis,
        )
        
        report.policy_version = recommendation_policy[
            "policy"
        ][
            "version"
        ]

        report.metadata = metadata_engine.extract_metadata(
            vm.tags,
        )
        
        ###############################################################
        # Default Recommendation
        ###############################################################

        analysis.recommended_vm_size = (
            vm.vm_size
        )

        ###############################################################
        # Candidate Evaluation
        ###############################################################

        candidates = (
            vm_sizing_engine.get_candidates(
                vm.vm_size,
                analysis.recommendation,
            )
        )

        for candidate in candidates:

            summary = validation_engine.validate(
                vm,
                candidate,
            )

            evaluation = CandidateEvaluation(

                candidate_vm_size=candidate.name,

                validation_summary=summary,

                passed_validation=summary.passed,
            )

            analysis.candidate_evaluations.append(
                evaluation
            )

            if summary.passed:

                analysis.recommended_vm_size = (
                    candidate.name
                )

                break

        ###############################################################
        # Cost Analysis
        ###############################################################

        current_price = pricing_connector.get_vm_price(

            region=vm.location,

            vm_size=vm.vm_size,
        )

        recommended_price = pricing_connector.get_vm_price(

            region=vm.location,

            vm_size=analysis.recommended_vm_size,
        )

        report.cost_analysis.currency = (
            current_price.currency
        )

        report.cost_analysis.current_hourly_cost = (
            current_price.hourly_price
        )

        report.cost_analysis.recommended_hourly_cost = (
            recommended_price.hourly_price
        )

        report.cost_analysis.current_monthly_cost = (
            current_price.hourly_price
            * HOURS_PER_MONTH
        )

        report.cost_analysis.recommended_monthly_cost = (
            recommended_price.hourly_price
            * HOURS_PER_MONTH
        )

        report.cost_analysis.monthly_savings = (
            report.cost_analysis.current_monthly_cost
            -
            report.cost_analysis.recommended_monthly_cost
        )

        report.cost_analysis.yearly_savings = (
            report.cost_analysis.monthly_savings
            * 12
        )

        ###############################################################
        # Store Report
        ###############################################################

        reports.append(
            report
        )

    ####################################################################
    # Render
    ####################################################################

    renderer.render_summary(
        reports
    )

    renderer.render_dashboard(
        reports
    )

    renderer.render_detailed_report(
        reports
    )

################    
if __name__ == "__main__":
        main()
################