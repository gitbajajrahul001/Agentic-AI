from rich.console import Console
from rich.table import Table

from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_virtual_machine_metrics import (
    AzureVirtualMachineMetrics,
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

        self.console.print(table)

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