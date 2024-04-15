from flask import Flask, render_template,request,redirect
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

      data = response.json()

      cards = data['data']

      for card in cards:
        print(card['name'])
        print(card['type'])
        print(card['desc'])

        for card_set in card['card_sets']:
          print(card_set['set_name'])

        for card_image in card['card_images']:
          file.append(card_image['image_url'])

      print(json.dumps(data, indent=4))
    else:
      # If the status code is not 200, there was an error
      print(f"Error: {response.status_code}")
    return render_template('api.html', files=file)

if __name__ == '__main__':
    app.run(port=3000)
