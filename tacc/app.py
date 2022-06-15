from flask import Flask, flash, redirect, render_template, \
     request, url_for, jsonify
import pickle
import sqlite3
import numpy as np
import pandas as pd
import json


app = Flask(__name__)

# listas para formulario
listaTipos = [{"name":"House"}, {"name":"Apartment"}, {"name":"Land"}]
listaTiposD3 = [{"name":"casas"}, {"name":"departamentos"}, {"name":"terrenos"}]
listaEntidades = [{'name':'Aguascalientes'}, {'name':'Baja California'}, {'name':'Baja California Sur'}, {'name': 'Campeche'},
                    {'name':'Chiapas'}, {'name': 'Chihuahua'}, {'name': 'Ciudad de México'}, {'name': 'Coahuila de Zaragoza'},
                    {'name':'Colima'}, {'name': 'Durango'}, {'name': 'Guanajuato'}, {'name': 'Guerrero'}, {'name': 'Hidalgo'},
                    {'name': 'Jalisco'}, {'name':'Michoacán de Ocampo'}, {'name': 'Morelos'}, {'name': 'México'},
                    {'name': 'Nayarit'}, {'name': 'Nuevo León'}, {'name':'Oaxaca'}, {'name': 'Puebla'}, {'name': 'Querétaro'},
                    {'name': 'Quintana Roo'}, {'name': 'San Luis Potosí'}, {'name':'Sinaloa'}, {'name': 'Sonora'}, 
                    {'name': 'Tabasco'}, {'name': 'Tamaulipas'}, {'name': 'Tlaxcala'}, {'name':'Veracruz de Ignacio de la Llave'}, 
                    {'name': 'Yucatán'}, {'name': 'Zacatecas'}]
listaBanos = [{'name':'1'}, {'name':'1.5'},{'name':'2'},{'name':'2.5'},{'name':'3'},{'name':'3.5'},{'name':'4'},{'name':'4.5'},{'name':'5'},{'name':'5.5'}]
listaParking = [{'name':'1'}, {'name':'2'},{'name':'3'},{'name':'4'},{'name':'5'},{'name':'6'},{'name':'7'},{'name':'8'}]
colsCSV = ['tipo', 'entidad', 'municipio_x', 'precio', 'predPrices', 'diffPrices', 'percentDiff','m2Terreno','m2Construccion', 'estacionamientos', 'Banos', 'antiguedad']
colsDB = ",".join(colsCSV)

#2. Declare data stores
class DataStore():
    entidadD3=None
    typeD3=None
    tablaD3=None
data=DataStore()


# def get_db_connection():
#     # connect to database
#     conn = sqlite3.connect('./Resources/finalData.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# def getData(tipo, entidad):
#     if tipo == 'House':
#         tipo2 = 'Casas'
#     elif tipo == 'Apartment':
#         tipo2 = 'Departamentos'
#     else:
#         tipo2 = 'Terrenos'
#     entidad = f'{entidad}'
#     query = f"""SELECT {colsDB} FROM {tipo2} WHERE entidad= '{entidad}' ORDER BY percentDiff DESC, precio DESC LIMIT 20"""
#     conn = get_db_connection()
#     #data = conn.execute(query).fetchall()
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     data = df.to_json(orient="records")
#     data = json.dumps(data)
#     #save to datastore
#     data.tablaD3 = json.loads(flare)
#     #Save to temporary variable
#     tabla=data.tablaD3
#     return tabla

