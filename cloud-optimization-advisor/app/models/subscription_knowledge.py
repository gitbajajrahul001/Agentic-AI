from pydantic import BaseModel


class SubscriptionKnowledge(BaseModel):

    execution: dict

    subscription: dict

    inventory: dict

    optimization: dict

    financial: dict

    insights: dict

    source_documents: list[str]