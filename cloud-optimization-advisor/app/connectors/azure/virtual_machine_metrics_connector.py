from datetime import (
    datetime,
    timedelta,
    timezone,
)

from azure.monitor.query import (
    LogsQueryClient,
    LogsQueryStatus,
)

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

    CPU:
        Azure Monitor Metrics API

    Memory:
        Azure Log Analytics (Perf table)
    """

    def __init__(
        self,
        credential,
        observation_window: int,
        workspace_id: str,
    ):

        super().__init__(credential)

        self.observation_window = observation_window

        self.logs_client = LogsQueryClient(
            credential
        )

        self.workspace_id = workspace_id

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

        #
        # Remaining telemetry
        #

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

        samples = self._get_metric_timeseries(
            vm,
            AzureMetricNames.CPU_PERCENTAGE,
        )

        metrics.sample_count = len(samples)

        metrics.cpu_average_percent = (
            Statistics.average(samples)
        )

        metrics.cpu_max_percent = (
            Statistics.maximum(samples)
        )

        metrics.cpu_p95_percent = (
            Statistics.p95(samples)
        )

    ####################################################################
    # Memory
    ####################################################################

    def _populate_memory_metrics(
        self,
        vm: AzureVirtualMachine,
        metrics: AzureVirtualMachineMetrics,
    ) -> None:

        samples = self._get_memory_timeseries(
            vm
        )

        if not samples:
            return
        
        metrics.memory_metrics_available = True

        metrics.memory_average_percent = (
            Statistics.average(samples)
        )

        metrics.memory_max_percent = (
            Statistics.maximum(samples)
        )

        metrics.memory_p95_percent = (
            Statistics.p95(samples)
        )

    ####################################################################
    # Network
    ####################################################################

    def _populate_network_metrics(
        self,
        vm: AzureVirtualMachine,
        metrics: AzureVirtualMachineMetrics,
    ) -> None:

        #
        # MVP
        #
        # Implement later
        #

        pass

    ####################################################################
    # Disk
    ####################################################################

    def _populate_disk_metrics(
        self,
        vm: AzureVirtualMachine,
        metrics: AzureVirtualMachineMetrics,
    ) -> None:

        #
        # MVP
        #
        # Implement later
        #

        pass

    ####################################################################
    # Azure Monitor
    ####################################################################

    def _get_metric_timeseries(
        self,
        vm: AzureVirtualMachine,
        metric_name: str,
    ) -> list[float]:
        """
        Retrieves hourly metric samples from Azure Monitor.
        """

        observation_end = datetime.now(
        timezone.utc
)

        observation_start = (
            observation_end -
            timedelta(days=self.observation_window)
        )

        endpoint = (
            f"https://management.azure.com{vm.id}"
            "/providers/Microsoft.Insights/metrics"
        )

        params = {
            "api-version": AzureApiVersions.METRICS,
            "metricnames": metric_name,
            "timespan": (
            f"{observation_start.strftime('%Y-%m-%dT%H:%M:%SZ')}/"
            f"{observation_end.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            ),
            "interval": "PT1H",
            "aggregation": "Average",
        }

        response = self._get(
            endpoint,
            params,
        )

        samples: list[float] = []

        for metric in response.get("value", []):
            for series in metric.get("timeseries", []):
                for point in series.get("data", []):
                    value = point.get("average")

                    if value is not None:
                        samples.append(
                            float(value)
                        )

        return samples

    ####################################################################
    # Azure Log Analytics
    ####################################################################

    def _get_memory_timeseries(
        self,
        vm: AzureVirtualMachine,
    ) -> list[float]:
        """
        Retrieves Memory utilization from the Perf table.

        Counter:
            % Committed Bytes In Use
        """
        
        counter_name = (
            "% Used Memory"
            if vm.operating_system == "Linux"
            else "% Committed Bytes In Use"
        )

        query = f"""
Perf
| where TimeGenerated > ago({self.observation_window}d)
| where _ResourceId == "{vm.id.lower()}"
| where ObjectName == "Memory"
| where CounterName == "{counter_name}"
| project TimeGenerated, CounterValue
| order by TimeGenerated asc
"""

        observation_end = datetime.now(
            timezone.utc
        )

        observation_start = (
            observation_end -
            timedelta(days=self.observation_window)
        )
        

        result = self.logs_client.query_workspace(
            workspace_id=self.workspace_id,
            query=query,
            timespan=(
                observation_start,
                observation_end,
            ),
        )

        if result.status != LogsQueryStatus.SUCCESS:
            return []

        if not result.tables:
            return []

        table = result.tables[0]

        if not table.rows:
            return []

        counter_value_index = table.columns.index(
            "CounterValue"
        )

        samples = []

        for row in table.rows:
            samples.append(
                float(row[counter_value_index])
            )

        return samples