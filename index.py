from flask import Flask
from flask import render_template
import os
import json
import time
import urllib


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World";

@app.route("/goodbye")
def goodbye():
    return "Goodye, World!"

@app.route("/hello/<name>/<int:age>")
def hello(name,age):
    return "Hello, {}, you are {} years old.".format(name, age)

@app.route("/weather/<searchcity>")
def get_weather(searchcity="London"):

    url=  "http://api.openweathermap.org/data/2.5/forecast/daily?g={}&cnt=10&mode=json&units=metric&APPID=fc7b81c70e613b852f216410cf2f7cfd".format(searchcity)
    response = urllib.request.urlopen(url).read().decode('utf8');
    data  = json.loads(response)

    city = data['city']['name']
    country = data['city']['country']
    forecast_list=[]

    for d in data.get('list'):
        day = time.strftime('%A %d %B %G',time.localtime(d.get('dt')))
        mini = d.get('temp').get('min')
        maxi = d.get('temp').get('max')
        description = d.get('weather')[0].get('description')
        forecast_list.append((day,mini,maxi,description));

    return render_template('index.html',forecast_list = forecast_list,city=city,country=country)


@app.route("/followers/<username>")
def followers(username='david'):
    url="https://api.github.com/users/{}/followers".format(username)
    response = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(response)

    users =[]
    for d in data:
        user={}
        user["login"]=d["login"]
        user["imageSrc"]=d["avatar_url"]
        user["link"]=d["html_url"]
        users.append(user)

    return render_template("followers.html",users=users)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=port,debug=True)
