import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


SEVENTEEN_LANDS_PATH = "https://www.17lands.com/card_ratings"
SCRYFALL_PATH = "https://scryfall.com/card/neo/"                # e.g. https://scryfall.com/card/neo/1/ancestral-katana


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

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.edition = ""
        self.commons = []

    def create_commons(self):
        self.driver.get(SEVENTEEN_LANDS_PATH)

        self.edition = self.scrap_edition()
        time.sleep(3)
        self.commons = self.scrap_commons()

    def scrap_edition(self):
        edition_xpath = "//select[@name='expansion']/option"
        edition_condition = EC.presence_of_element_located((By.XPATH, edition_xpath))
        edition_element = WebDriverWait(self.driver, 10).until(edition_condition)
        return edition_element.get_attribute("value")

    def scrap_commons(self):
        cards = self.scrap_all_cards()
        return self.filter_commons(cards)

    def scrap_all_cards(self):
        card_xpath = "//tr[td/div/@class='list_card']"
        return self.driver.find_elements(By.XPATH, card_xpath)

    def filter_commons(self, cards):
        num = 0
        total = len(cards)
        commons = []
        for card in cards:
            num += 1
            print(f"{num}/{total}")
            attributes = card.find_elements(By.TAG_NAME, "td")
            if is_common(attributes):
                commons.append(self.create_common(attributes, num))
        return commons

    def create_common(self, attributes, num):
        common = self.Common()
        common.num = num
        common.name = attributes[0].text
        common.color = attributes[1].text
        common.winrate = int(attributes[14].text[:2])
        return common

    def add_img_url(self, common):
        print(f"self.edition {self.edition}")
        print(f"common.num {common.num}")
        self.driver.get(f"https://scryfall.com/card/{self.edition}/{common.num}")
        img_xpath = "//div[@class='card-profile']//img"
        img_condition = EC.presence_of_element_located((By.XPATH, img_xpath))
        img_element = WebDriverWait(self.driver, 10).until(img_condition)
        common.img_url = img_element.get_attribute("src")
