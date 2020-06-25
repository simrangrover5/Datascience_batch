from flask import Flask,render_template,request,jsonify
import requests
from filtering import filter
import json
from flask_restful import Resource,Api  #pip install flask_restful

app = Flask(__name__)
api = Api(app)   #crete an object of api

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/title/",methods=["POST","GET"])
def title():
    
    """
        This function is used to return movie data
    """
    
    movie = request.form.get("title")
    url = f"http://www.omdbapi.com/?t={movie}&apikey=e22bdd41"
    page = requests.get(url)
    data = json.loads(page.text)
    content = ['Title','Actors','Year','Genre','Released','Director','Plot','Language','imdbRating']
    d = {}
    for i in content:
        d[i]=data[i]
    poster = data['Poster']
    return render_template("movie.html",data=d,poster=poster)

@app.route("/lan/",methods=['GET','POST'])
def language():
    if request.method == "POST":
        lang = request.form.get("lan")
        df = filter()
        d1 = df[df['original_language'] == lang].sort_values(by="popularity",ascending=False)[:7][['original_title','homepage']]
        all_data = []
        for i,h in zip(d1['original_title'],d1['homepage']):
            url = f"http://www.omdbapi.com/?t={i}&apikey=e22bdd41"
            page = requests.get(url)
            if page.status_code == 200:
                data = json.loads(page.text)
                content = ['Title','Actors','Year','Genre','Released','Director','Plot','Language','imdbRating']
                d = {}
                try:
                    for i in content:
                        d[i]=data[i]
                    d['poster'] = data['Poster']
                    d['homepage'] = h
                    all_data.append(d)
                except:
                    pass
            else:
                pass
        return render_template("lang.html",data=all_data)

@app.route("/api/<movie>/")   #create your own api
def get_api(movie):
    url = f"http://www.omdbapi.com/?t={movie}&apikey=e22bdd41"
    page = requests.get(url)
    if page.status_code == 200:
        data = json.loads(page.text)
        content = ['Title','Actors','Year','Genre','Released','Director','Plot','Language','imdbRating','poster']
        d = {}
        try:
            for i in content:
                d[i]=data[i]
        except:
            pass
    else:
        pass
    return jsonify(d)

@app.route("/api/post/<name>/<int:age>")
def post_api(name,age):
    """Add your data into database"""
    return "Hello"


class Movie(Resource):

    def get(self):
        req = request.get_json()
        print(req)
        movie = req["movie"]
        url = f"http://www.omdbapi.com/?t={movie}&apikey=e22bdd41"
        page = requests.get(url)
        if page.status_code == 200:
            data = json.loads(page.text)
            content = ['Title','Actors','Year','Genre','Released','Director','Plot','Language','imdbRating','poster']
            d = {}
            try:
                for i in content:
                    d[i]=data[i]
            except:
                pass
        else:
            pass
        return jsonify(d)

api.add_resource(Movie,"/myapi/")

app.run(host="localhost",port=80,debug=True)
