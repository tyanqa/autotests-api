from pydantic import BaseModel, Field, ConfigDict

from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema
# Импортируем заранее созданный экземпляр класса Fake
from tools.fakers import fake


class CourseSchema(BaseModel):
    """
    Описание структуры курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    description: str
    preview_file: FileSchema = Field(alias="previewFile")  # Вложенная структура файла
    estimated_time: str = Field(alias="estimatedTime")
    created_by_user: UserSchema = Field(alias="createdByUser")  # Вложенная структура пользователя


class GetCoursesQuerySchema(BaseModel):
    """
    Описание структуры query параметров для получения списка курсов.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")


class GetCoursesResponseSchema(BaseModel):
    """
    Описание структуры ответа получения списка курсов.
    """
    courses: list[CourseSchema]


class GetCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа получения курса.
    """
    course: CourseSchema


class CreateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    # Добавили генерацию случайного заголовка
    title: str = Field(default_factory=fake.sentence)
    # Добавили генерацию случайного максимального балла
    max_score: int = Field(alias="maxScore", default_factory=fake.max_score)
    # Добавили генерацию случайного минимального балла
    min_score: int = Field(alias="minScore", default_factory=fake.min_score)
    # Добавили генерацию случайного описания
    description: str = Field(default_factory=fake.text)
    # Добавили генерацию случайного предполагаемого времени прохождения курса
    estimated_time: str = Field(alias="estimatedTime", default_factory=fake.estimated_time)
    # Добавили генерацию случайного идентификатора файла
    preview_file_id: str = Field(alias="previewFileId", default_factory=fake.uuid4)
    # Добавили генерацию случайного идентификатора пользователя
    created_by_user_id: str = Field(alias="createdByUserId", default_factory=fake.uuid4)


class CreateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания курса.
    """
    course: CourseSchema


class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    # Добавили генерацию случайного заголовка
    title: str | None = Field(default_factory=fake.sentence)
    # Добавили генерацию случайного максимального балла
    max_score: int | None = Field(alias="maxScore", default_factory=fake.max_score)
    # Добавили генерацию случайного минимального балла
    min_score: int | None = Field(alias="minScore", default_factory=fake.min_score)
    # Добавили генерацию случайного описания
    description: str | None = Field(default_factory=fake.text)
    # Добавили генерацию случайного предполагаемого времени прохождения курса
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=fake.estimated_time)


class UpdateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления курса.
    """
    course: CourseSchema
