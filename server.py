# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 20:50:14 2023

@author: Seba
"""

import subprocess
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from itertools import product

app = Flask(__name__)
CORS(app) 

secuencia_letras_patente = ['B','C','D','F','G','H','J','K','L','P','R','S','T','V','W','X','Y','Z']

#FALTA IMPLEMENTAR LA ITERACION SOBRE LAS LETRAS, ACTUALMENTE ES MANUAL
letra_buscar = 'L'
uri_datos = r"..."
cargar_cache = False
patentes_cache = []


if cargar_cache:
    with open(uri_datos + letra_buscar.lower() + '/no_ok.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            patentes_cache.append(x)
else:
    patentes_cache = [letra_buscar + ''.join(combs) for combs in product(secuencia_letras_patente, repeat = 3)]

patentes_en_busqueda = []
patentes_fallida = []


#AGREGAR UN METODO PARA RETOMAR LAS PATENTES QUE QUEDEN EN BUSQUEDA
@app.route('/endpoint', methods=['GET','POST'])
def handle_extension_request():
       
    if request.method == 'GET':
        patente_enviar = patentes_cache[0]
        patentes_en_busqueda.append(patente_enviar)
        patentes_cache.remove(patente_enviar)
                
        return patente_enviar
    
    if request.method == 'POST':
        #AGREGAR VALIDACION DE QUERY VACIA, PUEDEN LLEGAR PATENTES QUE NO TENGAN DATOS
        #AGREGAR ALGO PARA SACAR LAS PATENTES EN BUSQUEDA SI DEVUELVEN RESULTADO POSITIVO
        #AGREGAR TRY ACA EN CASO DE PROBLEMAS, DEVOLVER UN 400-500 O PARECIDO
        with open(uri_datos + letra_buscar.lower() + '/ok.txt', 'a+') as f:
            for fila in request.get_json():
                f.write(request.headers['patente'] + '\t' +
                        fila['Patente']  + '\t' +
                        fila['Tipo'] + '\t' +
                        fila['Marca'] + '\t' +
                        fila['Modelo'] + '\t' +
                        fila['Rut'] + '\t' +
                        fila['NroMotor'] + '\t' +
                        fila['Año'] + '\t' +
                        fila['Propietario'] + '\t'                                                 
                        + '\n')
        
        
        
        return "Success", 201
   

def run_flask_server():
    app.run(host='127.0.0.1', port=5000)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    #AGREGAR PARA TOMAR LAS PATENTES QUE QUEDEN EN BUSQUEDA/INCOMPLETAS
    try:
        if(len(patentes_cache) > 0):
                with open(uri_datos + letra_buscar.lower() + '/no_ok.txt', 'w+') as f:
                    for patente in patentes_cache:        
                        f.write("%s\n" % patente)
    except Exception as e:
        print(e)
    finally: 
        shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_server)
    flask_thread.start()
    
    # chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    # url_to_open = "..."
    # subprocess.run([chrome_path, url_to_open, '--profile-directory="Profile 4"'])




# //EMPEZAR A CALCULAR EN BASE A LARGO DEL INPUT TALVEZ
# function calcular_siguiente_letra(letra){
#     let index_letra = secuencia_letras_patente.indexOf(letra)
#     return secuencia_letras_patente[index_letra+1]
# }

# function calcular_patente(){
#     for(var  i = patente_calcular.length - 1; i >= 0; i--){ 
#         let letra = patente_calcular[i]
#         if(letra == 'Z'){
#             patente_calcular[i] = 'B'
#             continue;
#         }
#         patente_calcular[i] = calcular_siguiente_letra(letra)
#         break;

#     }
#     return patente_calcular.join('') + '%'
# }
