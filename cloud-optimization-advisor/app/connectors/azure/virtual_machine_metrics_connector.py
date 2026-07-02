from datetime import datetime, timedelta

from app.connectors.azure.base_azure_connector import (
    BaseAzureConnector,
)

from app.core.constants import (
    AzureApiVersions,
    AzureMetricNames,
)

from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_virtual_machine_metrics import (
    AzureVirtualMachineMetrics,
)

from app.utils.statistics import (
    Statistics,
)


class VirtualMachineMetricsConnector(BaseAzureConnector):
    """
    Collects runtime telemetry for an Azure Virtual Machine.
    """

    def __init__(
        self,
        credential,
        observation_window: int,
    ):

        super().__init__(credential)

        self.observation_window = observation_window

    ####################################################################
    # Public API
    ####################################################################

    def get_virtual_machine_metrics(
        self,
        vm: AzureVirtualMachine,
    ) -> AzureVirtualMachineMetrics:

        metrics = AzureVirtualMachineMetrics()

        self._populate_cpu_metrics(
            vm,
            metrics,
        )

        self._populate_memory_metrics(
            vm,
            metrics,
        )

        self._populate_network_metrics(
            vm,
            metrics,
        )

        self._populate_disk_metrics(
            vm,
            metrics,
        )

        return metrics

    ####################################################################
    # CPU
    ####################################################################

    def _populate_cpu_metrics(
        self,
        vm: AzureVirtualMachine,
        metrics: AzureVirtualMachineMetrics,
    ) -> None:

        cpu_samples = self._get_metric_timeseries(
            vm,
            AzureMetricNames.CPU_PERCENTAGE,
        )

        metrics.sample_count = len(cpu_samples)

        metrics.cpu_average_percent = (
            Statistics.average(cpu_samples)
        )

        metrics.cpu_max_percent = (
            Statistics.maximum(cpu_samples)
        )

        metrics.cpu_p95_percent = (
            Statistics.p95(cpu_samples)
        )

    ####################################################################
    # Memory (Placeholder)
    ####################################################################

    def _populate_memory_metrics(
        self,
        vm: AzureVirtualMachine,
        metrics: AzureVirtualMachineMetrics,
    ) -> None:

        pass

    ####################################################################
    # Network (Placeholder)
    ####################################################################

    def _populate_network_metrics(
        self,
        vm: AzureVirtualMachine,
        metrics: AzureVirtualMachineMetrics,
    ) -> None:

        pass

    ####################################################################
    # Disk (Placeholder)
    ####################################################################

    def _populate_disk_metrics(
        self,
        vm: AzureVirtualMachine,
        metrics: AzureVirtualMachineMetrics,
    ) -> None:

        pass

    ####################################################################
    # Shared Metric Retrieval
    ####################################################################

    def _get_metric_timeseries(
        self,
        vm: AzureVirtualMachine,
        metric_name: str,
    ) -> list[float]:

        observation_end = datetime.utcnow()

        observation_start = (
            observation_end
            - timedelta(days=self.observation_window)
        )

        endpoint = (
            f"https://management.azure.com{vm.id}"
            f"/providers/Microsoft.Insights/metrics"
        )

        params = {

            "api-version": AzureApiVersions.METRICS,

            "metricnames": metric_name,

            "timespan":
                f"{observation_start.isoformat()}Z/"
                f"{observation_end.isoformat()}Z",

            "interval": "PT1H",

            "aggregation": "Average"

        }

        response = self._get(
            endpoint,
            params,
        )

        samples: list[float] = []

        for metric in response.get("value", []):

            for series in metric.get("timeseries", []):

                for point in series.get("data", []):

                    average = point.get("average")

                    if average is not None:

                        samples.append(float(average))

        return samples