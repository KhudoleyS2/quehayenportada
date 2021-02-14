from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)


#Simple Sqlite3 funcionalidad ___________________
from flask import g

DATABASE = './scraper/sqlite.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
# ________________________________________________




# Rutas
@app.route('/')
def index():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM periodicos ORDER BY fecha DESC')
    data = cursor.fetchall()
    
    return render_template('index.html',data=data)



if __name__=="__main__":
    app.run(debug=True)