from datetime import datetime
import calendar
import logging
from pathlib import Path

from config.settings import (
    ORGANIZATION_NAME,
    PROJECT_NAME,
    USER_EMAIL,
    PERSONAL_ACCESS_TOKEN,
    TARGET_VELOCITY,
)
from clients.azure_devops import AzureDevOpsClient
from services.calendar_service import CalendarService
from services.velocity_calculator import VelocityCalculator


def setup_logger() -> logging.Logger:
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "run.log"

    logger = logging.getLogger("dev-run")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def main() -> None:
    logger = setup_logger()

    today = datetime.today()
    start_of_month = datetime(today.year, today.month, 1)
    end_of_month = datetime(
        today.year,
        today.month,
        calendar.monthrange(today.year, today.month)[1],
    )

    logger.info(
        "Período analisado: %s até %s",
        start_of_month.strftime("%Y-%m-%d"),
        end_of_month.strftime("%Y-%m-%d"),
    )

    client = AzureDevOpsClient(
        ORGANIZATION_NAME,
        PROJECT_NAME,
        PERSONAL_ACCESS_TOKEN,
    )

    items = client.fetch_done_items_with_effort(
        USER_EMAIL,
        start_of_month.strftime("%Y-%m-%d"),
        end_of_month.strftime("%Y-%m-%d"),
    )

    if not items:
        logger.warning("Nenhum ticket com Effort finalizado neste mês.")
        return

    total_effort = VelocityCalculator.total_effort(items)
    total_business_value = VelocityCalculator.total_business_value(items)

    days_until_today = CalendarService.working_days_until_today(start_of_month)
    days_in_month = CalendarService.working_days_in_month(start_of_month, end_of_month)

    logger.info(
        "Velocidade atual: %.2f",
        VelocityCalculator.velocity(total_effort, days_until_today),
    )
    logger.info(
        "Velocidade final: %.2f",
        VelocityCalculator.velocity(total_effort, days_in_month),
    )
    logger.info(
        "Effort adicional necessário: %.2f",
        VelocityCalculator.additional_effort_for_target(
            TARGET_VELOCITY,
            days_in_month,
            total_effort,
        ),
    )
    logger.info(
        "Business Value (horas): %.2f",
        total_business_value / 60,
    )


if __name__ == "__main__":
    main()
