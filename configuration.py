# ОБЩИЕ НАСТРОЙКИ ОКРУЖЕНИЯ (URL)
BASE_URL_UI = "https://shop.mts.ru/catalog/smartfony/"
BASE_URL_API = "https://shop.mts.ru/api/v1"
BASE_URL_API_GW = "https://shop.mts.ru/apigw/api/v1"
URL_IPHONE = (
    "https://shop.mts.ru"
    "/product/smartfon-apple-iphone-17-pro-256-gb-esim-sim-cosmic-orange"
)
AUTH_TOKEN = (
    "f8a6b96dff5251a0a368dde8ca0a0337372e3232322e39372e313537302e34323037"
    "323230302031373633343730323434"
)
CART_URL = "https://shop.mts.ru/personal/basket"
SORTED_URL = (
    "https://shop.mts.ru/catalog/smartfony/"
    "?order=PRICE_ASC"
)

# ДАННЫЕ ДЛЯ API-ТЕСТОВ (test_api.py)
ENDPOINTS = dict(
    cart="/baskets/current?corporate=false",
    cart_add="/cart/add",
    search="/search/hits"
)

SEARCH_PARAMS = {
    "st": "Чехлы",
    "project": "shop",
    "platform": "web",
    "strategy": "advanced_xname,zero_queries",
    "regionId": "77000000000000000000000000",
    "showUnavailable": "true",
    "location": "77000000000000000000000000"
}

PRODUCT_VALID = {"id": "823044", "quantity": 1, "discount": 0}
PRODUCT_INVALID_ID = {
    "id": "iphone",
    "quantity": 1,
    "discount": 0
}
PRODUCT_ZERO_QTY = {"id": "947754", "quantity": 0, "discount": 0}

# ЛОКАТОРЫ И ДАННЫЕ ДЛЯ UI-ТЕСТОВ (test_ui.py)
UI_LOCATORS = {
    "product_card": ".product-card",
    "product_title_in_card": ".product-card__name-link",
    "product_page_header": "h1",
    "search_input": (
        "input[type='search'], input[placeholder*='Поиск'], "
        ".mtsds-search-input__field"
    ),
    "search_result_item": ".product-card",
    "search_query_text": "Чехлы",
    "add_to_cart_btn": (
        "//button[contains(., 'Купить') or contains(., 'корзину') "
        "or contains(@class, 'buy-button')]"
    ),
    "buy_button_text": "span.button__text",
    "cart_counter": ".mdsx-counter-button__quantity",
    "cart_url": "https://shop.mts.ru/personal/basket",
    "phones_catalog_url": "https://shop.mts.ru/catalog/smartfony/",
    "sort_dropdown": ".catalog-sorting",
    "product_price": "[class*='product-price__current']"
}
