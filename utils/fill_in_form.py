from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from decouple import config

import time
import os
import datetime


class Form:
    def __init__(self, user_id, name, surname, email, phone_number, date, executable_path):
        self.__options = webdriver.ChromeOptions()
        self.__options.headless = True
        self.__driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.__options)
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.email = email
        self.phone_number = phone_number
        self.date = date

    def get_window(self, url: str):
        """
        Отпрытие окна по url
        """
        return self.__driver.get(url)

    def _find_element(self, by, value: str):
        """
        Поиск элемента
        """
        return self.__driver.find_element(by, value)

    def find_element_by_name(self, value):
        """
        Поиск элемента по name
        """
        return self._find_element(by=By.NAME, value=value)

    def find_element_by_xpath(self, value):
        """
        Поиск элемента по xpath
        """
        return self._find_element(by=By.XPATH, value=value)

    def find_element_by_class_name(self, value):
        """
        Поиск элемента по class name
        """
        return self._find_element(by=By.CLASS_NAME, value=value)

    @staticmethod
    def __send_key(element, key):
        """
        Отправка ключа в input
        """
        return element.send_keys(key)

    def send_name(self, element):
        """
        Отправка имени в input
        """
        self.__send_key(element, self.name)

    def send_surname(self, element):
        """
        Отправка фамилии в input
        """
        self.__send_key(element, self.surname)

    def send_email(self, element):
        """
        Отправка почты в input
        """
        self.__send_key(element, self.email)

    def send_phone_number(self, element):
        """
        Отправка номера телефона в input
        """
        self.__send_key(element, self.phone_number)

    def send_date(self, element):
        """
        Отправка даты в input
        """
        self.__send_key(element, self.date)

    @staticmethod
    def clear_input(element):
        """
        Метод для очистки input'ов
        """
        element.clear()

    def delete_script(self, script, element):
        """
        Удаление аргумента с помощью скрипта из страницы
        """
        self.__driver.execute_script(script, element)

    def save_screenshot(self, path):
        """
        Создание скриншота
        """
        self.__driver.save_screenshot(path)

    def quite(self):
        """
        Выход из браузера
        """
        self.__driver.quit()

    def close(self):
        """
        закрытие вкладки
        """
        self.__driver.close()


def send_user_values(name, surname, user_id, email, phone_number, date):
    executable_path = os.path.abspath("chromdriver/chromedriver")
    form = Form(user_id=user_id, name=name, surname=surname, email=email, phone_number=phone_number, date=date,
                executable_path=executable_path)

    try:
        form.get_window(config("URL"))
        time.sleep(1.5)

        # получение полей имя и фамилия
        name_input = form.find_element_by_name("name")
        surname_input = form.find_element_by_name("lastname")

        time.sleep(0.8)
        # Очистить поля на всякий случай
        form.clear_input(name_input)
        form.clear_input(surname_input)

        # Отправка ключей
        form.send_name(name_input)
        time.sleep(0.8)
        form.send_surname(surname_input)

        time.sleep(0.8)

        # Поиск кнопки "Продолжить"
        continue_btn = form.find_element_by_class_name("b24-form-btn-block")

        time.sleep(0.8)

        # Эмуляция нажатия кнопки "Далее"
        continue_btn.click()

        time.sleep(1)

        # Поиск полей
        email_input = form.find_element_by_name('email')
        phone_input = form.find_element_by_name("phone")

        # Очистка этих полей (email, phone number)
        form.clear_input(email_input)
        form.clear_input(phone_input)

        time.sleep(0.8)

        # Отправка значений в поля email, phone number
        form.send_email(email_input)
        time.sleep(1)
        form.send_phone_number(phone_input)

        # Поиск кнопки "Далее"
        next_btn = form.find_element_by_xpath(
            "/html/body/main/div/section/div/div/div/div/div/div/div/div/div[2]/form/div[3]/div[2]/button")

        # Эмуляция нажатия кнопки "Далее"
        next_btn.click()
        time.sleep(1)

        # Поиск календаря
        calendar = form.find_element_by_class_name("b24-form-control")

        script = "arguments[0].removeAttribute('readonly','readonly')"
        # Удаление аргумента "readonly" из страницы
        form.delete_script(script=script, element=calendar)

        # Очистка input'а
        calendar.clear()
        time.sleep(0.8)

        calendar.send_keys(date)

        send_btn_xpath = "/html/body/main/div/section/div/div/div/div/div/div/div/div/div[2]/form/div[4]/div[2]/button"
        send_btn = form.find_element_by_xpath(send_btn_xpath)
        time.sleep(0.8)

        send_btn.click()
        time.sleep(5)

        path = f"{os.path.abspath('screenshots')}/{datetime.datetime.now().strftime('%Y-%m-%d__%H')}:mm__{user_id}.png"

        # сохранение скриншота
        form.save_screenshot(path)

        return path

    except Exception as ex:
        return ex
    finally:
        form.close()
        form.quite()
