import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuration import (
    BASE_URL_UI, UI_LOCATORS,
    CART_URL, SORTED_URL
)


@pytest.mark.ui
@allure.epic("UI Тесты MTS Shop")
class TestMtsUi:

    @allure.feature("Карточка товара")
    @allure.title("Кейс 1: Открытие карточки товара по клику")
    def test_open_product_card(self, browser):
        wait = WebDriverWait(browser, 5)
        with allure.step(f"Открыть страницу каталога {BASE_URL_UI}"):
            browser.get(BASE_URL_UI)

        with allure.step("Найти название товара и кликнуть по нему"):
            title_element = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, UI_LOCATORS["product_title_in_card"])
            ))
            expected_name = title_element.text.strip()

            browser.execute_script("arguments[0].click();", title_element)

        with allure.step("Проверить заголовок на открывшейся странице"):
            header = wait.until(EC.visibility_of_element_located(
                (By.TAG_NAME, UI_LOCATORS["product_page_header"])
            ))
            assert expected_name.lower() in header.text.lower()

    @allure.feature("Поиск")
    @allure.title("Кейс 2: Работа поисковой строки")
    @pytest.mark.ui
    def test_search_functional(self, browser):
        from selenium.webdriver.common.keys import Keys
        wait = WebDriverWait(browser, 5)

        with allure.step("Открыть страницу"):
            browser.get(BASE_URL_UI)
            time.sleep(5)
            browser.execute_script(
                "document.querySelectorAll"
                "('.mtsds-v2-modal, [class*=\"region\"]')"
                ".forEach(el => el.remove());"
            )

        with allure.step("Ввести запрос в поиск"):
            search_input = wait.until(
                EC.presence_of_element_located
                ((By.CSS_SELECTOR, UI_LOCATORS["search_input"]))
            )

            browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                search_input
            )
            time.sleep(1)

            browser.execute_script("arguments[0].click();", search_input)
            search_input.clear()

            search_input.send_keys(UI_LOCATORS["search_query_text"])
            time.sleep(1)
            search_input.send_keys(Keys.ENTER)

        with allure.step("Проверить наличие результатов поиска"):
            time.sleep(5)
            results = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".product-card, [class*='ProductCard']")
            ))

            allure.attach(
                browser.get_screenshot_as_png(),
                name="search_results",
                attachment_type=allure.attachment_type.PNG
            )
            assert len(results) > 0, "Результаты поиска не найдены"

    @allure.feature("Корзина")
    @allure.title("Кейс 3: Проверка добавления товара в корзину")
    def test_cart_add_verification(self, browser):
        wait = WebDriverWait(browser, 5)

        with allure.step("Открыть карточку iPhone 17 Pro"):
            from configuration import URL_IPHONE
            browser.get(URL_IPHONE)
            time.sleep(5)

        with allure.step("Нажать кнопку 'Купить'"):
            buy_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".buy-button"))
            )
            browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                buy_btn
            )
            time.sleep(2)
            browser.execute_script("arguments[0].click();", buy_btn)
            time.sleep(3)

        with allure.step("Перейти в корзину и проверить наличие товара"):
            browser.get(CART_URL)
            time.sleep(5)

            item_selectors = (
                ".cart-item, [class*='Card'], [class*='Product'], "
                ".basket-item, a[href*='/product/']"
            )

            wait.until(
                EC.presence_of_element_located
                ((By.CSS_SELECTOR, item_selectors))
            )

            items = browser.find_elements(By.CSS_SELECTOR, item_selectors)

            allure.attach(
                browser.get_screenshot_as_png(),
                name="cart_final_look",
                attachment_type=allure.attachment_type.PNG
            )

            assert len(items) > 0, (
                "Корзина пуста, товары не найдены в коде страницы"
            )

    @allure.story("Сортировка товаров")
    @allure.title("Кейс 4: Работа сортировки по цене (сначала дешевые)")
    @pytest.mark.ui
    def test_sorting_by_price(self, browser):
        wait = WebDriverWait(browser, 5)

        with allure.step(
                "Открыть каталог смартфонов с сортировкой 'Сначала дешевые'"
        ):
            browser.get(SORTED_URL)
            browser.get(SORTED_URL)
            time.sleep(7)

        with allure.step("Удалить всплывающие окна (регион, куки)"):
            js_script = (
                "let overlays = document.querySelectorAll('.mtsds-v2-modal, "
                "[class*=\"region\"], .cookie-banner');"
                "overlays.forEach(el => el.remove());"
            )
            browser.execute_script(js_script)

        with allure.step("Собрать цены первых товаров из карточек"):
            try:
                cards = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".product-card, [class*='ProductCard']")
                ))
            except Exception:
                cards = browser.find_elements(
                    By.XPATH, "//div[contains(@class, 'product')]"
                )

            prices = []
            for card in cards[:5]:
                try:
                    price_element = card.find_element(
                        By.CSS_SELECTOR, "[class*='price-current'],"
                                         "[class*='price']"
                    )
                    price_text = price_element.text

                    clean_price = "".join(filter(lambda x: x.isdigit(), price_text))
                    if clean_price:
                        prices.append(int(clean_price))
                except Exception:
                    continue

        with allure.step(
            f"Проверка: цены {prices} должны идти по возрастанию"
        ):
            assert len(prices) >= 2, (
                f"Не удалось собрать достаточно цен для проверки."
                f"Найдено: {len(prices)}"
            )

            assert prices == sorted(prices), (
                f"Сортировка не сработала! Ожидалось {sorted(prices)}, "
                f"но получили {prices}"
            )

        allure.attach(
            browser.get_screenshot_as_png(),
            name="final_result",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.feature("Корзина")
    @allure.title("Кейс 5: Отображение списка товаров в корзине")
    @pytest.mark.ui
    def test_cart_items_display(self, browser):
        wait = WebDriverWait(browser, 5)

        with allure.step("Открыть каталог и подготовить страницу"):
            browser.get(BASE_URL_UI)
            wait.until(
                EC.presence_of_element_located
                ((By.CSS_SELECTOR, ".product-card"))
            )
            browser.execute_script(
                    "document.querySelectorAll"
                    "('.mtsds-v2-modal, [class*=\"region\"]')"
                    ".forEach(el => el.remove());"
                )
            time.sleep(2)

        with allure.step("Найти товар и добавить в корзину"):
            title_el = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, UI_LOCATORS["product_title_in_card"])
                )
            )

            name = title_el.text.strip()

            buy_btn = wait.until(
                EC.element_to_be_clickable
                ((By.XPATH, UI_LOCATORS["add_to_cart_btn"]))
            )

            browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                buy_btn
            )
            time.sleep(1)
            browser.execute_script("arguments[0].click();", buy_btn)

            time.sleep(3)

        with allure.step("Перейти в корзину"):
            browser.get(CART_URL)
            time.sleep(5)

        with allure.step("Проверить название товара в корзине"):
            item_in_cart = wait.until(EC.visibility_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{name[:10]}')]")
            ))

            assert name[:10].lower() in item_in_cart.text.lower(), (
                f"Товар {name} не найден в корзине"
            )
