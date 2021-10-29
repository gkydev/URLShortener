from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

import link_builder

#DB Model
class UrlDatabaseModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    real_link = db.Column(db.String(100),unique=False,nullable=False)
    ip_addy = db.Column(db.String(20),unique=False,nullable=False)
    ad_type = db.Column(db.String(5),unique=False,nullable=False)
    token = db.Column(db.String(10),unique=True,nullable=False)
    date = db.Column(db.String(20),unique=False,nullable=False)
    hour = db.Column(db.String(20),unique=False,nullable=False)

class CreateUrl():
    def __init__(self, ad_type):
        self.ad_type = ad_type
    def create(self):
        if self.ad_type == "False":
            builder = link_builder.WithoutAdUrlBuilder()
            builder.get_ad_type()
            return builder
        elif self.ad_type == "True":
            builder = link_builder.AdUrlBuilder()
            builder.get_ad_type()
            return builder
