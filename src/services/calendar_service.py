from datetime import datetime, timedelta

class CalendarService:
    @staticmethod
    def working_days_until_today(start_of_month: datetime) -> int:
        today = datetime.today()
        return sum(
            1
            for i in range(today.day)
            if (start_of_month + timedelta(days=i)).weekday() < 5
        )

    @staticmethod
    def working_days_in_month(start_of_month: datetime, end_of_month: datetime) -> int:
        return sum(
            1
            for i in range((end_of_month - start_of_month).days + 1)
            if (start_of_month + timedelta(days=i)).weekday() < 5
        )