def getDataCsv():
    tipos = ['casas', 'departamentos', 'terrenos']
    entidades = [x['name'] for x in listaEntidades]
    # if tipo == 'House':
    #     tipo2 = 'casas'
    # elif tipo == 'Apartment':
    #     tipo2 = 'departamentos'
    # else:
    #     tipo2 = 'terrenos'
    # read csv
    df = pd.read_csv('./tacc/Resources/inmueblesFinalData.csv', encoding='utf-8-sig')
    #create empty df
    dfJson = pd.DataFrame(columns = colsCSV)
    #get the top 20 results for tipo and entidad
    for tipo in tipos:
        for entidad in entidades:
            dftipo = df.loc[(df.tipo ==tipo) & (df.entidad==entidad), colsCSV].sort_values(by=['percentDiff'])
            dftipo = dftipo.iloc[:20,]
            dfJson = dfJson.append(dftipo)
    # change format for visualization
    dfJson['precio'] = dfJson['precio'].map("{:,}".format)
    dfJson['predPrices'] = dfJson['predPrices'].map("{:,}".format)
    dfJson['diffPrices'] = dfJson['diffPrices'].map("{:,.0f}".format)
    dfJson['percentDiff'] = dfJson['percentDiff'].map("{:.2f}".format)
    dfJson['m2Terreno'] = dfJson['m2Terreno'].map("{:,}".format)
    dfJson['m2Construccion'] = dfJson['m2Construccion'].map("{:,}".format)
    # convert to json
    flare = dfJson.to_json(orient="records")
    data.tablaD3 = json.loads(flare)
    datos = data.tablaD3
    return datos

# Seleccion de modelo
def modelSel(tipo):
    if tipo == 'House':
        model = pickle.load(open('./tacc/modeloCasas.pkl','rb'))
    elif tipo == 'Apartment':
        model = pickle.load(open('./tacc/modeloDepas.pkl','rb'))
    else:
        model = pickle.load(open('./tacc/modeloTerrenos.pkl','rb'))
    return model

@app.route('/',methods=["GET","POST"])
def base():
    resultado = ""
    # entidadD3 = request.form.get('estadoSelD3', 'Ciudad de México')
    # typeD3 = request.form.get('typeD3', 'House')
    datos = getDataCsv()
    # data.tablaD3 = datos
    # data.entidadD3 = entidadD3
    # data.typeD3 = typeD3
    return render_template('formPricing.html', listaTipos=listaTipos, listaEntidades=listaEntidades, listaTiposD3=listaTiposD3, listaBanos=listaBanos, listaParking=listaParking, resultado=resultado, datos=datos)

@app.route("/formPricing/" , methods=['GET', 'POST'])
def formPricing():
    # Get data from form
    if request.method == 'POST':
        tipo = request.form.get('type')
        estadoSelecc = request.form.get('estadoSelecc')
        m2Construccion = float(request.form['m2Construccion'])
        m2Terreno = float(request.form['m2Terreno'])
        banos = float(request.form['banos'])
        estacionamientos = int(request.form['estacionamientos'])
        antiguedad = float(request.form['antiguedad'])

    # elaborate predicted array based on type
    if tipo == 'House':
        predictArray = [np.log(m2Construccion), np.log(m2Terreno), banos, estacionamientos, antiguedad]
        estados = ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
       'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila de Zaragoza',
       'Colima', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco',
       'Michoacán de Ocampo', 'Morelos', 'México', 'Nayarit', 'Nuevo León',
       'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí',
       'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala',
       'Veracruz de Ignacio de la Llave', 'Yucatán', 'Zacatecas']
        asset = 'house'
    elif tipo == 'Apartment':
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
    
    # asigna 1 al estado seleccionado y 0 a los demás 
    for i in estados:
        if estadoSelecc == i:
            predictArray.append(1)
        else:
            predictArray.append(0)
    # array final
    predictArray = [predictArray]

    #selecciona modelo y 
    model = modelSel(tipo)
    predictedValue = round(np.exp(model.predict(predictArray))[0]/1000000,2)*1000000
    result = f"According to our model the predicted price for your {asset} is: $" + "{:,.0f}".format(predictedValue)

    return render_template('formPricing.html/', listaTipos=listaTipos, listaEntidades=listaEntidades, listaTiposD3=listaTiposD3, resultado=result)

@app.route("/get-data", methods=['GET', 'POST'])
def returnProdData():
    f = data.tablaD3
    return jsonify(f)

if __name__=='__main__':
    app.run(debug=True)
    # app.run(debug=True)