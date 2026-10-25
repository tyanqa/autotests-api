import platform
import sys

from config import settings


def create_allure_environment_file():
    # Создаем список из элементов в формате {key}={value}
    items = [f'{key}={value}' for key, value in settings.model_dump().items()]
    # Добавляем информацию об операционной системе и версии интерпретатора Python
    items.append(f'os_info={platform.system()}, {platform.release()}')
    items.append(f'python_version={sys.version}')
    # Собираем все элементы в единую строку с переносами
    properties = '\n'.join(items)

    # Создаем папку allure-results, если её ещё нет
    settings.allure_results_dir.mkdir(exist_ok=True)

    # Открываем файл ./allure-results/environment.properties на чтение
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)  # Записываем переменные в файл
