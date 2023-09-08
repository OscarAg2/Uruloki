from flask import  Flask, render_template, request, jsonify
from flask_paginate import Pagination,get_page_args

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyBpYcf0TjJrOI2Aw3UJ5_KLDJQewicguEw'

app.template_folder = "templates"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Torneos')
def torneos():
    return render_template('torneos.html')

@app.route('/Tienda')
def tienda(): 
    return render_template('tienda.html') #, data=data, page=page,total_pages=total_pages

@app.route('/login')
def login():
    return render_template('login.html')
    
if __name__ == '__main__':
    app.run(debug=True)