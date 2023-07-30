from flask import  Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Torneos')
def torneos():
    return render_template('torneos.html')

@app.route('/Tienda')
def tienda():
    return render_template('tienda.html')

if __name__ == '__main__':
    app.run(debug=True)