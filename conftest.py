import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from configuration import AUTH_TOKEN, BASE_URL_UI


@pytest.fixture(scope="function")
def browser():
    with allure.step("Запуск браузера Chrome"):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.maximize_window()
        driver.implicitly_wait(10)

    yield driver

    with allure.step("Закрытие браузера"):
        driver.quit()


@pytest.fixture(scope="function")
def auth_browser(browser):

    with allure.step("Авторизация в системе через Cookies"):
        browser.get(BASE_URL_UI)

        browser.add_cookie({
            "api_token": (
                "f8a6b96dff5251a0a368dde8ca0a0337372e3232322e39372e313537302e"
                "34323037323230302031373633343730323434"
            ),
            "value": AUTH_TOKEN,
            "domain": ".mts.ru"
        })

        browser.refresh()

    return browser
