from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from .BasePage import BasePage
import time


class SearchResultsPage(BasePage):
    """
    Implements actions on the page with dresses
    """
    result_text = (By.XPATH, "//*[@id='js-product-list-top']/div[1]/p")
    lst = (By.XPATH, "//*[@id='js-product-list']/div[1]")
    items = (By.XPATH, "article")
    price = (By.XPATH, "div/div/div/span[@class='price']")
    # sorting_popup = (By.CLASS_NAME, "material-icons pull-xs-right")
    sorting_popup = (By.XPATH, "//*[@id='js-product-list-top']/div[2]/div/div")
    from_high = (By.XPATH, "div/a")
    item_prices = (By.XPATH, "div/div/div/span")

    ALL_PRICES = []  # pool of items prices and discounts

    @staticmethod
    def price_customizer(lst):
        """
        Static method that transforms the string representation of prices and discounts to floats and ints
        """
        time.sleep(0.25)
        result = {"price": float(str(lst[0][:-2]).replace(',', '.'))}
        if len(lst) > 1:
            result["discount"] = int(lst[1][:-1])
            result["new price"] = float(str(lst[2][:-2]).replace(',', '.'))
        return result

    def find_items(self):
        """
        Bounded method that returns the list of items on the page
        """
        while True:
            try:
                result_list = self.wait.until(EC.presence_of_element_located(SearchResultsPage.lst))
                return result_list.find_elements(*SearchResultsPage.items)
            except StaleElementReferenceException:
                pass

    def check_results_count(self):
        """
        Returns True if title of the items list contains correct number of items
        """
        shown_text = self.browser.find_element(*SearchResultsPage.result_text)
        items = self.find_items()
        return shown_text.text == f'Товаров: {len(items)}.'

    def check_dollar(self):
        """
        Checks if the USD signs are present in the items prices
        """
        dollar = self.get_currency_sign()
        items = self.find_items()
        return dollar, [item.find_element(*SearchResultsPage.price).text for item in items]

    def set_sort_from_high(self):
        """
        Performs the sorting of items on the page from highest to lowest price
        """
        popup = self.browser.find_element(*SearchResultsPage.sorting_popup)
        popup.find_element_by_xpath("a/i").click()
        sort_types = popup.find_elements(*SearchResultsPage.from_high)
        # //div[@class='dropdown-menu']//a
        sort_types[-1].click()

    def is_sorted(self):
        """
        Returns the empty list if items correctly sorted
        """
        time.sleep(1)
        items = self.find_items()
        for item in items:
            prices = item.find_elements(*SearchResultsPage.item_prices)
            tmp = SearchResultsPage.price_customizer([price.text for price in prices[:-1]])
            SearchResultsPage.ALL_PRICES.append(tmp)
        price_order = [p["price"] for p in SearchResultsPage.ALL_PRICES]
        return [i for i, j in zip(price_order, sorted(price_order, reverse=True)) if i != j]

    @classmethod
    def check_discount(cls):
        """
        Returns the tuple with the pairs of computed discounts and actual prices of the items
        """
        discounted_items = [tuple(prices.values()) for prices in SearchResultsPage.ALL_PRICES if len(prices) > 1]
        items_for_check = tuple(map(lambda item: round(item[2] - item[0]*item[1]/100, 2), discounted_items))  # making tuple with computed discounts for every item
        return tuple(zip(items_for_check, discounted_items))

