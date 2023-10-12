from flask import  Flask, render_template, jsonify, request
from flask_paginate import Pagination,get_page_args
from pymongo import MongoClient
import random, string

app = Flask(__name__)

# MongoDB connection
uri = "mongodb+srv://xchar:minionswar2@cluster0.2loqznr.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
db = client.get_database('tienda-uruloki')  # Replace with your database name


RESULTS_PER_PAGE = 12 # Number of results per page

GOOGLE_API_KEY = 'AIzaSyBpYcf0TjJrOI2Aw3UJ5_KLDJQewicguEw'

app.template_folder = "Templates"

# Function to generate a unique username
def generate_username():
    while True:
        collection = db.get_collection('clientes')
        # Generate a random 5-digit number as a string
        random_numbers = ''.join(random.choices(string.digits, k=5))
        usercode = f'CLI{random_numbers}'
        
        # Check if the generated username is unique
        if not collection.find_one({'codigo-cliente':usercode}):
            return usercode

@app.route('/')
def home():
    collection = db.get_collection('juegos-de-mesa')  # Replace with your collection name
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

@app.route('/panel')
def panel():
    return render_template("paneldecontrol.html")
    
@app.route('/eventos')
def eventos():
    return render_template("eventos.html")

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    collection = db.get_collection('clientes')
    if request.method == 'POST':
        # Get data from the form
        codigocliente = request.form['username']
        credit = request.form['credit']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Create a dictionary with the data
        customer_data = {
            'codigo-cliente': codigocliente,
            'credito': credit,
            'nombre-completo': [first_name,last_name]   
        } 

        # Insert the data into the MongoDB collection
        collection.insert_one(customer_data)
    username = generate_username()
    
    return render_template("clientes.html",username=username)

@app.route('/search', methods=['GET'])
def search_customer():
    collection = db.get_collection('clientes')
    codigo = request.args.get('codigo')

    # Use your MongoDB collection to search for the customer data
    # Replace 'your_collection' with your actual collection name
    customer_data = collection.find_one({"codigo-cliente": codigo})

    if customer_data:
        # Return the customer data as JSON
        return jsonify({
            "nombre": customer_data.get("nombre-completo"),
            "credito": customer_data.get("credito")
        })
    else:
        # Return an empty JSON object if not found
        return jsonify({})

@app.route('/update', methods=['PUT'])
def update_customer():
    collection = db.get_collection('clientes')
    credito = request.args.get('credito')
    nombre_completo = request.args.get('nombre_completo')
    codigo = request.args.get('codigo')
    
    # Find the customer to update
    query = {'codigo-cliente': codigo}
    customer = collection.find_one(query)
    
    if customer:
        
        if nombre_completo:
            nombre, apellido = nombre_completo.split(',',1)
        
            # Define the new values for the customer
            new_values = {'$set': {'nombre-completo':[nombre,apellido],'credito':credito }}
            
            # Update the customer's information
            result = collection.update_one(query, new_values)
            
            # Check if the update was successful
            if result.modified_count == 1:
                return 'Customer information updated successfully'
            else:
                return 'An error occurred while updating the customer information'
        else:
            return 'Full name not provided'
        
    else:
        return 'Customer not found'

        
if __name__ == '__main__':
    app.run(debug=True)