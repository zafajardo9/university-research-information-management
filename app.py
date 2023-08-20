from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'universityResearch',
    #     'USER': 'zackery',
    #     'PASSWORD': 'zackery1234',
    # }

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://zackery:zackery1234@localhost/universityResearch'

db=SQLAlchemy(app)


@app.get("/")
def home():
    return render_template("main.html")  


@app.route("/login")
def login():
    return render_template("login.html")  


@app.route("/signup")
def signup():
    return render_template("signup.html")  


if __name__ == '__main__':
    app.run(debug=True)