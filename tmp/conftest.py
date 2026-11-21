import logging
import time

import pytest
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def log_test_start_end(request):
    """Логгирует начало и конец каждого теста."""

    logger = logging.getLogger(request.module.__name__)
    logger.info(f"🚀 Начало теста: {request.node.name}")
    start_time = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    logger.info(
        f"🏁 Конец теста: {request.node.name}\n⏳ Время выполнения теста: {minutes:02d}:{seconds:02d}"
    )


@pytest.fixture(scope="session", autouse=True)
def log_test_total_time():
    """Логгирует общее время выполнения всех тестов."""

    start_time = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    logger.info(f"⏳ Общее время выполнения всех тестов: {minutes:02d}:{seconds:02d}")


@pytest.fixture(scope="session")
def browser_name() -> str:
    """Выбрать браузер по умолчанию."""

    return "chromium"


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict[str, object],
    request: pytest.FixtureRequest,
) -> dict[str, object]:
    """Запустить браузер в headless, если явно не передан --headed."""

    headed = request.config.getoption("--headed", default=False)
    return {
        **browser_type_launch_args,
        "headless": not headed,
    }


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict[str, object],
) -> dict[str, object]:
    """Переопределяет параметры браузерного контекста для всех тестов.

    Устанавливает:
        - Локаль: ru-RU
        - Часовой пояс: Europe/Moscow
        - Размер окна: 1440x900
    """

    return {
        **browser_context_args,
        "locale": "ru-RU",
        "timezone_id": "Europe/Moscow",
        "viewport": {"width": 1440, "height": 900},
    }
