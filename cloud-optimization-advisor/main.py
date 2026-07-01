from rich.console import Console

from app.core.config_loader import ConfigLoader
from app.models.azure_virtual_machine import AzureVirtualMachine

console = Console()


def main():

    console.rule("[bold blue]Cloud Optimization Advisor[/bold blue]")

    config = ConfigLoader.load()

    console.print("✓ Configuration loaded successfully.", style="green")

    vm = AzureVirtualMachine(
        id="/subscriptions/xxxxxxxx/resourceGroups/payroll-rg/providers/Microsoft.Compute/virtualMachines/payroll-01",
        name="payroll-01",
        subscription_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        resource_group="payroll-rg",
        location="eastus",
        vm_size="Standard_D16s_v5",
        operating_system="Windows",
        power_state="VM running",
        tags={
            "Environment": "Production",
            "Application": "Payroll",
            "Owner": "Finance Team"
        }
    )

    console.print()
    console.print(vm)


if __name__ == "__main__":
    main()