from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv


def create_app():
  app = Flask(__name__)
  client = MongoClient(os.getenv("MONGODB_URI"))
  #
  app.db= client.entries
    
  entries= []
  @app.route('/', methods=["GET", "POST"])
  def home():
    #print([e for e in app.db.entries.find({})])
    entries_with_date = []
    if request.method == "POST":
      entry_content = request.form.get("content")
      formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
      # entries.append((entry_content, formatted_date))
      app.db.entries.insert_one({"content":entry_content,"date" : formatted_date}) 
      #print (app.db.entries.find({}))

      entries_with_date= [(
        entry['content'],
        ##datetime.datetime.strftime("%Y-%m-%d"),
        entry["date"],
        datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime('%b %d')
      )
        #[print("MongoDB Collection" , entry) 
        for entry in app.db.entries.find({})
      ]
      
    return render_template("home.html", entries=entries_with_date)
    #return render_template("home.html", entries=app.db.entries.find({}))
  return app 
