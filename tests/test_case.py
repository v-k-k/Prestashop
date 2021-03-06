from PageObjects.HomePage import HomePage
from PageObjects.SearchResultPage import SearchResultsPage
from tests.BaseClass import BaseClass
from allure_commons.types import AttachmentType
import allure


class TestCase(BaseClass):

    @allure.feature("Check currency signs for all the items")
    @allure.story("Doing first test...")
    @allure.severity("TRIVIA")
    def test_currency_signs(self):
        """
        Checks if all the items currency signs matches with the currency sign in the header
        """
        home_page = HomePage(self.browser)
        result = home_page.check_items_currency()
        assert result[0] == result[1]
        home_page.make_dollar()
        home_page.search_dress()

    @allure.feature("Check the title content of the page")
    @allure.story("Doing second test...")
    @allure.severity("TRIVIA")
    def test_title_text(self):
        """
        Checks if the title matches with the pattern and number of items
        """
        result_page = SearchResultsPage(self.browser)
        assert result_page.check_results_count()

    @allure.feature("Check if USD sign are present")
    @allure.story("Doing third test...")
    @allure.severity("CRITICAL")
    def test_dollar(self):
        """
        Checks if the USD signs are present in all the items prices
        """
        result_page = SearchResultsPage(self.browser)
        dollar, prices = result_page.check_dollar()
        for text in prices:
            assert dollar in text

    @allure.feature("Check if items are sorted")
    @allure.story("Doing fourth test...")
    @allure.severity("CRITICAL")
    def test_sorting(self):
        """
        Checks if list of items sorted correctly
        """
        result_page = SearchResultsPage(self.browser)
        result_page.set_sort_from_high()
        #with allure.step("Doing screenshot"):
         #   allure.attach(result_page.browser.get_screenshot_as_png(),
          #                name="screenshit", attachment_type=AttachmentType.PNG)
        assert not len(result_page.is_sorted())

    @allure.feature("Check the discounts")
    @allure.story("Doing fifth test...")
    @allure.severity("CRITICAL")
    def test_discount(self):
        """
        Checks if the discounted price correctly computed
        """
        result_page = SearchResultsPage(self.browser)
        pairs = result_page.check_discount()
        for pair in pairs:
            assert pair[0] == pair[1][0]
