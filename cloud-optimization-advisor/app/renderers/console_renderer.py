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
    # Optimization Dashboard
    ####################################################################

    def render_dashboard(
        self,
        reports: list[VMOptimizationReport],
    ) -> None:

        table = Table(
            title="Cloud Optimization Advisor"
        )

        table.add_column(
            "VM",
            style="cyan",
        )
        table.add_column(
            "Region",
        )        

        table.add_column(
            "Current Size",
        )

        table.add_column(
            "CPU Avg %",
            justify="right",
        )

        table.add_column(
            "Memory Avg %",
            justify="right",
        )

        table.add_column(
            "Recommendation",
        )

        table.add_column(
            "Confidence",
        )

        table.add_column(
            "Recommended Size",
        )

        for report in reports:

            recommended_size = (
                report.analysis.recommended_vm_size
                or "N/A"
            )

            recommendation_value = (
                report.analysis.recommendation.value
            )

            recommendation = (
                recommendation_value
                .replace("_", " ")
                .title()
            )

            if recommendation_value == "UPSIZE":
                recommendation = f"[yellow]{recommendation}[/yellow]"

            elif recommendation_value == "DOWNSIZE":
                recommendation = f"[green]{recommendation}[/green]"

            elif recommendation_value == "KEEP_CURRENT_SIZE":
                recommendation = f"[cyan]{recommendation}[/cyan]"

            else:
                recommendation = f"[red]{recommendation}[/red]"

            confidence = (
                report.analysis.confidence.value
                .replace("_", " ")
                .title()
            )

            table.add_row(
                report.virtual_machine.name,
                report.virtual_machine.location,
                report.virtual_machine.vm_size,
                f"{report.metrics.cpu_average_percent:.2f}%",
                f"{report.metrics.memory_average_percent:.2f}%",
                recommendation,
                confidence,
                recommended_size,
            )
        self.console.print(table)

####################################################################
# Optimization Summary
####################################################################

    def render_summary(
        self,
        reports: list[VMOptimizationReport],
    ) -> None:

        upsize = 0
        downsize = 0
        keep = 0
        insufficient = 0

        for report in reports:

            action = report.analysis.recommendation.value

            if action == "UPSIZE":
                upsize += 1

            elif action == "DOWNSIZE":
                downsize += 1

            elif action == "KEEP_CURRENT_SIZE":
                keep += 1

            else:
                insufficient += 1

        table = Table(
            title="Cloud Optimization Summary"
        )

        table.add_column(
            "Metric",
            style="cyan",
        )

        table.add_column(
            "Value",
            justify="right",
        )

        table.add_row(
            "Virtual Machines",
            str(len(reports)),
        )

        table.add_row(
            "Upsize",
            str(upsize),
        )

        table.add_row(
            "Downsize",
            str(downsize),
        )

        table.add_row(
            "Keep Current Size",
            str(keep),
        )

        table.add_row(
            "Insufficient Data",
            str(insufficient),
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

            self.console.print()
            
            
            self.console.print(
                "[bold cyan]Pre-Evaluation Recommendation[/bold cyan]"
            )

            self.console.print(
                f"    {report.analysis.recommendation.value.replace('_', ' ').title()}"
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

                for result in evaluation.validation_summary.results:

                    icon = (
                        "[green]✓[/green]"
                        if result.passed
                        else "[red]✗[/red]"
                    )

                    self.console.print(
                        f"        {icon} "
                        f"[bold]{result.rule}:[/bold] "
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

            self.console.rule()
            
            