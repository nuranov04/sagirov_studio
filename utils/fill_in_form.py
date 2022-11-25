from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config

import time
import os
import datetime


class Form:
    def __init__(self, user_id, name, surname, email, phone_number, date, executable_path):

        self.__options = webdriver.ChromeOptions()
        self.__driver = webdriver.Chrome(
            executable_path=executable_path,
            options=self.__options
        )
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.email = email
        self.phone_number = phone_number
        self.date = date

    def get_window(self, url: str):
        return self.__driver.get(url)

    def _find_element(self, by, value: str):
        return self.__driver.find_element(by, value)

    def find_element_by_name(self, value):
        return self._find_element(by=By.NAME, value=value)

    def find_element_by_xpath(self, value):
        return self._find_element(by=By.XPATH, value=value)

    def find_element_by_class_name(self, value):
        return self._find_element(by=By.CLASS_NAME, value=value)

    @staticmethod
    def __send_key(element, key):
        return element.send_keys(key)

    def send_name(self, element):
        self.__send_key(element, self.name)

    def send_surname(self, element):
        self.__send_key(element, self.surname)

    def send_email(self, element):
        self.__send_key(element, self.email)

    def send_phone_number(self, element):
        self.__send_key(element, self.phone_number)

    def send_date(self, element):
        self.__send_key(element, self.date)

    @staticmethod
    def clear_input(element):
        element.clear()

    def delete_script(self, script, element):
        self.__driver.execute_script(script, element)

    def save_screenshot(self, path):
        self.__driver.save_screenshot(path)

    def quite(self):
        self.__driver.quit()

    def close(self):
        self.__driver.close()


def main(name, surname, user_id, email, phone_number, date):
    executable_path = os.path.abspath("chromdriver/chromedriver")
    form = Form(user_id=user_id, name=name, surname=surname, email=email, phone_number=phone_number, date=date,
                executable_path=executable_path)

    try:
        form.get_window(config("URL"))
        time.sleep(3)

        # получение полей имя и фамилия
        name_input = form.find_element_by_name("name")
        print('asd')
        surname_input = form.find_element_by_name("lastname")

        time.sleep(1)
        # Очистить поля на всякий случай
        form.clear_input(name_input)
        form.clear_input(surname_input)

        # Отправка ключей
        form.send_name(name_input)
        time.sleep(1)
        form.send_surname(surname_input)

        time.sleep(1)

        continue_btn = form.find_element_by_class_name("b24-form-btn-block")

        time.sleep(1)

        continue_btn.click()

        time.sleep(2)

        email_input = form.find_element_by_name('email')
        phone_input = form.find_element_by_name("phone")

        form.clear_input(email_input)
        form.clear_input(phone_input)

        time.sleep(1)

        form.send_email(email_input)
        time.sleep(1)
        form.send_phone_number(phone_input)

        next_btn = form.find_element_by_xpath(
            "/html/body/main/div/section/div/div/div/div/div/div/div/div/div[2]/form/div[3]/div[2]/button")

        next_btn.click()
        time.sleep(1)

        calendar = form.find_element_by_class_name("b24-form-control")
        script = "arguments[0].removeAttribute('readonly','readonly')"
        form.delete_script(script=script, element=calendar)

        calendar.clear()
        time.sleep(1)

        calendar.send_keys(date)

        send_btn_xpath = "/html/body/main/div/section/div/div/div/div/div/div/div/div/div[2]/form/div[4]/div[2]/button"
        send_btn = form.find_element_by_xpath(send_btn_xpath)
        time.sleep(1)

        send_btn.click()

        time.sleep(3)

        path = f"{os.path.abspath('screenshots')}/{datetime.datetime.now().strftime('%Y-%m-%d__%H')}:mm__{user_id}.png"

        form.save_screenshot(path)

        return path

    except Exception as ex:
        print(ex)
        return ex
    finally:
        form.close()
        form.quite()


# if __name__ == "__main__":
#     main(name="Artur", surname='Nuranov', email="adsa@gmail.com", phone_number="+996 (778) 919-715",
#          date="29.10.2004", user_id="14")
