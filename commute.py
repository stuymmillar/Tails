from flask import Flask, render_template
import json
from urllib import request

app = Flask(__name__)

@app.route('/')
def render_test():
    homelat = 
    url = "https://transit.api.here.com/v3/route.json?app_id=7jNm9uNlO3Up0edHuqK0&app_code=6QxzobcNH0yyWBd27YItEg&routing=all&dep=" homelat + "," + homelong + "&arr=" + schoollat + "," + schoollong + "&time=2018-11-27T07%3A30%3A00"
    data = json.loads((request.urlopen(url)).read())
    return str(data)

if __name__ == '__main__':
    app.debug = True
    app.run()


