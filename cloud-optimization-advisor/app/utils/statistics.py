from math import ceil


class Statistics:
    """
    Statistical helper methods used by the recommendation engine.
    """

    @staticmethod
    def average(values: list[float]) -> float:

        if not values:
            return 0.0

        return round(sum(values) / len(values), 2)

    @staticmethod
    def maximum(values: list[float]) -> float:

        if not values:
            return 0.0

        return round(max(values), 2)

    @staticmethod
    def percentile(
        values: list[float],
        percentile: int
    ) -> float:

        if not values:
            return 0.0

        sorted_values = sorted(values)

        index = ceil(
            percentile / 100 * len(sorted_values)
        ) - 1

        index = max(index, 0)

        index = min(
            index,
            len(sorted_values) - 1
        )

        return round(
            sorted_values[index],
            2
        )

    @staticmethod
    def p95(values: list[float]) -> float:

        return Statistics.percentile(
            values,
            95
        )