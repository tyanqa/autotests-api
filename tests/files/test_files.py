from http import HTTPStatus

import allure  # Импортируем allure
import pytest
from allure_commons.types import Severity  # Импортируем enum Severity из Allure

from clients.errors_schema import ValidationErrorResponseSchema, InternalErrorResponseSchema
from clients.files.files_client import FilesClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, GetFileResponseSchema
from fixtures.files import FileFixture
from tools.allure.epics import AllureEpic  # Импортируем enum AllureEpic
from tools.allure.features import AllureFeature  # Импортируем enum AllureFeature
from tools.allure.stories import AllureStory  # Импортируем enum AllureStory
from tools.allure.tags import AllureTag  # Импортируем enum с тегами
from tools.assertions.base import assert_status_code
from tools.assertions.files import assert_create_file_response, assert_create_file_with_empty_filename_response, \
    assert_create_file_with_empty_directory_response, assert_file_not_found_response, \
    assert_get_file_with_incorrect_file_id_response, assert_get_file_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.files
@pytest.mark.regression
@allure.tag(AllureTag.FILES, AllureTag.REGRESSION)  # Добавили теги
@allure.epic(AllureEpic.LMS)  # Добавили epic
@allure.feature(AllureFeature.FILES)  # Добавили feature
@allure.parent_suite(AllureEpic.LMS)  # allure.parent_suite == allure.epic
@allure.suite(AllureFeature.FILES)  # allure.suite == allure.feature
class TestFiles:
    @allure.tag(AllureTag.CREATE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.CREATE_ENTITY)  # Добавили story
    @allure.title("Create file")  # Добавили заголовок
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    @allure.sub_suite(AllureStory.CREATE_ENTITY)  # allure.sub_suite == allure.story
    def test_create_file(self, files_client: FilesClient):
        request = CreateFileRequestSchema(upload_file="./testdata/files/image.png")
        response = files_client.create_file_api(request)
        response_data = CreateFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_file_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)  # Добавили тег
    @allure.story(AllureStory.GET_ENTITY)  # Добавили story
    @allure.title("Get file")  # Добавили заголовок
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    @allure.sub_suite(AllureStory.GET_ENTITY)  # allure.sub_suite == allure.story
    def test_get_file(self, files_client: FilesClient, function_file: FileFixture):
        response = files_client.get_file_api(function_file.response.file.id)
        response_data = GetFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_file_response(response_data, function_file.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.VALIDATE_ENTITY)  # Добавили story
    @allure.title("Create file with empty filename")  # Добавили заголовок
    @allure.severity(Severity.NORMAL)  # Добавили severity
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)  # allure.sub_suite == allure.story
    def test_create_file_with_empty_filename(self, files_client: FilesClient):
        request = CreateFileRequestSchema(
            filename="",
            upload_file="./testdata/files/image.png"
        )
        response = files_client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        
        # Проверка, что код ответа соответствует ожиданиям (422 - Unprocessable Entity)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # Проверка, что ответ API соответствует ожидаемой валидационной ошибке
        assert_create_file_with_empty_filename_response(response_data)
        
        # Дополнительная проверка структуры JSON, чтобы убедиться, что схема валидационного ответа не изменилась
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.VALIDATE_ENTITY)  # Добавили story
    @allure.title("Create file with empty directory")  # Добавили заголовок
    @allure.severity(Severity.NORMAL)  # Добавили severity
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)  # allure.sub_suite == allure.story
    def test_create_file_with_empty_directory(self, files_client: FilesClient):
        request = CreateFileRequestSchema(
            directory="",
            upload_file="./testdata/files/image.png"
        )
        response = files_client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        
        # Проверка, что код ответа соответствует ожиданиям (422 - Unprocessable Entity)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # Проверка, что ответ API соответствует ожидаемой валидационной ошибке
        assert_create_file_with_empty_directory_response(response_data)
        
        # Дополнительная проверка структуры JSON
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.VALIDATE_ENTITY)  # Добавили story
    @allure.title("Get file with incorrect file id")  # Добавили заголовок
    @allure.severity(Severity.NORMAL)  # Добавили severity
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)  # allure.sub_suite == allure.story
    def test_get_file_with_incorrect_file_id(self, files_client: FilesClient):
        # Передаем заведомо некорректный идентификатор файла (не UUID)
        response = files_client.get_file_api("incorrect-file-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        # Проверка, что код ответа соответствует ожиданиям (422 - Unprocessable Entity)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # Проверка, что ответ API соответствует ожидаемой валидационной ошибке
        assert_get_file_with_incorrect_file_id_response(response_data)

        # Дополнительная проверка структуры JSON
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)  # Добавили тег
    @allure.story(AllureStory.DELETE_ENTITY)  # Добавили story
    @allure.title("Delete file")  # Добавили заголовок
    @allure.severity(Severity.NORMAL)  # Добавили severity
    @allure.sub_suite(AllureStory.DELETE_ENTITY)  # allure.sub_suite == allure.story
    def test_delete_file(self, files_client: FilesClient, function_file: FileFixture):
        # 1. Удаляем файл
        delete_response = files_client.delete_file_api(function_file.response.file.id)
        # 2. Проверяем, что файл успешно удален (статус 200 OK)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        
        # 3. Пытаемся получить удаленный файл
        get_response = files_client.get_file_api(function_file.response.file.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        
        # 4. Проверяем, что сервер вернул 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        # 5. Проверяем, что в ответе содержится ошибка "File not found"
        assert_file_not_found_response(get_response_data)
        
        # 6. Проверяем, что ответ соответствует схеме
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

        
                    