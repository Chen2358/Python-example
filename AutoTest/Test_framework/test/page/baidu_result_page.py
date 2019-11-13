from selenium.webdriver.common.by import By
from test.common.page.baidu_main_page import BaiDuMainPage


class BaiDuResultPage(BaiDuMainPage):

	loc_result_links = (By.XPATH, '//div[contains(@class,"result")]/h3/a')

	@property
	def result_link(self):
		return self.find_elements(*self.loc_result_links)