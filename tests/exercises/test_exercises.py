from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema
)
from fixtures.courses import CourseFixture
from clients.errors_schema import InternalErrorResponseSchema
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_exercise_not_found_response,
    assert_get_exercise_response,
    assert_update_exercise_response
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
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

    def test_get_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
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

    def test_update_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
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

    def test_delete_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
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
