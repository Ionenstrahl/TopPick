from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
import os


class DataBase:

    # speicher Datum letztes Update
    # speicher editions_name

    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(app)

    class Commons(self.db.Model):
        id = self.db.Column(self.db.Integer, primary_key=True)
        num = self.db.Column(self.db.String(100), unique=True)
        name = self.db.Column(self.db.String(100))
        color = self.db.Column(self.db.String(10))
        winrate = ""
        img_url = ""

        def __init__(self):
            __tablename__ = "commons"


            # self.num = 0
            # self.name = ""
            # self.color = ""
            # self.winrate = 0
            # self.img_url = ""
        # This will act like a List of BlogPost objects attached to each User.
        # The "author" refers to the author property in the BlogPost class.
        blog_posts = relationship("BlogPost", back_populates="author")
        comments = relationship("Comment", back_populates="author")

    def check_card_mapping(self):
        pass

    def update_card_mapping(self):
        pass




class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = Column(Integer, ForeignKey('users.id'))
    # Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = relationship("User", back_populates="blog_posts")
    comments = relationship("Comment", back_populates="blog_post")
