from flask import  Flask, render_template, jsonify, request, session
from flask_paginate import Pagination,get_page_args
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

#Extracting Info from the .env file
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY') #Secret Key for the session
uri = os.getenv('MONGO_URI') #Uri for the mongo DB

# Create a new client and connect to the server
client = MongoClient(uri)
db = client.get_database('tienda-uruloki')  # Replace with your database name

#Google API Key for the maps
GOOGLE_API_KEY = os.getenv('GAPIKEY')

# Number of results per page
RESULTS_PER_PAGE = 12

# Set the default folder of templates
app.template_folder = "Templates"

# Function to generate a unique username
def generate_username():
    collection = db.get_collection('Cliente')
    # Retrieve the current count from the database
    count = collection.count_documents({})
    usercode = f'CLI{str(count).zfill(3)}'
    
    # Check if the generated username is unique
    if not collection.find_one({'codigo-cliente': usercode}):
        return usercode
    else:
        raise Exception("Failed to generate a unique username")

# Function to generate a unique inventory code
def generate_inventory_code(gametype):
    collection = db.get_collection('Inventario')
    # Retrieve the current count from the database
    count = collection.count_documents({})
    if gametype == "Juego de Mesa":
        invcode = f'JDM{str(count).zfill(3)}'
    else:
        invcode = f'ACC{str(count).zfill(3)}'
    
    # Check if the generated inventory code is unique
    if not collection.find_one({'Codigo': invcode}):
        return invcode
    else:
        raise Exception("Failed to generate a unique inventory code")
        
def split_players(players):
    x, y = players.split('-')
    return int(x),int(y)

@app.route('/')
def home():
    collection = db.get_collection('Inventario')  # Replace with your collection name
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

#ENDPOINT OF INVENTARIO
@app.route('/inventario')
def inventario():
    collection = db.get_collection('Inventario')
    productos = list(collection.find())
    return render_template('inventario.html', productos=productos)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    price_unitary = request.form.get('price_unitary')

    if 'shopping_cart' not in session:
        session['shopping_cart'] = {}

    if product_id in session['shopping_cart']:
        session['shopping_cart'][product_id]['quantity'] += 1
    else:
        session['shopping_cart'][product_id] = {
            "product_name": product_name,
            "quantity": 1,
            "price_unitary": price_unitary
        }

    session.modified = True
    return jsonify(success=True)

@app.route('/get_cart_items', methods=['GET'])
def get_cart_items():
    return jsonify(session.get('shopping_cart', {}))

@app.route('/upload', methods=['POST'])
def upload_file():
    collection = db.get_collection('Inventario')
    
    name = request.form['name']
    typegame = request.form['type']
    price = request.form['price']
    players = request.form['players']
    quantity = request.form['quantity']
    details = request.form['details']
    image = request.files['image']
    
    #Split the values of players
    min_players, max_players = split_players(players)
    
    #Save the image in a directory
    if not os.path.exists('gameimages'):
        os.makedirs('gameimages')
    filename = secure_filename(image.filename)

    #Generate the inventory code
    invcode = generate_inventory_code(typegame)
    data = {
        "Codigo": invcode,
        "Imagen": filename,
        "Nombre": name,
        "Tipo": typegame,
        "Detalles": details,
        "Precio": float(price),
        "Stock": int(quantity),
        "Descuento": False,
        "Precios-descuento": [
            0
        ],
        "jugadoresminimos": int(min_players) ,
        "jugaodresmaximos": int(max_players) ,
    }

    productoagregado = collection.insert_one(data)

    if productoagregado.acknowledged == 1:
        image.save(os.path.join('gameimages', filename))
        return jsonify(
            {
                "message": "Producto agregado",
                "code": invcode
                })
    else:
        return jsonify({"message": "No se pudo agregar el producto"})

@app.route('/panel')
def panel():
    return render_template("paneldecontrol.html")
    
@app.route('/eventos')
def eventos():
    return render_template("eventos.html")

#ENDPOINT DE CLIENTES
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    collection = db.get_collection('Cliente')
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
            'nombre-completo': [first_name, last_name
            ]   
        } 

        # Insert the data into the MongoDB collection
        collection.insert_one(customer_data)
    username = generate_username()
    
    return render_template("clientes.html",username=username)

@app.route('/search', methods=['GET'])
def search_customer():
    collection = db.get_collection('Cliente')
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
        return jsonify({"message": "Cliente no encontrado"})

@app.route('/update', methods=['PUT'])
def update_customer():
    collection = db.get_collection('Cliente')
    credito = request.form.get('credito')
    nombre_completo = request.form.get('nombre_completo')
    if nombre_completo:
        # Split the nombre_completo string into first and last name variables
        first_name, last_name = nombre_completo.split(',', 1)
    else:
        # Handle the case where nombre_completo is not provided
        first_name = ''
        last_name = ''
    codigo = request.args.get('codigo')
    
    # Find the customer to update
    query = {'codigo-cliente': codigo}
    customer = collection.find_one(query)
    
    if customer:
        
        if nombre_completo:     
            # Define the new values for the customer
            new_values = {'$set': {'nombre-completo.0':first_name,'nombre-completo.1':last_name,'credito':credito }}
            
            # Update the customer's information
            result = collection.update_one(query, new_values)
            
            # Check if the update was successful
            if result.modified_count == 1:
                return jsonify({"message": "Actualizado"})
            else:
                return jsonify({"message": "No se pudo actualizar"})
        else:
            return jsonify({"message": "Nombre no valido"})
        
    else:
        return jsonify({"message":"Cliente no encontrado"})

        
if __name__ == '__main__':
    app.run(debug=True)