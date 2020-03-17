from PageObjects.HomePage import HomePage
from PageObjects.SearchResultPage import SearchResultsPage
from tests.BaseClass import BaseClass


class TestCase(BaseClass):

    def test_currency_signs(self):
        """
        Checks if all the items currency signs matches with the currency sign in the header
        """
        home_page = HomePage(self.browser)
        result = home_page.check_items_currency()
        assert result[0] == result[1]
        home_page.make_dollar()
        home_page.search_dress()

    def test_title_text(self):
        """
        Checks if the title matches with the pattern and number of items
        """
        result_page = SearchResultsPage(self.browser)
        assert result_page.check_results_count()

    def test_dollar(self):
        """
        Checks if the USD signs are present in all the items prices
        """
        result_page = SearchResultsPage(self.browser)
        dollar, prices = result_page.check_dollar()
        for text in prices:
            assert dollar in text

    def test_sorting(self):
        """
        Checks if list of items sorted correctly
        """
        result_page = SearchResultsPage(self.browser)
        result_page.set_sort_from_high()
        assert not len(result_page.is_sorted())

    def test_discount(self):
        """
        Checks if the discounted price correctly computed
        """
        result_page = SearchResultsPage(self.browser)
        pairs = result_page.check_discount()
        for pair in pairs:
            assert pair[0] == pair[1][0]

'''
    def test_formSubmission(self,getData):
        log = self.getLogger()
        homepage= HomePage(self.driver)
        log.info("first name is "+getData["firstname"])
        homepage.getName().send_keys(getData["firstname"])
        homepage.getEmail().send_keys(getData["lastname"])
        homepage.getCheckBox().click()
        self.selectOptionByText(homepage.getGender(), getData["gender"])

        homepage.submitForm().click()

        alertText = homepage.getSuccessMessage().text

        assert ("Success" in alertText)
        self.driver.refresh()

    @pytest.fixture(params=HomePageData.getTestData("Testcase2"))
    def getData(self, request):
        return request.param
'''