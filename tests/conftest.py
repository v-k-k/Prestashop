from settings import FIREFOX, CHROME, URL
from selenium import webdriver
import pytest


BROWSER = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="firefox"
    )


@pytest.fixture(scope="class", autouse=True)
def setup(request):
    global BROWSER
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

'''
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
        driver.get_screenshot_as_file(name)

'''