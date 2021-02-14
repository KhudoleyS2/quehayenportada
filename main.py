from flask import Flask
from flask import render_template
import json

app = Flask(__name__)



# Rutas
@app.route('/')
def index():
    with open('./scraper/datos.json','r') as json_file:
        data = json.load(json_file)
    
    return render_template('index.html',data=data)



if __name__=="__main__":
    app.run(debug=True)