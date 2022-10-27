from flask import Flask, render_template
from blueprint import bp_user, bp_food, bp_note
from datetime import timedelta
import time

app = Flask(__name__)
app.secret_key = 'p\x8aE\xce\xa2\xc9dS\xab\xf4Az<J\x82\xcb'
app.permanent_session_lifetime = timedelta(hours=12)
app.debug = True

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/page-introduction')
def page_intro():
    return render_template('page_intro.html')

app.register_blueprint(bp_user)
app.register_blueprint(bp_food)
app.register_blueprint(bp_note)

app.run()
