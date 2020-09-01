from settings import FIREFOX, CHROME, URL
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from enum import Enum
from .utils import get_desired_capabilities, get_environment
import pytest


ENV = get_environment()

HUB = "http://192.168.99.100:4444/wd/hub"
# "http://192.168.99.100:4444/wd/hub" --> for Docker
# "http://localhost:4444/wd/hub" --> for SeleniumGrid

BROWSER = None


class DesiredCapabilitiesEnum(Enum):
    Grid = {
        "chrome": DesiredCapabilities.CHROME,
        "firefox": DesiredCapabilities.FIREFOX
    }
    Selenoid = {
        "browserName": "chrome",
        "version": "85.0",
        "enableVNC": True,
        "enableVideo": False
    }


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class", params=get_desired_capabilities())
def setup_multiple(request):
    global BROWSER, ENV
    browser_name = request.config.getoption("browser_name")

    # BROWSER = webdriver.Remote(desired_capabilities=desiredCapabilities, command_executor=HUB)
    BROWSER = webdriver.Remote(
        command_executor="http://192.168.99.100:4444/wd/hub",
        desired_capabilities=request.param)

    print(f"\n\n\n{request.param}\n\n\n")

    BROWSER.get(URL)
    BROWSER.maximize_window()

    request.cls.browser = BROWSER
    yield
    BROWSER.close()


@pytest.fixture(scope="class")
def setup_single(request):
    global BROWSER, ENV

    if ENV.use_selenoid:
        caps = DesiredCapabilitiesEnum.Selenoid.value
    else:
        caps = DesiredCapabilitiesEnum.Grid.value

    BROWSER = webdriver.Remote(
        command_executor="http://192.168.99.100:4444/wd/hub",
        desired_capabilities=caps)

    BROWSER.get(URL)
    BROWSER.maximize_window()

    request.cls.browser = BROWSER
    yield
    BROWSER.close()


if ENV.single_run:
    setup = setup_single
else:
    setup = setup_multiple
