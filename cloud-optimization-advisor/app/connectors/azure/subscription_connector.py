from azure.mgmt.subscription import SubscriptionClient


class SubscriptionConnector:
    """
    Azure Subscription Connector

    Responsibility
    --------------
    Retrieve all Azure subscriptions accessible
    by the authenticated Service Principal.
    """

    def __init__(self, credential):
        self.client = SubscriptionClient(credential)

    def get_subscription_ids(self) -> list[str]:
        """
        Returns a list of Azure Subscription IDs.
        """

        subscription_ids = []

        for subscription in self.client.subscriptions.list():
            subscription_ids.append(subscription.subscription_id)

        return subscription_ids

    def get_subscriptions(self):
        """
        Returns full subscription objects.
        Useful later for reporting.
        """

        return list(self.client.subscriptions.list())