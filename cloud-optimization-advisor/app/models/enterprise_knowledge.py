from pydantic import BaseModel


class EnterpriseKnowledge(BaseModel):

    execution: dict

    enterprise: dict

    inventory: dict

    optimization: dict

    financial: dict

    insights: dict

    source_documents: list[str]