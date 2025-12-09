import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pages.login_page import LoginPage
import os
from datetime import datetime


# ----- FIXTURE DRIVER -----
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--incognito")

    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()


# ----- LOGIN AUTOMÁTICO + CAPTURA SI FALLA -----
@pytest.fixture
def login_in_driver(driver, usuario, password):
    try:
        LoginPage(driver).abrir_pagina().login_completo(usuario, password)
        return driver
    except Exception:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/ERROR_login_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n📸 Captura guardada por error en login: {screenshot_path}")
        raise


# ----- CAPTURA EN CUALQUIER TEST QUE FALLE -----
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()

    # SOLO capturar fallos en la ejecución del test ("call")
    if rep.when == "call" and rep.failed:

        if "driver" in item.fixturenames:
            driver = item.funcargs.get("driver")

            if driver:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                testname = item.name

                os.makedirs("screenshots", exist_ok=True)
                path = f"screenshots/ERROR_{testname}_{timestamp}.png"

                driver.save_screenshot(path)
                print(f"\n📸 Captura guardada: {path}")


# ----- FIXTURES API -----
@pytest.fixture
def url_base():
    return "https://reqres.in/api/users"

"""@pytest.fixture
def header_request():
    return {"x-api-key": "YOUR_API_KEY"}
              
"""
@pytest.fixture
def header_request():
    return {}
