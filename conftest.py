import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from selenium.webdriver.firefox.options import Options
import os
from datetime import datetime

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox") # github
    options.add_argument("--disable-gpu") # github
    options.add_argument("--window-size=1920,1080") # github
    options.add_argument("--headless=new") # github


    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def login_in_driver(driver, usuario, password):
    try:
        LoginPage(driver).abrir_pagina().login_completo(usuario, password)
        return driver
    except Exception as e:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"reports/screenshots/error_login_{timestamp}.png"
        
        os.makedirs("reports/screenshots", exist_ok=True)
        driver.save_screenshot(screenshot_path)
        print(f"\nCaptura guardada en: {screenshot_path}")
        raise e
    
# Hook que captura automáticamente en cualquier error
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.failed and "driver" in item.fixturenames:
        driver = item.funcargs.get("driver")
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"reports/screenshots/error_{item.name}_{timestamp}.png"
            
            os.makedirs("reports/screenshots", exist_ok=True)
            driver.save_screenshot(screenshot_path)
            print(f"\nCaptura guardada en: {screenshot_path}")

@pytest.fixture
def url_base():
    return "https://reqres.in/api/users"

@pytest.fixture
def header_request():
    return {"x-api-key": "reqres-free-v1"}

