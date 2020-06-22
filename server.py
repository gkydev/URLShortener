from flask import Flask, redirect, request, render_template, abort, jsonify
import link_builder
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
#Director Class
global domain_name
#Change domain_name with your domain name
domain_name = "127.0.0.1:5000"
class UrlDatabaseModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    real_link = db.Column(db.String(100),unique=False,nullable=False)
    ip_addy = db.Column(db.String(20),unique=False,nullable=False)
    ad_type = db.Column(db.String(5),unique=False,nullable=False)
    token = db.Column(db.String(10),unique=True,nullable=False)
    date = db.Column(db.String(20),unique=False,nullable=False)
    hour = db.Column(db.String(20),unique=False,nullable=False)
    def __repr__(self):
        return f"Url('{self.id}','{self.real_link}','{self.ip_addy}','{self.ad_type}','{self.token}','{self.date}','{self.hour}')"
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
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/shortit',methods=["POST"])
def short_it():
    #Building url
    builder = CreateUrl(str(request.form.getlist("ad_type")[0])).create()
    builder.get_ip_addy(request.remote_addr)
    builder.get_real_link(request.form["urltoshorten"])
    builder.generate_token()
    created_url = UrlDatabaseModel(real_link= builder.link.real_link,ip_addy= builder.link.ip_addy,ad_type=builder.link.ad_type,token=builder.link.token,date=builder.link.date,hour=builder.link.hour)
    db.session.add(created_url)
    db.session.commit()
    return redirect("/")
@app.route('/api/shortit',methods=["POST"])
def api_short_it():
    try:
        builder = CreateUrl(request.json["ad_type"]).create()
        builder.get_ip_addy(request.remote_addr)
        builder.get_real_link(request.json["url"])
        builder.generate_token()
        created_url = UrlDatabaseModel(real_link= builder.link.real_link,ip_addy= builder.link.ip_addy,ad_type=builder.link.ad_type,token=builder.link.token,date=builder.link.date,hour=builder.link.hour)
        db.session.add(created_url)
        db.session.commit()
        return_data = {
            "Status": "Success",
            "Shortened_url": "http://" + domain_name + "/" + builder.link.token
        }
    except ValueError:
        return_data = {
            "Status": "Failure"
        }
    return jsonify(return_data)
@app.route("/shortenedlinks")
def shortenedlinks():
    URLs = UrlDatabaseModel.query.all()
    return render_template("shortenedlinks.html",URLs=URLs)
@app.route('/<token>')
def redirect_to(token):
    URLs = UrlDatabaseModel.query.all()
    for URL in URLs:
        if URL.token == token:
            if "http://" in URL.real_link: 
                    return redirect(URL.real_link)
            else:
                return redirect(("http://" + URL.real_link))
    print(token)
    return abort(404)
if __name__=='__main__':
    app.run(debug=True)

