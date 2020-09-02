from settings import FIREFOX, CHROME, URL
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from enum import Enum
from . import get_desired_capabilities, get_environment, get_sauce_labs_capabilities, get_browser_stack_capabilities
import pytest
import configparser
import os


config = configparser.ConfigParser()
config.read(f'tests{os.sep}remote_services.ini')


ENV = get_environment()

HUB = "http://192.168.99.100:4444/wd/hub"
# "http://192.168.99.100:4444/wd/hub" --> for Docker
# "http://localhost:4444/wd/hub" --> for SeleniumGrid

BROWSER = None

capabilities = {
  'browserName': 'MicrosoftEdge',
  'browserVersion': '84.0',
  'platformName': 'Windows 10',
  'sauce:options': {
  }
}


class ServiceEnvEnum(Enum):
    SouceLabs = 1, "ondemand.eu-central-1.saucelabs.com:443"
    BrowserStack = 2, "hub-cloud.browserstack.com"

    def __init__(self, _id, title):
        self.id = _id
        self.title = title


class ServiceConfig:

    _ENV = ServiceEnvEnum

    def __init__(self, username, access_key, num):
        self._username = username
        self._access_key = access_key
        self._num = num

    @property
    def command(self):
        target = (i.title for i in self._ENV if i.id == self._num)
        return f"https://{self._username}:{self._access_key}@{next(target)}/wd/hub"


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

    BROWSER = webdriver.Remote(
        command_executor="http://192.168.99.100:4444/wd/hub",
        desired_capabilities=request.param)

    print(f"\n\n\n{request.param}\n\n")

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


def setup_multiple_service(request):
    global BROWSER, user, access, number
    service_config = ServiceConfig(user, access, number)

    BROWSER = webdriver.Remote(
        command_executor=service_config.command,
        desired_capabilities=request.param)

    print(f"\n\n\n{request.param}\n\n")

    BROWSER.get(URL)
    BROWSER.maximize_window()

    request.cls.browser = BROWSER
    yield
    BROWSER.close()


if ENV.sauce_labs:
    user = config['Sauce Labs']['username']
    access = config['Sauce Labs']['access_key']
    number = 1
    setup = pytest.fixture(scope="class", params=get_sauce_labs_capabilities())(setup_multiple_service)
elif ENV.browser_stack:
    user = config['Browser Stack']['username']
    access = config['Browser Stack']['access_key']
    number = 2
    setup = pytest.fixture(scope="class", params=get_browser_stack_capabilities())(setup_multiple_service)
else:
    if ENV.single_run:
        setup = setup_single
    else:
        setup = setup_multiple




