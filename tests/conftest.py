from settings import FIREFOX, CHROME, URL
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import pytest


BROWSER = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class", autouse=True)
def setup(request):
    global BROWSER, desiredCapabilities
    browser_name = request.config.getoption("browser_name")

    if browser_name == "chrome":
        BROWSER = webdriver.Chrome(executable_path=CHROME)
    elif browser_name == "firefox":
        BROWSER = webdriver.Firefox(executable_path=FIREFOX)

    BROWSER.get(URL)
    BROWSER.maximize_window()

    request.cls.browser = BROWSER
    yield
    BROWSER.close()

