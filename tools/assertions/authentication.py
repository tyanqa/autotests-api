import allure  # Импортируем allure

from clients.authentication.authentication_schema import LoginResponseSchema
from tools.assertions.base import assert_equal, assert_is_true
from tools.logger import get_logger  # Импортируем функцию для создания логгера

logger = get_logger("AUTHENTICATION_ASSERTIONS")  # Создаем логгер с именем "AUTHENTICATION_ASSERTIONS"


@allure.step("Check login response")  # Добавили allure шаг
def assert_login_response(response: LoginResponseSchema):
    """
    Проверяет корректность ответа при успешной авторизации.

    :param response: Объект ответа с токенами авторизации.
    :raises AssertionError: Если какое-либо из условий не выполняется.
    """
    # Логируем факт начала проверки
    logger.info("Check login response")

    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")
