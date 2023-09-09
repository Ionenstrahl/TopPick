import requests

URL = "https://api.scryfall.com/cards/search"


class ScryFall:

    @staticmethod
    def request_img_urls(card_name):
        print(ScryFall.__create_params(card_name))
        response = requests.get(url=URL, params=ScryFall.__create_params(card_name))
        print(response)
        card = response.json()["data"][0]
        print(card)
        img_urls = ScryFall.get_img_urls(card)
        return {
            "img": img_urls["border_crop"],
            "cropped_img": img_urls["art_crop"]
        }

    @staticmethod
    def get_img_urls(card):
        if ScryFall.is_adventure(card):
            return card["image_uris"]
        if ScryFall.is_double_faced(card):
            return card["card_faces"][0]["image_uris"]
        else:
            return card["image_uris"]

    @staticmethod
    def is_adventure(card):
        return card["layout"] == "adventure"

    @staticmethod
    def is_double_faced(card):
        return "card_faces" in card

    @staticmethod
    def __create_params(query):
        return {
            "q": query,
            "unique": "cards",
            "order": "released"
        }
