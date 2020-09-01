from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    """
    Implements the base test-page
    """
    currency = (By.XPATH, "//*[@id='_desktop_currency_selector']/div/span[2]")

    def __init__(self, browser):
        self.browser = browser

    def get_currency_sign(self):
        """
        Gets the current currency sign in the header
        """
        currency_signs = self.browser.find_element(*BasePage.currency).text.split()
        return currency_signs[1]

    @property
    def wait(self):
        """
        Protected method that returns 10 sec explicit waiting
        """
        return WebDriverWait(self.browser, 10)

    @property
    def action(self):
        return ActionChains(self.browser)


