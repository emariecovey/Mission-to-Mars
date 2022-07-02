#using flask to render a template, redirect to another url, and create a url
from flask import Flask, render_template, redirect, url_for
#use PyMongo to interact with Mongo database
from flask_pymongo import PyMongo
#using scraping code (from scraping.py) by converting Jupyter notebook to python
import scraping


#set up flask
#flask routes bind functions to urls. Routes can be embedded in a web app and accessed through links or buttons 
app = Flask(__name__)


#connect Mongo using Pymongo:
#our app will connect to Mongo using uri (uniform resource identifier, which is like a url)
app.config["MONGO_URI"]="mongod://localhost:27017/mars_app" #uri says app can reach mongo through our local server, using port 27017 and a database named "mars_app"
mongo = Pymongo(app)


#main HTML page flask route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one() #find mars collection
    return render_template("index.html", mars=mars) #make html template from index file of scraped data

#index.html is the default html file we're using to display the content being scraped, 
# so when we're in the web app's html page, we'll see the home page  
#mars = ... uses pymongo to find "mars" collection on database
#return render... tells flask to return HTML template using an index.html file
#mars=mars says to use mars collection in MongoDB



#flask route that will actually scrape new data with code
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

#this allows us to access mars database, 
# scrape data with scraping.py using scrape_all function
# update the database with new data, inserting but not if an identical record exists. 
# because the update_one brackets are empty, it will update the first matching document in the collection
# upsert=True means that mongo needs to create a new document if one doesn't exist and that new data will always be saved, even if we haven't created a document for it
# Here's the syntax: .update_one(query_parameter, {"$set": data}, options)
# there's a redirect at the end to navigate back to the '/' page to see updated content

#need these last to lines to tell flask to run
if __name__ == "__main__":
   app.run() #debug=true inside parentheses if developing