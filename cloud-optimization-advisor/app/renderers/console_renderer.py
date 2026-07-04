from rich.console import Console
from rich.table import Table

from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_virtual_machine_metrics import (
    AzureVirtualMachineMetrics,
)

from app.models.vm_optimization_report import (
    VMOptimizationReport,
)




class ConsoleRenderer:
    """
    Responsible for rendering application output
    to the console.

    This class should contain NO business logic.
    It only displays domain objects.
    """

    def __init__(self):

        self.console = Console()

    ####################################################################
    # Virtual Machines
    ####################################################################

    def render_virtual_machines(
        self,
        virtual_machines: list[AzureVirtualMachine]
    ) -> None:

        table = Table(
            title="Azure Virtual Machines"
        )

        table.add_column("Name")

        table.add_column("VM Size")

        table.add_column("Location")

        for vm in virtual_machines:

            table.add_row(

                vm.name,

                vm.vm_size,

                vm.location

            )

        self.console.print(table)

    ####################################################################
    # VM Metrics
    ####################################################################

    def render_vm_metrics(
        self,
        metrics: AzureVirtualMachineMetrics
    ) -> None:

        table = Table(
            title="Virtual Machine Metrics"
        )

        table.add_column(
            "Metric",
            style="cyan"
        )

        table.add_column(
            "Value",
            justify="right"
        )

        #
        # CPU
        #

        table.add_row(
            "CPU Average (%)",
            f"{metrics.cpu_average_percent:.2f}"
        )

        table.add_row(
            "CPU Maximum (%)",
            f"{metrics.cpu_max_percent:.2f}"
        )

        table.add_row(
            "CPU P95 (%)",
            f"{metrics.cpu_p95_percent:.2f}"
        )

        table.add_section()

        #
        # Memory
        #

        table.add_row(
            "Memory Average (%)",
            f"{metrics.memory_average_percent:.2f}"
        )

        table.add_row(
            "Memory Maximum (%)",
            f"{metrics.memory_max_percent:.2f}"
        )

        table.add_row(
            "Memory P95 (%)",
            f"{metrics.memory_p95_percent:.2f}"
        )

        table.add_section()

        #
        # Telemetry
        #

        table.add_row(
            "Sample Count",
            str(metrics.sample_count)
        )

        self.console.print(table)
    ####################################################################
    # VM Analysis
    ####################################################################

    def render_vm_analysis(
        self,
        analysis,
    ) -> None:

        table = Table(
            title="Virtual Machine Analysis"
        )

        table.add_column(
            "Property",
            style="cyan"
        )

        table.add_column(
            "Value"
        )

        table.add_row(
            "Recommendation",
            analysis.recommendation.value
        )

        table.add_row(
            "Confidence",
            analysis.confidence.value
        )

        table.add_row(
            "Current VM Size",
            analysis.current_vm_size
        )

        if analysis.recommended_vm_size:

            table.add_row(
                "Recommended VM Size",
                analysis.recommended_vm_size
            )

        #self.console.print(table)

        observations = Table(
            title="Observations"
        )

        observations.add_column(
            "Observation",
            style="green"
        )

        for observation in analysis.observations:

            observations.add_row(
                f"✓ {observation}"
            )

        self.console.print(
            observations
        )    
    ####################################################################
    # Optimization Recommendations
    ####################################################################

    def render_dashboard(
        self,
        reports: list[VMOptimizationReport],
    ) -> None:

        table = Table(
            title="Optimization Recommendations"
        )

        table.add_column(
            "VM",
        )

        table.add_column(
            "Current SKU",
        )

        table.add_column(
            "Target SKU",
        )

        table.add_column(
            "Recommendation",
        )

        table.add_column(
            "Monthly Savings",
            justify="right",
        )

        table.add_column(
            "Annual Savings",
            justify="right",
        )

        for report in reports:

            monthly_savings = (
                f"${report.cost_analysis.monthly_savings:.2f}"
            )

            annual_savings = (
                f"${report.cost_analysis.yearly_savings:.2f}"
            )

            if report.cost_analysis.monthly_savings > 0:

                monthly_savings = (
                    f"[green]{monthly_savings}[/green]"
                )

            if report.cost_analysis.yearly_savings > 0:

                annual_savings = (
                    f"[green]{annual_savings}[/green]"
                )

            if (
                report.analysis.recommended_vm_size
                ==
                report.virtual_machine.vm_size
            ):

                final_recommendation = (
                    "Keep Current Size"
                )

            else:

                final_recommendation = (
                    report.analysis.recommendation.value
                    .replace("_", " ")
                    .title()
                )

            table.add_row(

                report.virtual_machine.name,

                report.virtual_machine.vm_size,

                report.analysis.recommended_vm_size,

                final_recommendation,

                monthly_savings,

                annual_savings,
            )
        self.console.print(table)

            ####################################################################
            # Cloud Optimization Summary
            ####################################################################

    def render_summary(
        self,
        reports,
    ):
        table = Table(
            title="Cloud Optimization Summary"
        )

        table.add_column(
            "Metric",
            style="bold cyan",
        )

        table.add_column(
            "Value",
            justify="right",
        )

        vm_count = len(reports)

        current_monthly_cost = sum(

            report.cost_analysis.current_monthly_cost

            for report in reports
        )

        optimized_monthly_cost = sum(

            report.cost_analysis.recommended_monthly_cost

            for report in reports
        )

        monthly_savings = sum(

            report.cost_analysis.monthly_savings

            for report in reports
        )

        annual_savings = sum(

            report.cost_analysis.yearly_savings

            for report in reports
        )

        table.add_row(
            "Virtual Machines Analyzed",
            str(vm_count),
        )

        table.add_row(
            "Current Monthly Cost",
            f"${current_monthly_cost:.2f}",
        )

        table.add_row(
            "Optimized Monthly Cost",
            f"${optimized_monthly_cost:.2f}",
        )

        table.add_row(
            "Estimated Monthly Savings",
            f"${monthly_savings:.2f}",
        )

        table.add_row(
            "Estimated Annual Savings",
            f"${annual_savings:.2f}",
        )

        self.console.print(table)
    
