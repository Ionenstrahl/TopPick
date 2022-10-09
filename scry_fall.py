import requests

URL = "https://api.scryfall.com/cards/search"


class ScryFall:

    @staticmethod
    def request_img_urls(self, card_name):
        response = requests.get(url=URL, params=self.create_params(card_name))
        img_urls = response.json()["data"][0]["image_uris"]
        return {
            "img": img_urls["border_crop"],
            "cropped_img": img_urls["art_crop"]
        }

    @staticmethod
    def __create_params(query):
        return {
            "q": query,
            "unique": "cards",
            "order": "released"
        }
