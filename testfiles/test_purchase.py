from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Данные для теста
LOGIN_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
PRODUCT_NAME = "Sauce Labs Backpack"
FIRST_NAME = "John"
LAST_NAME = "Doe"
POSTAL_CODE = "12345"


def test_purchase():
    # Настройка WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Открываем страницу логина
        driver.get(LOGIN_URL)
        driver.maximize_window()

        # Логинимся на сайте
        driver.find_element(By.ID, "user-name").send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Ждем загрузки страницы

        # Выбираем продукт и добавляем его в корзину
        driver.find_element(By.XPATH, f"//div[text()='{PRODUCT_NAME}']").click()
        time.sleep(1)
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

        # Переходим в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)
        # Проверяем, что продукт добавлен в корзину
        assert driver.find_element(By.CLASS_NAME,
                                   "inventory_item_name").text == PRODUCT_NAME, "Продукт не добавлен в корзину!"
        time.sleep(2)
        # Нажимаем кнопку Checkout для оформления заказа
        driver.find_element(By.ID, "checkout").click()
        time.sleep(2)
        # Вводим данные для оформления заказа
        driver.find_element(By.ID, "first-name").send_keys(FIRST_NAME)
        driver.find_element(By.ID, "last-name").send_keys(LAST_NAME)
        driver.find_element(By.ID, "postal-code").send_keys(POSTAL_CODE)
        driver.find_element(By.ID, "continue").click()

        # Подтверждаем заказ и завершаем покупку
        driver.find_element(By.ID, "finish").click()
        time.sleep(2)
        # Проверяем, что покупка завершена успешно
        success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert success_message == "THANK YOU FOR YOUR ORDER", "Ошибка при оформлении покупки!"
        time.sleep(2)
        print("Тест пройден: Покупка успешно завершена!")

    except Exception as e:
        print(f"Тест провален: {str(e)}")

    finally:
        # Закрываем браузер
        driver.quit()


if __name__ == "__main__":
    test_purchase()