####################################################################
# Detailed Report
####################################################################

    def render_detailed_report(
        self,
        reports: list[VMOptimizationReport],
    ) -> None:

        self.console.rule(
            "[bold cyan]Detailed Recommendation Report[/bold cyan]"
        )

        for report in reports:

            self.console.print()

            #
            # VM
            #

            self.console.print()

            self.console.print(
                "[bold cyan]Resource Details[/bold cyan]"
            )

            self.console.print(
                f"    [bold]VM Hostname:[/bold] "
                f"{report.virtual_machine.name}"
            )

            self.console.print(
                f"    [bold]Subscription ID:[/bold] "
                f"{report.virtual_machine.subscription_id}"
            )

            self.console.print(
                f"    [bold]Resource Group:[/bold] "
                f"{report.virtual_machine.resource_group}"
            )

            self.console.print(
                f"    [bold]Azure Region:[/bold] "
                f"{report.virtual_machine.location}"
            )

            self.console.print(
                f"    [bold]Current VM SKU:[/bold] "
                f"{report.virtual_machine.vm_size}"
            )
            
            ####################################################################
            # Business Metadata
            ####################################################################

            for key, value in report.metadata.items():

                if not value:
                    continue

                display_name = (
                    key.replace(
                        "_",
                        " ",
                    ).title()
                )

                self.console.print(
                    f"    [bold]{display_name}: [/bold]"
                    f"{value} "
                )

            self.console.print()
            
            
            self.console.print(
                "[bold cyan]Pre-Evaluation Recommendation[/bold cyan]"
            )

            self.console.print(
                f"    {report.analysis.recommendation.value.replace('_', ' ').title()}"
            )

            self.console.print()
            
                        #
            # Recommendation Rationale
            #

            if report.analysis.reasons:

                self.console.print()

                self.console.print(
                    "[bold cyan]Recommendation Rationale[/bold cyan]"
                )

                for reason in report.analysis.reasons:

                    self.console.print(
                        f"    [bold]{reason.category}[/bold]"
                    )

                    self.console.print(
                        f"        {reason.message}"
                    )

                    self.console.print()

            #
            # Candidate Evaluations
            #
            
            self.console.print(
                "[bold cyan]Evaluation Results[/bold cyan]"
            )

            for evaluation in report.analysis.candidate_evaluations:

                self.console.print(
                    f"    [bold green]Candidate VM SKU:[/bold green] "
                    f"{evaluation.candidate_vm_size}"
                )

                grouped_results = {}

                for result in evaluation.validation_summary.results:

                    grouped_results.setdefault(
                        result.domain,
                        [],
                    ).append(result)
                    
                for domain, results in grouped_results.items():

                    self.console.print()

                    self.console.print(
                        f"[#FFB000]{domain}[/#FFB000]"
                    )

                    self.console.print(
                        "-" * len(domain)
                    )

                    for result in results:

                        icon = (
                            "[green]✓[/green]"
                            if result.passed
                            else "[red]✗[/red]"
                        )

                        self.console.print(
                            f"    {icon} "
                            f"[bold]{result.rule}[/bold]: "
                            f"{result.message}"
                        )

            #
            # Final Recommendation
            #

            post_recommendation = (
                report.analysis.recommendation.value
                .replace("_", " ")
                .title()
            )

            if (
                report.analysis.recommended_vm_size
                ==
                report.virtual_machine.vm_size
            ):
                post_recommendation = "Keep Current Size"
            else:
                post_recommendation = (
                    report.analysis.recommendation.value
                    .replace("_", " ")
                    .title()
                )

            self.console.print()

            self.console.print(
                "[bold cyan]Post-Evaluation Recommendation[/bold cyan]"
            )
                        
            self.console.print(
                f"    {post_recommendation}"
            )
            self.console.print()
            
            self.console.print(
                "[bold cyan]Recommended Target SKU[/bold cyan]"
            )
            self.console.print(
                f"    {report.analysis.recommended_vm_size}"
            )
            self.console.print()

            self.console.print(
                "[bold cyan]Cost Analysis[/bold cyan]"
            )

            self.console.print(
                f"    [bold]Currency:[/bold] "
                f"{report.cost_analysis.currency}"
            )

            self.console.print(
                f"    [bold]Current Hourly Cost:[/bold] "
                f"${report.cost_analysis.current_hourly_cost:.4f}"
            )

            self.console.print(
                f"    [bold]Recommended Hourly Cost:[/bold] "
                f"${report.cost_analysis.recommended_hourly_cost:.4f}"
            )

            self.console.print(
                f"    [bold]Current Monthly Cost:[/bold] "
                f"${report.cost_analysis.current_monthly_cost:.2f}"
            )

            self.console.print(
                f"    [bold]Recommended Monthly Cost:[/bold] "
                f"${report.cost_analysis.recommended_monthly_cost:.2f}"
            )

            self.console.print(
                f"    [bold]Estimated Monthly Savings:[/bold] "
                f"${report.cost_analysis.monthly_savings:.2f}"
            )

            self.console.print(
                f"    [bold]Estimated Annual Savings:[/bold] "
                f"${report.cost_analysis.yearly_savings:.2f}"
            )



            self.console.rule()
            
            