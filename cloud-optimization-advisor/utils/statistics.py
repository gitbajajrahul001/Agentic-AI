from typing import List


class Statistics:

    @staticmethod
    def average(values: List[float]) -> float:

        if not values:
            return 0.0

        return sum(values) / len(values)

    @staticmethod
    def maximum(values: List[float]) -> float:

        if not values:
            return 0.0

        return max(values)

    @staticmethod
    def p95(values: List[float]) -> float:

        if not values:
            return 0.0

        values = sorted(values)

        index = int(0.95 * (len(values) - 1))

        return values[index]