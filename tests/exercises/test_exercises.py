from http import HTTPStatus

import allure  # Импортируем allure
import pytest
from allure_commons.types import Severity  # Импортируем enum Severity из Allure

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesQuerySchema, \
    GetExercisesResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.allure.epics import AllureEpic  # Импортируем enum AllureEpic
from tools.allure.features import AllureFeature  # Импортируем enum AllureFeature
from tools.allure.stories import AllureStory  # Импортируем enum AllureStory
from tools.allure.tags import AllureTag  # Импортируем enum с тегами
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION)  # Добавили теги
@allure.epic(AllureEpic.LMS)  # Добавили epic
@allure.feature(AllureFeature.EXERCISES)  # Добавили feature
@allure.parent_suite(AllureEpic.LMS)  # allure.parent_suite == allure.epic
@allure.suite(AllureFeature.EXERCISES)  # allure.suite == allure.feature
class TestExercises:
    @allure.tag(AllureTag.CREATE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.CREATE_ENTITY)  # Добавили story
    @allure.title("Create exercise")  # Добавили заголовок
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    @allure.sub_suite(AllureStory.CREATE_ENTITY)  # allure.sub_suite == allure.story
    def test_create_exercise(self, exercises_client: ExercisesClient, function_course: CourseFixture):
        # Формируем запрос, передавая идентификатор курса из фикстуры
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        # Отправляем POST-запрос на создание задания
        response = exercises_client.create_exercise_api(request)
        # Преобразуем JSON-ответ в объект схемы
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_exercise_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)  # Добавили тег
    @allure.story(AllureStory.GET_ENTITY)  # Добавили story
    @allure.title("Get exercise")  # Добавили заголовок
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    @allure.sub_suite(AllureStory.GET_ENTITY)  # allure.sub_suite == allure.story
    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        # Отправляем GET-запрос на получение задания по его идентификатору
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        # Преобразуем JSON-ответ в объект схемы
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные задания соответствуют ответу на его создание
        assert_get_exercise_response(response_data, function_exercise.response)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.UPDATE_ENTITY)  # Добавили story
    @allure.title("Update exercise")  # Добавили заголовок
    @allure.severity(Severity.CRITICAL)  # Добавили severity
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)  # allure.sub_suite == allure.story
    def test_update_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        # Формируем данные для обновления задания (все значения генерируются автоматически)
        request = UpdateExerciseRequestSchema()
        # Отправляем PATCH-запрос на обновление задания
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id, request)
        # Преобразуем JSON-ответ в объект схемы
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу на обновление
        assert_update_exercise_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.DELETE_ENTITY)  # Добавили story
    @allure.title("Delete exercise")  # Добавили заголовок
    @allure.severity(Severity.CRITICAL)  # Добавили severity
    @allure.sub_suite(AllureStory.DELETE_ENTITY)  # allure.sub_suite == allure.story
    def test_delete_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        # Удаляем задание, созданное фикстурой
        delete_response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)

        # Проверяем статус-код ответа на удаление
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # Пытаемся получить удаленное задание
        get_response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # Проверяем, что сервер вернул 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        # Проверяем, что в ответе содержится ошибка "Exercise not found"
        assert_exercise_not_found_response(response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(get_response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)  # Добавили тег
    @allure.story(AllureStory.GET_ENTITIES)  # Добавили story
    @allure.title("Get exercises")  # Добавили заголовок
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    @allure.sub_suite(AllureStory.GET_ENTITIES)  # allure.sub_suite == allure.story
    def test_get_exercises(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture,
            function_exercise: ExerciseFixture
    ):
        # Формируем параметры запроса, передавая course_id для фильтрации списка заданий
        query = GetExercisesQuerySchema(course_id=function_course.response.course.id)
        # Отправляем GET-запрос на получение списка заданий
        response = exercises_client.get_exercises_api(query)
        # Преобразуем JSON-ответ в объект схемы
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что список заданий соответствует ранее созданному заданию
        assert_get_exercises_response(response_data, [function_exercise.response])

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())
