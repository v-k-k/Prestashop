from .BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):
    """
    Implements actions on the home page
    """
    most_populars = (By.XPATH, "//article")
    items_price = (By.XPATH, "div/div/div/span")
    catalog_input = (By.XPATH, "//form/input[2]")
    currencies = (By.XPATH, "//*[@id='_desktop_currency_selector']/div/ul/li/a")
    button_input = (By.XPATH, "../button")

    def check_items_currency(self):
        """
        Returns the tuple with the popular items count and number of items with correct currency sign
        """
        currency_sign = HomePage.get_currency_sign(self)
        popular_items = self.browser.find_elements(*HomePage.most_populars)
        prices = [item.find_element(*HomePage.items_price).text for item in popular_items
                  if currency_sign in item.find_element(*HomePage.items_price).text]
        return len(popular_items), len(prices)

    def make_dollar(self):
        """
        Selects the USD in the currencies list
        """
        show_currencies = self.browser.find_element(*HomePage.currency)
        show_currencies.click()
        currencies_list = show_currencies.find_element_by_xpath("..")
        currencies = currencies_list.find_elements(*HomePage.currencies)
        for cur in currencies:
            if "Доллар" in cur.get_attribute("title"):
                self.browser.execute_script("$(arguments[0]).click();", cur)
                # cur.click()
                break

    def search_dress(self):
        """
        Launch the searching by the keyword 'dress.'
        """
        input_field = self.browser.find_element(*HomePage.catalog_input)
        input_field.send_keys("dress.")
        input_field.find_element(*HomePage.button_input).click()

