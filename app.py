from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    files = os.listdir('static')
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(port=3000)
