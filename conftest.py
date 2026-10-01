pytest_plugins = (
    "fixtures.users",
    "fixtures.files",
    "fixtures.courses",  # Добавляем фикстуры для работы с курсами
    "fixtures.exercises",  # Добавляем фикстуры для работы с заданиями
    "fixtures.authentication"
)