from flask import  Flask, render_template, request, jsonify
from flask_paginate import Pagination,get_page_args
import pyodbc
import requests

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'server': 'uruloki.cxwhbhuw13bl.us-east-2.rds.amazonaws.com',
    'database': 'Uruloki',
    'user': 'admin',
    'password': 'minionswar2',
    'port': 1433  # Specify the port here
}

RESULTS_PER_PAGE = 12 # Number of results per page

GOOGLE_API_KEY = 'AIzaSyBpYcf0TjJrOI2Aw3UJ5_KLDJQewicguEw'

app.template_folder = "Templates"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Torneos')
def torneos():
    return render_template('torneos.html')

@app.route('/Tienda')
def tienda(): 
    page = request.args.get('page', 1, type=int)

    conn = pyodbc.connect(
        f"DRIVER=ODBC Driver 17 for SQL Server;"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['user']};"
        f"PWD={db_config['password']};"
        f"PORT={db_config['port']}"
    )

    cursor = conn.cursor()

    query = """
        SELECT *
        FROM (
            SELECT *, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS row_num
            FROM OscarPrueba
        ) AS t
        WHERE row_num BETWEEN ? AND ?
    """
    
    start_row = (page - 1) * RESULTS_PER_PAGE + 1
    end_row = start_row + RESULTS_PER_PAGE - 1
    
    cursor.execute(query, (start_row, end_row))
    data = cursor.fetchall()

    # Calculate total number of pages
    cursor.execute("SELECT COUNT(*) FROM OscarPrueba")
    total_rows = cursor.fetchone()[0]
    total_pages = (total_rows + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
    
    conn.close()

    return render_template('tienda.html', data=data, page=page,total_pages=total_pages)
    
if __name__ == '__main__':
    app.run(debug=True)