from flask import  Flask, render_template, jsonify, request
from flask_paginate import Pagination,get_page_args
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
uri = "mongodb+srv://xchar:minionswar2@cluster0.2loqznr.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
db = client.get_database('tienda-uruloki')  # Replace with your database name
collection = db.get_collection('juegos-de-mesa')  # Replace with your collection name


RESULTS_PER_PAGE = 12 # Number of results per page

GOOGLE_API_KEY = 'AIzaSyBpYcf0TjJrOI2Aw3UJ5_KLDJQewicguEw'

app.template_folder = "Templates"

@app.route('/')
def home():
    items = list(collection.find().sort('_id', -1).limit(5))
    return render_template('home.html', items=items)

@app.route('/Torneos')
def torneos():
    return render_template('torneos.html')

@app.route('/Tienda')
def tienda(): 
    return render_template('tienda.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/inventario')
def inventario():
    return render_template('inventario.html')
    
if __name__ == '__main__':
    app.run(debug=True)