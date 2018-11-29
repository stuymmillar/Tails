from flask import Flask, render_template
import urllib, json

app = Flask(__name__)

@app.route('/')
def helloWorld():
    #Weather api
    #api_key = "49c480c99387a9288020a78b60fb253e"
    url = "https://api.openweathermap.org/data/2.5/weather?zip=10282,us&appid=49c480c99387a9288020a78b60fb253e"
    #url = url.replace('[]', api_key)
    result = json.loads(urllib.request.urlopen(url).read())
    return render_template('weather.html', u=result)

if __name__ == '__main__':
    app.debug = True
    app.run()
