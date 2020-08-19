from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_dataDB = mongo.db.mars.find_one()
    #mars_data = scrape_mars.scrape_all()
    # print("***")
    #print("THIS IS MARS DATA ", mars_data)
    return render_template("index.html", mars=mars_dataDB)
    #return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars_dataDB = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    #mars.replace_one({}, mars_data, upsert = True)
    mars_dataDB.update({}, mars_data, upsert = True)
    #return "Done Scraping"
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True, port = 5005)