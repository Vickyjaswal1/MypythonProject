from    flask import Flask ,request
from    flask  import render_template
from flask_sqlalchemy import SQLAlchemy
import json

#connection with json file

with open('config.json' , 'r') as c:
    params= json.load(c)["params"]

local_server=True


#Database connection
app = Flask(__name__)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_server']
else:
        app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_server']

db = SQLAlchemy(app)

#contact page  and table connection
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(30), unique=True, nullable=False)
    message=db.Column(db.String(30), unique=True, nullable=False)
    date = db.Column(db.String(10), unique=True, nullable=True)
   
class posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(20), unique=False, nullable=False)
    content = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.String(30), unique=True, nullable=False)
    slug=db.Column(db.String(30), unique=True, nullable=False)
    

@app.route("/")
def hello_world():
#                                     here params=parms means to configure the fb urls and other urls in the page from json
    return render_template("index.html", params=params)

@app.route("/about")
def about():
    return render_template("about.html",params=params)


@app.route("/post/<string:post_slug>", methods=['GET'])

def post_route(post_slug):
    post=posts.query.filter_by(slug=post_slug).first()

    return render_template("post.html",params=params,post=post)

@app.route("/contact" , methods = ['POST', 'GET'])
def contact():
    #fetching entry to DB
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
#add entry to DB
        entry=contact(name=name, phone=phone , message=message, email=email)
        db.session.add(entry)
        db.session.commit()


    return render_template("contact.html",params=params)





app.run(debug=True)
