import datetime as dt
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists
from web_scraper import WebScraper


# APP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///common.db")
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
    timestamp = db.Column(db.DateTime)
    edition = db.Column(db.String(100))


def create_and_update_commons():
    if not database_exists("sqlite:///common.db") or Common.query.first() is None:
        db.create_all()
        create_commons()
    if needs_updated():
        db.drop_all()
        db.create_all()
        create_commons()


def needs_updated():
    last_update_date = Common.query.get(1).timestamp.strftime('%Y-%m-%d')
    current_date = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d')
    return current_date != last_update_date


def get_top_commons_white():
    return Common.query.filter_by(color="W").order_by(Common.winrate.desc()).limit(5).all()


def get_top_commons_blue():
    return Common.query.filter_by(color="U").order_by(Common.winrate.desc()).limit(5).all()


def get_top_commons_black():
    return Common.query.filter_by(color="B").order_by(Common.winrate.desc()).limit(5).all()


def get_top_commons_red():
    c = Common.query.filter_by(color="R").order_by(Common.winrate.desc()).limit(5).all()
    print(c[0].img_url)


def get_top_commons_green():
    return Common.query.filter_by(color="G").order_by(Common.winrate.desc()).limit(5).all()


def get_top_commons_colorless():
    return Common.query.filter_by(color="").order_by(Common.winrate.desc()).limit(5).all()


def get_top_commons_multicolor():
    return Common.query.filter(len(Common.color) > 1).order_by(Common.winrate.desc()).limit(5).all()


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
            img_url=common.img_url,
            timestamp=dt.datetime.now(dt.timezone.utc),
            edition=common.edition
        )
        db.session.add(new_common)
        db.session.commit()


def add_urls(top_commons):
    for mono_color_commons in top_commons:
        for common in mono_color_commons:
            scraper.retrieve_img_url(common)


# MAIN
create_and_update_commons()
print(get_top_commons_red())
# add_urls(top_commons)


# SERVER
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)

# TODO
# db: create img_url
# style
# headless browser
    # chrome_options = Options()
    # chrome_options.add_argument("--disable-gpu")  # recommended for headless chrome on win
    # chrome_options.add_argument("--headless")
    # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# responsive
# Dummy Image if not found
