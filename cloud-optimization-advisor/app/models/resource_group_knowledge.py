from pydantic import BaseModel

class ResourceGroupKnowledge(BaseModel):

    execution: dict

    resource_group: dict

    inventory: dict

    optimization: dict

    financial: dict

    insights: dict

    source_documents: list[str]