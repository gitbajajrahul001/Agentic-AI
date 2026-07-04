from pydantic import BaseModel


class CostAnalysis(BaseModel):
    """
    Cost comparison between the current
    and recommended VM.
    """

    currency: str = "USD"

    current_hourly_cost: float = 0.0

    recommended_hourly_cost: float = 0.0

    current_monthly_cost: float = 0.0

    recommended_monthly_cost: float = 0.0

    monthly_savings: float = 0.0

    yearly_savings: float = 0.0