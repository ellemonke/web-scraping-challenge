from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_info = mongo.db.mars_data.find_one()
    # return render_template("index.html", mars_info=mars_info)
    return render_template('index.html', mars_info=mars_info)

@app.route("/scrape")
def scraper():
    mars_info = mongo.db.mars_data
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

@app.route("/hemispheres")
def hemispheres():
    mars_info = mongo.db.mars_data.find_one()
    return render_template("mars_hemispheres.html", mars_info=mars_info)

# Preview on http://127.0.0.1:5000/
if __name__ == "__main__":
    app.run(debug=True)
