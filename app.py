from flask import Flask, render_template, request, redirect
import os
import requests
import json

app = Flask(__name__)


@app.route('/')
def home():
  files = os.listdir('static')
  return render_template('index.html', files=files)


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
    file = {"Image": None, "Name": None, "Type": None, "Price": None, "Desc": None, "ATK": None, "DEF": None,
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
      file['ATK'] = card['atk']
      file['Attribute'] = card['attribute']

      file['Image'] = card['card_images'][0]['image_url']

      price = card['card_prices'][0]['cardmarket_price']




    print(json.dumps(data, indent=4))
  else:
    # If the status code is not 200, there was an error
    print(f"Error: {response.status_code}")
  return render_template('api.html', files=file)


if __name__ == '__main__':
  app.run(port=3000)
