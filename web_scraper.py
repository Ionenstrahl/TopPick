from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# import pydash


SEVENTEEN_LANDS_PATH = "https://www.17lands.com/card_ratings"
SCRYFALL_PATH = "https://scryfall.com/card/neo/"  # https://scryfall.com/card/neo/1/ancestral-katana


class WebScraper:

    class Common:
        def __init__(self):
            self.num = 0
            self.name = ""
            self.color = ""
            self.winrate = 0
            self.img_url = ""

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")  # recommended for headless chrome on win
        chrome_options.add_argument("--headless")

        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        self.edition = ""
        self.commons = []

    def create_commons(self):
        self.driver.get(SEVENTEEN_LANDS_PATH)

        # Edition
        edition_xpath = "//select[@name='expansion']/option"
        edition_condition = EC.presence_of_element_located((By.XPATH, edition_xpath))
        edition_element = WebDriverWait(self.driver, 10).until(edition_condition)
        self.edition = edition_element.get_attribute("value")
        print(self.edition)

        # wait for card data to load
        card_xpath = "//tr[td/div/@class='list_card']"
        card_condition = EC.presence_of_element_located((By.XPATH, card_xpath))
        card = WebDriverWait(self.driver, 10).until(card_condition)

        # relevant common Data
        cards = self.driver.find_elements(By.XPATH, card_xpath)
        num = 0
        total = len(cards)
        for card in cards:
            num += 1
            print(f"{num}/{total}")
            attributes = card.find_elements(By.TAG_NAME, "td")
            rarity = attributes[2].text
            if rarity == "C":
                common = self.Common()
                common.num = num
                common.name = attributes[0].text
                common.color = attributes[1].text
                common.winrate = int(attributes[14].text[:2])
                self.commons.append(common)
                print(f"added {common.num}, len(commons)={len(self.commons)}")

    def add_img_url(self, common):
        print(f"self.edition {self.edition}")
        print(f"common.num {common.num}")
        self.driver.get(f"https://scryfall.com/card/{self.edition}/{common.num}")
        img_xpath = "//div[@class='card-profile']//img"
        img_condition = EC.presence_of_element_located((By.XPATH, img_xpath))
        img_element = WebDriverWait(self.driver, 10).until(img_condition)
        common.img_url = img_element.get_attribute("src")
