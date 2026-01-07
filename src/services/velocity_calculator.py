class VelocityCalculator:
    @staticmethod
    def total_effort(items: list[dict]) -> float:
        return sum(
            item["fields"].get("Microsoft.VSTS.Scheduling.Effort", 0)
            for item in items
        )

    @staticmethod
    def total_business_value(items: list[dict]) -> int:
        return sum(
            item["fields"].get("Microsoft.VSTS.Common.BusinessValue", 0)
            for item in items
        )

    @staticmethod
    def velocity(effort: float, days: int) -> float:
        return effort / days if days > 0 else 0

    @staticmethod
    def additional_effort_for_target(
        target_velocity: float,
        total_days: int,
        current_effort: float,
    ) -> float:
        required = target_velocity * total_days
        return max(0, required - current_effort)
