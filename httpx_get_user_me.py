import httpx  # Импортируем библиотеку HTTPX

# Данные для входа в систему
login_payload = {
    "email": "user12@example.com",
    "password": "password12"
}

# Выполняем запрос на аутентификацию
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

# Извлекаем accessToken из ответа
access_token = login_response_data["token"]["accessToken"]

# Выполняем запрос на получение данных текущего пользователя
headers = {
    "Authorization": f"Bearer {access_token}"
}
get_user_me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=headers)
get_user_me_response_data = get_user_me_response.json()

# Выводим данные пользователя и статус код ответа
print("User data:", get_user_me_response_data)
print("Status Code:", get_user_me_response.status_code)
