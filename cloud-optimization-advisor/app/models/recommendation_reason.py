from pydantic import BaseModel


class RecommendationReason(BaseModel):
    """
    Explains why a recommendation was made.
    """

    category: str

    message: str