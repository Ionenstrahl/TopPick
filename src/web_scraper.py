import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from src.scry_fall import ScryFall

SEVENTEEN_LANDS_PATH = "https://www.17lands.com/card_data"  # ?user_group=top"


def is_common(attributes):
    rarity = attributes[2].text
    return rarity == "C"


class WebScraper:
    class Common:
        def __init__(self):
            self.num = 0
            self.name = ""
            self.color = ""
            self.winrate = 0
            self.img_url = ""
            self.cropped_img_url = ""
            self.edition = ""

    def __init__(self):
        self.edition = ""
        self.commons = []

    def create_commons(self):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get(SEVENTEEN_LANDS_PATH)

        self.edition = self.__scrap_edition(driver)
        time.sleep(3)
        self.commons = self.__scrap_commons(driver)

    def __scrap_edition(self, driver):
        edition_xpath = "//select[@name='expansion']/option"
        edition_condition = EC.presence_of_element_located((By.XPATH, edition_xpath))
        edition_element = WebDriverWait(driver, 10).until(edition_condition)
        return edition_element.get_attribute("value").lower()

    def __scrap_commons(self, driver):
        cards = self.__scrap_all_cards(driver)
        return self.__filter_commons(cards)

    def __scrap_all_cards(self, driver):
        card_xpath = "//tr[td/div/@class='list_card']"
        return driver.find_elements(By.XPATH, card_xpath)

    def __filter_commons(self, cards):
        num = 0
        total = len(cards)
        commons = []
        for card in cards:
            num += 1
            print(f"{num}/{total}")
            attributes = card.find_elements(By.TAG_NAME, "td")
            if is_common(attributes):
                commons.append(self.__create_common(attributes, num))
        return commons

    def __create_common(self, attributes, num):
        common = self.Common()
        common.num = num
        common.name = attributes[0].text
        common.color = attributes[1].text

        scraped_winrate = attributes[15].text[:4]
        common.winrate = float(scraped_winrate) if len(scraped_winrate) > 0 else 0.0
        common.edition = self.edition

        img_urls = ScryFall.request_img_urls(common.name)
        common.img_url = img_urls["img"]
        common.cropped_img_url = img_urls["cropped_img"]
        return common
