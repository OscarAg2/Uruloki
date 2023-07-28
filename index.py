from flask import  Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Torneos')
def torneos():
    return "Torneos"

@app.route('/Tienda')
def tienda():
    return "Tienda"

if __name__ == '__main__':
    app.run()