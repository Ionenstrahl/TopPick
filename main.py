import random

from flask import Flask, render_template
from web_scraper import WebScraper
from data_processing import DataProcessing
from flask_sqlalchemy import SQLAlchemy
import os


# APP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DB
class Common(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(10))
    winrate = db.Column(db.Float)
    img_url = db.Column(db.String(1000))


# WEB SCRAPING
scraper = WebScraper()


def create_commons():
    scraper.create_commons()
    for common in scraper.commons:
        new_common = Common(
            num=common.num,
            name=common.name,
            color=common.color,
            winrate=common.winrate,
            img_url=common.img_url
        )
        db.session.add(new_common)
        db.session.commit()


def sort_data(amount):
    sorted_commons = DataProcessing.sort_commons(scraper.commons)
    top_commons = DataProcessing.retrieve_top_commons(sorted_commons, amount)
    return top_commons


def add_urls(top_commons):
    for mono_color_commons in top_commons:
        for common in mono_color_commons:
            scraper.add_img_url(common)


create_commons()
top_commons = sort_data(3)
print(top_commons)
add_urls(top_commons)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)

# TODO
# add db
# add logic that db refreshes after load
# style
# headless browser
    # chrome_options = Options()
    # chrome_options.add_argument("--disable-gpu")  # recommended for headless chrome on win
    # chrome_options.add_argument("--headless")
    # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# responsive
# Dummy Image if not found

random_number = random.randint()