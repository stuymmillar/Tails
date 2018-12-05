import json
import urllib

from flask import Flask, request, session, redirect, render_template, flash


app = Flask(__name__)

@app.route('/')
def story():
    url_stub="http://api.nytimes.com/svc/topstories/v2/home.json?api-key="
    with open('keys.json') as f:
        key = json.load(f)["news"]
    req=urllib.request.urlopen(url_stub+key)
    fin=json.loads(req.read())

    return render_template("news.html",
                               news=fin["results"])
'''
                               url=fin["results"][0]["url"],
                               title=fin["results"][0]["title"],
                               abstract=fin["results"][0]["abstract"])'''

app.debug=True
app.run()
