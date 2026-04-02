import pytest
import requests
import allure
from configuration import (
    BASE_URL_API, BASE_URL_API_GW, ENDPOINTS,
    AUTH_TOKEN, SEARCH_PARAMS, PRODUCT_VALID,
    PRODUCT_INVALID_ID, PRODUCT_ZERO_QTY
)


@pytest.mark.api
@allure.epic("API Тесты MTS Shop")
class TestMtsApi:

    @allure.feature("Корзина")
    @allure.title("Кейс 1: Запрос содержимого корзины (GET)")
    def test_get_cart_content(self):
        url = f"{BASE_URL_API.rstrip('/')}/{ENDPOINTS['cart'].lstrip('/')}"

        print(f"\nFINAL URL: {url}")

        headers = {
            "Cookie": f"token={AUTH_TOKEN}",
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                           "AppleWebKit/537.36 (KHTML, like Gecko)"
                           "Chrome/120.0.0.0 Safari/537.36")
        }

        with allure.step(f"Отправить GET запрос на {url}"):
            response = requests.get(url, headers=headers)

        if response.status_code == 404:
            allure.attach(response.text, name="Error 404 Page Content")

        with allure.step("Проверить статус 200"):
            assert response.status_code == 200

    @allure.feature("Поиск")
    @allure.title("Кейс 2: Поиск товара через API (GET)")
    def test_get_search_results(self):
        url = (
            f"{BASE_URL_API_GW.rstrip('/')}/"
            f"{ENDPOINTS['search'].lstrip('/')}"
        )
        with allure.step(f"Отправить GET запрос на {url}"):
            response = requests.get(url, params=SEARCH_PARAMS)

        with allure.step("Проверить статус 200 и структуру ответа"):
            assert response.status_code == 200
            data = response.json()

            allure.attach(str(list(data.keys())), name="JSON Keys")

            success_data = data.get("success_response")
            assert success_data is not None, (
                f"Бэкенд вернул ошибку: {data.get('error_backend')}"
            )
            assert ("hits" in success_data or "categories" in success_data), \
                "В ответе нет результатов поиска"

    @allure.feature("Корзина")
    @allure.title("Кейс 3: Добавление товара в корзину по ID (POST)")
    @pytest.mark.api
    def test_post_add_to_cart_valid(self):
        url = f"{BASE_URL_API.rstrip('/')}/{ENDPOINTS['cart_add'].lstrip('/')}"

        headers = {
            "Cookie": f"token={AUTH_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }

        with allure.step(f"POST запрос на {url}"):
            response = requests.post(url, headers=headers, json=PRODUCT_VALID)

        with allure.step("Проверить успешный статус"):
            assert response.status_code in [200, 201], (
                f"Ошибка: {response.status_code}, {response.text}"
            )
            data = response.json()
            assert data.get("success") is True or "items" in str(data)

    @allure.feature("Корзина")
    @allure.title("Кейс 4: Ошибка при некорректном ID товара (POST)")
    def test_post_add_invalid_id(self):
        url = f"{BASE_URL_API}{ENDPOINTS['cart_add']}"
        headers = {"Cookie": AUTH_TOKEN, "Content-Type": "application/json"}

        with allure.step("Отправить POST с текстовым ID 'iphone'"):
            response = requests.post(
                url,
                headers=headers,
                json=PRODUCT_INVALID_ID
            )

        with allure.step("Проверить статус 400 Bad Request"):
            assert response.status_code == 400

    @allure.feature("Корзина")
    @allure.title("Кейс 5: Ошибка при нулевом количестве товара (POST)")
    def test_post_add_zero_quantity(self):
        url = f"{BASE_URL_API}{ENDPOINTS['cart_add']}"
        headers = {"Cookie": AUTH_TOKEN, "Content-Type": "application/json"}

        with allure.step("Попытка добавить 0 штук товара"):
            response = requests.post(
                url,
                headers=headers,
                json=PRODUCT_ZERO_QTY
            )

        with allure.step("Проверить статус 400 Bad Request"):
            assert response.status_code == 400
