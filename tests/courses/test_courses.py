from http import HTTPStatus

import allure  # Импортируем allure
import pytest
from allure_commons.types import Severity  # Импортируем enum Severity из Allure

from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import UpdateCourseRequestSchema, UpdateCourseResponseSchema, GetCoursesQuerySchema, \
    GetCoursesResponseSchema, CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic  # Импортируем enum AllureEpic
from tools.allure.features import AllureFeature  # Импортируем enum AllureFeature
from tools.allure.stories import AllureStory  # Импортируем enum AllureStory
from tools.allure.tags import AllureTag  # Импортируем enum с тегами
from tools.assertions.base import assert_status_code
from tools.assertions.courses import assert_update_course_response, assert_get_courses_response, \
    assert_create_course_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTag.COURSES, AllureTag.REGRESSION)  # Добавили теги
@allure.epic(AllureEpic.LMS)  # Добавили epic
@allure.feature(AllureFeature.COURSES)  # Добавили feature
@allure.parent_suite(AllureEpic.LMS)  # allure.parent_suite == allure.epic
@allure.suite(AllureFeature.COURSES)  # allure.suite == allure.feature
class TestCourses:
    @allure.tag(AllureTag.CREATE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.CREATE_ENTITY)  # Добавили story
    @allure.title("Create course")  # Добавили заголовок
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    @allure.sub_suite(AllureStory.CREATE_ENTITY)  # allure.sub_suite == allure.story
    def test_create_course(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # Формируем запрос, передавая идентификаторы файла-превью и пользователя из фикстур
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )
        # Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # Преобразуем JSON-ответ в объект схемы
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.UPDATE_ENTITY)  # Добавили story
    @allure.title("Update course")  # Добавили заголовок
    @allure.severity(Severity.CRITICAL)  # Добавили severity
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)  # allure.sub_suite == allure.story
    def test_update_course(self, courses_client: CoursesClient, function_course: CourseFixture):
        # Формируем данные для обновления
        request = UpdateCourseRequestSchema()
        # Отправляем запрос на обновление курса
        response = courses_client.update_course_api(function_course.response.course.id, request)
        # Преобразуем JSON-ответ в объект схемы
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        
        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_update_course_response(request, response_data)
        
        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())
        
    @allure.tag(AllureTag.GET_ENTITIES)  # Добавили тег
    @allure.story(AllureStory.GET_ENTITIES)  # Добавили story
    @allure.title("Get courses")  # Добавили заголовок
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    @allure.sub_suite(AllureStory.GET_ENTITIES)  # allure.sub_suite == allure.story
    def test_get_courses(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_course: CourseFixture
    ):
        # Формируем параметры запроса, передавая user_id
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)
        # Отправляем GET-запрос на получение списка курсов
        response = courses_client.get_courses_api(query)
        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)
        
        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что список курсов соответствует ранее созданным курсам
        assert_get_courses_response(response_data, [function_course.response])
        
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())