import requests

from app.models.vm_price import (
    VmPrice,
)


class PricingConnector:
    """
    Retrieves Azure Retail VM pricing.
    """

    ENDPOINT = (
        "https://prices.azure.com/api/retail/prices"
    )

    def __init__(self):

        self._cache: dict[
            tuple[str, str],
            VmPrice,
        ] = {}

    ####################################################################
    # Public API
    ####################################################################

    def get_vm_price(
        self,
        region: str,
        vm_size: str,
    ) -> VmPrice:

        cache_key = (
            region.lower(),
            vm_size.lower(),
        )

        if cache_key in self._cache:

            return self._cache[cache_key]

        params = {

            "$filter": (

                "serviceName eq 'Virtual Machines' "

                f"and armRegionName eq '{region}' "

                f"and armSkuName eq '{vm_size}' "

                "and priceType eq 'Consumption'"

            )

        }

        response = requests.get(

            self.ENDPOINT,

            params=params,

            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        items = data.get(
            "Items",
            [],
        )

        if not items:

            raise Exception(

                f"No pricing found for "

                f"{vm_size} in {region}"

            )

        item = items[0]

        price = VmPrice(

            vm_size=vm_size,

            region=region,

            currency=item["currencyCode"],

            hourly_price=item["unitPrice"],
        )

        self._cache[cache_key] = price

        return price