from flask import Flask, render_template
import urllib, json

app = Flask(__name__)

@app.route('/')
def helloWorld():
    url = "https://api.openweathermap.org/data/2.5/weather?zip=10282,us&appid="
    with open('keys.json') as f:
        key = json.load(f)["weather"]
    url += key
    result = json.loads(urllib.request.urlopen(url).read())
    return render_template('weather.html', u=result)

if __name__ == '__main__':
    app.debug = True
    app.run()
