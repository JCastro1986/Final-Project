from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bd8e93b0aaa86df4abc6288a59c3847254b6c43320b99f2a'

def modelSel(tipo):
    if tipo == 'Casas':
        model = pickle.load(open('modeloCasas.pkl','rb'))
    elif tipo == 'Departamentos':
        model = pickle.load(open('modeloDepas.pkl','rb'))
    else:
        model = pickle.load(open('modeloTerrenos.pkl','rb'))
    return model

def get_db_connection():
    # connect to database
    conn = sqlite3.connect('./Resources/finalData.db')
    conn.row_factory = sqlite3.Row
    return conn


def getData(tipo):
    query = 'SELECT * FROM ' + tipo + " LIMIT 10"
    conn = get_db_connection()
    #data = conn.execute(query).fetchall()
    df = pd.read_sql_query(query, conn)
    data = df.to_json(orient="records")
    # data = df.to_html()
    conn.close()
    return data

@app.route('/')
def index():
     return render_template('base.html')


@app.route("/form")
def form():
    return render_template("form.html")

@app.route('/form/', methods=('GET', 'POST'))
def predict():
    # Get data from form
    if request.method == 'POST':
        estadoSelecc = request.form['estadoSelecc']
        tipo = request.form['type']
        m2Construccion = float(request.form['m2Construccion'])
        m2Terreno = float(request.form['m2Terreno'])
        banos = float(request.form['banos'])
        estacionamientos = int(request.form['estacionamientos'])
        antiguedad = float(request.form['antiguedad'])

    # elaborate predicted array based on type
    if tipo == 'Casas':
        predictArray = [np.log(m2Construccion), np.log(m2Terreno), banos, estacionamientos, antiguedad]
        estados = ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
       'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila de Zaragoza',
       'Colima', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco',
       'Michoacán de Ocampo', 'Morelos', 'México', 'Nayarit', 'Nuevo León',
       'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí',
       'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala',
       'Veracruz de Ignacio de la Llave', 'Yucatán', 'Zacatecas']
        asset = 'house'
    elif tipo == 'Departamentos':
        predictArray = [m2Construccion, banos, estacionamientos, antiguedad]
        estados = ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Chiapas', 'Chihuahua', 'Ciudad de México', 
            'Coahuila de Zaragoza','Colima', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán de Ocampo', 
            'Morelos', 'México', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 
            'Sinaloa','Tabasco', 'Tamaulipas', 'Veracruz de Ignacio de la Llave', 'Yucatán']
        asset = 'apartment'
    else:
        predictArray = [m2Terreno]
        estados = ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
       'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila de Zaragoza',
       'Colima', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco',
       'Michoacán de Ocampo', 'Morelos', 'México', 'Nayarit', 'Nuevo León',
       'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí',
       'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala',
       'Veracruz de Ignacio de la Llave', 'Yucatán', 'Zacatecas']
        asset = 'land'

    for i in estados:
        if estadoSelecc == i:
            predictArray.append(1)
        else:
            predictArray.append(0)

    predictArray = [predictArray]
    
    model = modelSel(tipo)
    predictedValue = round(np.exp(model.predict(predictArray))[0]/1000000,2)*1000000

        # if not type:
        #     flash('Title is required!')
        # elif not content:
        #     flash('Content is required!')
        # else:
        #     messages.append({'title': title, 'content': content})
        #     return redirect(url_for('index'))
    result = f"Predicted price for your {asset} is: $" + "{:,.0f}".format(predictedValue)

    data = getData(tipo)

    return render_template('index.html', result=result, data=data)

if __name__ == "__main__":
   app.run()