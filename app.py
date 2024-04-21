from flask import Flask, redirect, render_template, request, session, jsonify, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
import requests
import json
import firebase_admin
from firebase_admin import credentials, db, firestore
from helpers import apology, login_required, reg_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

cred = credentials.Certificate("static/yugioh-database-539a5-firebase-adminsdk-382aq-baf14b700e.json")
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

@app.route('/')
def home():
  if not session:
    return render_template("index.html")

  session["filename"] = None
  session["chat_id"] = ""

  return render_template('index.html')


@app.route('/api')
def api_root():
  return render_template('api.html')


@app.route('/search', methods=['POST'])
def search():
  card = request.form.get('card')
  url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name=" + card

  response = requests.get(url)
  file = []
  if response.status_code == 200:
    file = {"Image": None, "Name": None, "Type": None, "Price": None, "Desc": 0,
            "Level": None, "Attribute": None}

    data = response.json()

    cards = data['data']

    for card in cards:
      print(card['name'])
      print(card['type'])
      print(card['desc'])
      file['Name'] = card['name']
      file['Type'] = card['type']
      file['Desc'] = card['desc']
      file['Image'] = card['card_images'][0]['image_url']

      if "Spell" in card['type'] or "Trap" in card['type']:
        #Nothing
        i = 1
      else:
        file['Attribute'] = card['attribute']


      price = float(card['card_prices'][0]['cardmarket_price'])

      for timi in card['card_prices']:
        for extra in timi:
          if price <= 0 :
            price = float(timi[extra])
          if (float(timi[extra])< price and price > 0 and float(timi[extra]) > 0):
            price = float(timi[extra])
      file['Price'] = price

    print(json.dumps(data, indent=4))
  else:
    # If the status code is not 200, there was an error
    return apology("Card Not Found")
  return render_template('api.html', files=file)

@app.route("/Login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("psw"):
            return apology("must provide password", 403)

        # Query database for username

        rows = (
            db_firestore.collection("users")
            .where("username", "==", request.form.get("username"))
            .get()
        )

        # Ensure username exists and password is correct
        user_data = rows[0].to_dict()
        if len(rows) != 1 or not check_password_hash(
            user_data["hash"], request.form.get("psw")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0].id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/Register", methods=["GET", "POST"])
def Register():
  session.clear()

  """Register user"""
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("psw")
    confirm = request.form.get("psw-repeat")

    info = db_firestore.collection("users").where("username", "==", username).get()

    if not username:
      return apology("Didnt input a username")
    elif info:
      return apology("Username already taken")
    elif not password:
      return apology("Didnt input password")
    elif not confirm:
      return apology("Didnt input confirmation")
    elif password != confirm:
      return apology("passwords do not match")

    hash = generate_password_hash(password)
    print(hash)
    db_firestore.collection("users").add({"username": username, "hash": hash[0]})

    # Query database for username
    rows = (
      db_firestore.collection("users")
      .where("username", "==", request.form.get("username"))
      .get()
    )

    # Remember which user has logged in
    session["user_id"] = rows[0].id

    return redirect("/")
  else:
    return render_template("register.html")

@app.route("/LogOut" ,methods=["GET", "POST"])
def LogOut():

  session.clear()
  return redirect("/")

if __name__ == '__main__':
  app.run(port=3000)
