import link_builder
from app import app, db
from app import UrlDatabaseModel
import link_builder
from flask import redirect, request, render_template, abort, jsonify
from app import CreateUrl

@app.route('/')
def index():
    return render_template("index.html")

global domain_name 
domain_name = 'http://localhost:5000'

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
