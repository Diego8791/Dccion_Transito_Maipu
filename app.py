#!/usr/bin/env python
'''
API Gestión
---------------------------
Autor: Diego Farias
Version: 1.0

Descripcion:
Se utiliza en Direción de Tránsito de Maipú

Ejecución: Lanzar el .........


'''

__author__ = "Diego Farias"
__email__ = "dfarias8791@gmail.com"
__version__ = "1.0"


from flask import Flask, request, jsonify, render_template, Response, redirect, url_for, session, flash
import query_acc_db
import my_geo
import mysql.connector
import traceback
import numpy as np
import io
import estadisticas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import folium
import collections


app = Flask(__name__)

app.secret_key = 'tuiejfllkkejafljvu8092308985jlfalaji'

# conn = mysql.connector.connect(user='direcciontransit', password='0710princesafiona', host='direcciontransitomaipu2020.mysql.pythonanywhere-services.com', database='direcciontransit$dccion_transito_db')


#-----------------------CONTROL DE USUARIOS (SIMPLE)-----------------------------------------

@app.route('/')
def index():
    '''
    Ingresar en formulario index
    '''
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Obtener datos de usuario para validación. Consultar datos en base de datos users_db
    '''
    if request.method == 'GET':
        try:
            conn = mysql.connector.connect(user='username', password='password', host='localhost', database='users_db') # establecer la conección
            cursor = conn.cursor()                                                                                      # crear objeto cursor usando el método cursor() 
            username = []                                                                                               # lista para pasar los nombres de usuarios al formulario login_form.html
            cursor.execute("SELECT name FROM users")
            for name in cursor:                                                                                          # bucle que lee los nombres de los usuarios
                username.append(name)
            conn.close()                                                                                                 # cerrar la conección
            return render_template('index.html', username=username)                                                      # retornar formulario index.html
        except:
            return jsonify({'trace': traceback.format_exc()})
    if request.method == 'POST':
        # post
        try:
            # Recibir los datos desde el formulario index.html
            name = str(request.form['username'])
            email = str(request.form['email'])
            password = str(request.form['password'])
            # Obtener datos de base de datos
            conn = mysql.connector.connect(user='username', password='password', host='localhost', database='users_db') # Abrir base de datos users_db
            cursor = conn.cursor()                                                                                      # crear objeto cursor usando el método cursor()
            sql = "SELECT e_mail, password FROM users WHERE name = (%s)"                                                # leer password del usuario
            cursor.execute(sql, [name])
            data_user = (cursor.fetchone())
            conn.close()                                                                                                 # Cierre de cenexión
            # validar usuario
            if data_user[0] == email and data_user[1] == password:                                                       # valida e-mail y password
                session['user'] = name                                                                                  # validación correcta
                return redirect(url_for('user'))
            else:
                flash('Usuario Incorrecto')                                                                                # mensaje de error
                return redirect(url_for('login'))                                                                          # validación icorrecta
        except:
            return jsonify({'trace': traceback.format_exc()})


@app.route("/user/")
def user():
    '''
    Validar usuario
    '''
    try:
        if 'user' in session:
            name = session['user']                    # esta variable no tiene un uso posterior
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route('/logout/')
def logout():
    '''
    Cerrar sesión
    '''
    try:
        session.clear()                                                                                                 # Eliminar sesión
        flash('¡Sesión cerrada!')                                                                                       # Mensaje de sesión cerrada
        return redirect(url_for('login'))
    except:
        return jsonify({'trace': traceback.format_exc()})


# ----------------------------------------HOME-----------------------------------------------------

@app.route("/home/")
def home():
    '''
    Ingresar a página principal
    '''
    try:
        if 'user' in session:
            return render_template('home.html')
    except:
        return jsonify({'trace': traceback.format_exc()})


# -----------------------------------  ACCIDENTOLOGIA -----------------------------------------------

@app.route("/accidentologia/")
def accidentologia():
    '''
    Ingresar a principal de accidentología
    '''
    try:
        if 'user' in session:
            return render_template('accidentologia.html')                                               # ingresar a formulario accidentología.html
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/accidentologia/insert_acc_gral_data/", methods=['GET', 'POST'])
def insert_data():
    '''
    Ingresar datos generales del módulo de accidentología
    '''
    try:
        if 'user' in session:
            if request.method == 'GET':
                
                # Abrir base de datos
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                cursor = conn.cursor()                                                                                                 # crear objeto cursor usando el método cursor()
                # leer tipos de accidentes
                tipo_acc = []
                sql = "SELECT id, acc_tipo FROM tipo"
                cursor.execute(sql)
                for tipo in cursor:                                                                                                      # for que leer los tipos de accidentes
                    tipo_acc.append(tipo)
                # Cierre de conexión
                conn.close()

                return render_template("insert_gral_data_acc_db.html", tipo_acc=tipo_acc)                                                # abrir formulario

            if request.method == 'POST':                                                                                                # recibir datos de formulario
                n_acc = int(request.form['n_acc'])
                fecha = request.form['fecha']
                hora = request.form['hora']
                direccion = request.form['direccion']
                distrito = request.form['distrito']
                perito = int(request.form['perito'])
                tomado_en = int(request.form['tomado_en'])
                tipo = int(request.form['tipo'])
                con_sin_les = int(request.form['con_sin_les'])
                obs = request.form['obs']
				# enviar datos para geolocalización
                adress = direccion + ', ' + distrito + ', Maipú, Mendoza, Argentina'                                                       # crear string para georeferenciación
                lat, lng = my_geo.adress_locations(adress)                                                                                 # obterner latitud y longitud
                # Abrir base de datos users_db
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                cursor = conn.cursor()
				# cambiar nombre de distrito por id de distrito
                sql = 'SELECT id FROM distritos_maipu WHERE n_distritos_maipu = (%s)'                                                       # obtener id de distrito
                cursor.execute(sql, [distrito])
                distrito = cursor.fetchone()[0]
				# formar lista de registro de datos generales
                data = [n_acc, fecha, hora, direccion, distrito, perito, tomado_en, tipo, con_sin_les, obs, lat, lng]                        # registrar registro en base de datos accidentologia_db
                # registrar lista en base de datos
                sql = '''INSERT INTO datos_grales_acc
                            (n_acc, fecha, hora, direccion, fk_distrito_maipu_id, fk_perito_id,
                            fk_tomado_en_id, fk_tipo_id, fk_lesiones_id, obs, latitud, longitud)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cursor.execute(sql, data)
                conn.commit()
                # cerrar conexion
                conn.close()
                # mensaje confirmación de registro válido
                flash('¡BUEN TRABAJO!... se han cargado los datos generales!')                                                                                       # Mensaje de sesión cerrada
                return redirect(url_for('insert_data'))
    except:
        # mensaje de error al registrar en base de datos
        flash('¡ATENCIÓN!... Se ha producido un error al registrar los datos generales') 
        return redirect(url_for('insert_data'))    


@app.route("/accidentologia/insert_participe/", methods=['GET', 'POST'])
def insert_participe_accidentologia():
    '''
    Ingresar partícipes de accidentes
    '''
    if 'user' in session:
        if request.method == 'GET':
            return render_template("insert_participant_acc.html") 

        if request.method == 'POST':
            n_acc = int(request.form['n_acc'])
            dtv = request.form['dtv']
            n_doc = request.form['n_doc']
            categorias = request.form.getlist('categorias')
            categorias = "".join(categorias)                            #transformar la lista en string
            test_alcoholemia = request.form['test_alcoholemia']
            if test_alcoholemia == '':                                  #salvar cuando no se ha tomado alcoholemia
                test_alcoholemia = 'no se realizó'
            f_etaria = int(request.form['f_etaria'])
            dominio = request.form['dominio']

            try:
                # Abrir base de datos dccion_transito_db
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                cursor = conn.cursor()
				# consultar id de patente
                sql = 'SELECT id FROM rodado WHERE patente = (%s)'                                                                    # Obtener id de dominio de vehículo
                cursor.execute(sql,[dominio])
                id_patente = cursor.fetchone()[0]
				# consultar id de numero de documento
                sql = 'SELECT id FROM padron WHERE n_doc = (%s)'                                                                       # obtener id de dni
                cursor.execute(sql,[n_doc])
                id_n_doc = cursor.fetchone()[0]
                # Verificar que el numero de documento no esté ya cargado en el numero de accidente
                sql = 'SELECT fk_n_doc_id FROM participe WHERE n_acc = (%s)'
                cursor.execute(sql,[n_acc])
                resultado = cursor.fetchall()
                # validación de numero de documento para el número de accidente
                clave = False
                for fk_n_doc_id in resultado:
                    if id_n_doc == fk_n_doc_id[0]:
                        clave = True
                if clave == False:
                    data = [n_acc, dtv, id_n_doc, categorias, f_etaria, id_patente, test_alcoholemia]
                    sql = '''
                            INSERT INTO participe
                                (n_acc, dtv, fk_n_doc_id, lic_conducir, fk_fran_etaria, fk_rodado_id, alcoholemia)
                                VALUES (%s,%s,%s,%s,%s,%s,%s)
                            '''
                    cursor.execute(sql, data)
                    conn.commit()
                    conn.close()
                    # mensaje de validación satisfactoria
                    flash('¡BUEN TRABAJO!... Partícipe registrado con éxito')                                                                                # mensaje de error
                    return redirect(url_for('insert_participe_accidentologia'))  
                else:
					# mensaje de que el numero de documento ya se encuentra registrado en el accidente
                    flash('¡ATENCIÓN!...El partícipe ya se encuentra registrado en ese accidente')                                                                                # mensaje de error
                    return redirect(url_for('insert_participe_accidentologia'))
            except:
                # mensaje de error al registrar partícipe
                flash('¡ERROR AL REGISTRAR!... no se ha podido ingresar el partícipe')                                                                                # mensaje de error
                return redirect(url_for('insert_participe_accidentologia'))


# --------------------------------------- CONSULTAS ----------------------------------------------------


@app.route("/accidentologia/search_menu/", methods=['GET', 'POST'])
def search_menu():
    '''
    Menu de consultas
    - Buscar por D.N.I.
    - Buscar por dominio
    - Buscar por accidente
    - Buscar por fecha de ocurrencia
    '''
    if 'user' in session:
        try:
            if request.method == "GET":
                # llamar a formulario
                return render_template('search_data_form.html')                                                             # llamar a formulario principal de consultas

            if request.method == "POST":
                # recibir opción desde formulario
                opcion = int(request.form['consulta'])
                if opcion == 1:
                    return redirect(url_for('search_dni'))
                elif opcion == 2:
                    return redirect(url_for('select_dominio'))
                elif opcion == 3:
                    return redirect(url_for('data_acc_search'))
                else:
                    return redirect(url_for('date_search_acc'))
        except:
			# mensaje flash
            flash('¡ATENCION!... se ha producido un error en su seleccion')                                                                                
            return redirect(url_for('search_menu'))


@app.route("/search_dni/", methods=['GET', 'POST'])
def search_dni():
    '''
    Consultar datos por D.N.I.
    '''
    if 'user' in session:
        try:
            if request.method == "GET":
                datos_padron = ()
                datos_acc_list = ()
                return render_template('search_dni_form.html', data=datos_padron, datos_acc_list=datos_acc_list)

            if request.method == "POST":
                n_dni = request.form['n_dni']
                datos_padron, datos_acc_list = query_acc_db.padron_dni(n_dni)
                return render_template('search_dni_form.html', data=datos_padron, datos_acc_list=datos_acc_list)
        except:    
			# mensaje de que no está registrado el D.N.I.
            flash('D.N.I. no registrado')
            return redirect(url_for('search_dni'))                                                                
        

@app.route("/select_dominio/", methods=['GET', 'POST'])
def select_dominio():
    '''
    Consultar datos por dominio
    '''
    if 'user' in session:
        if request.method == "GET":
            datos_dominio = ()
            return render_template('search_dominio_form.html', data=datos_dominio)

        if request.method == "POST":
            dominio = request.form['dominio']
            datos_dominio, datos_acc_list = query_acc_db.search_dominio(dominio)
			# Evaluar el resultado de la busqueda
            if datos_dominio is not None:
                return render_template('search_dominio_form.html', data=datos_dominio, datos_acc=datos_acc_list)
            else:          
                # mensaje flash
                flash('Dominio no registrado')                                                                               
                return redirect(url_for('select_dominio'))                                        


@app.route("/accidentologia/data_acc_search/", methods=['GET', 'POST'])
def data_acc_search():
    '''
    Consultar datos por numero de accidente
    '''
    if 'user' in session:
        if request.method == 'GET':				
			# inicia listas necesarias
            datos_acc = []
            participe = []
			# latitud y longitud de inicio
            lat_long = [-32.9727, -68.8119]
            return render_template('search_data_acc_form.html', datos_acc=datos_acc, participe=participe, lat_long=lat_long)
    
        if request.method == 'POST':
            # inicio de listas necesarias
            datos_acc = []
            participes = []
            lat_long = []
            try:
                n_acc = int(request.form['n_acc'])
                # consulta de datos de accidente 
                datos_acc, participes, lat_long = query_acc_db.data_search_acc(n_acc)
                return render_template('search_data_acc_form.html', datos_acc=datos_acc, participes=participes, lat_long=lat_long)
            except:
				# mensaje flash
                flash('¡ATENCION!... Accidente no encontrado')
                return redirect(url_for('data_acc_search'))                                                                


@app.route("/accidentologia/date_search/", methods=['GET', 'POST'])
def date_search_acc():
    '''
    Consultar datos generales de accidentes por fecha
    '''
    if 'user' in session:
        if request.method == "GET":
            # iniciar lista necesaria
            data = []
            # llamar a formulario
            return render_template('search_date_acc_form.html', data=data)

        if request.method == 'POST':
            try:
				# recibe fecha de inicio y fin del intervalo
                fecha_inicio = request.form['fecha_inicio']
                fecha_final = request.form['fecha_final']
				# consulta de accidentes entre ambas fechas
                data = query_acc_db.date_search_acc(fecha_inicio, fecha_final)
				# llamar a formulario y pasar lista data
                return render_template('search_date_acc_form.html', data=data)
            except:
				# mensaje flash
                flash('¡ATENCION!... Entre las fechas solicitadas no se encontraron accidentes')
                return redirect(url_for('date_search_acc'))
				

# ----------------------REGISTRAR PERSONAS EN PADRON -----------------------------------


@app.route("/insert_persona/", methods=['GET', 'POST'])
def insert_persona():
    '''
    Ingresar datos de una persona que no se encuentra en base de datos padron_db
    '''
    if 'user' in session:
        try:
            if request.method == "GET":
                # Abrir base de datos
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                cursor = conn.cursor()
                # seleción datos dinámicos de distritos de todo el país
                # crea lista distritos
                sql = "SELECT id, n_distrito FROM distritos"
                cursor.execute(sql)
                distritos = []
                for distrito in cursor:
                    distritos.append(distrito)
                # seleción dinámica de departamentos de Mendoza
                # crea lista departamentos
                sql = "SELECT id, n_departamento FROM departamentos"
                cursor.execute(sql)
                departamentos = []
                for departamento in cursor:
                    departamentos.append(departamento)
                # seleción dinámica de provincias del país
                # crea lista provincias
                provincias = []
                sql = "SELECT id, provincia FROM provincias"
                cursor.execute(sql)
                for provincia in cursor:
                    provincias.append(provincia)
                # seleción dinámica de nacionalidades
                # forma lista nacionalidades
                nacionalidades = []
                sql = "SELECT id, nacionalidad FROM nacionalidades"
                cursor.execute(sql)
                for nacionalidad in cursor:
                    nacionalidades.append(nacionalidad)
                # cerrar conexion
                conn.close()
				# llamar a formulario y pasar listas
                return render_template('insert_persona_form.html', distrit=distritos, dptos=departamentos, nacion=nacionalidades, pcias=provincias)
        except:
			# mensaje flash
            flash('¡ATENCION!... Ha habido un problema al ingresar al formulario')
            return redirect(url_for('insert_persona'))
        
        try:
            if request.method == 'POST':
				# recibir datos de formulario
                nombre = request.form['nombre']
                tipo_dni = request.form['tipo_dni']
                n_doc = int(request.form['n_doc'])
                sexo = request.form['sexo']
                f_nacimiento = request.form['f_nacimiento']
                e_civil = int(request.form['e_civil'])
                cuil = request.form['cuil']
                domicilio = request.form['domicilio']
                distrito = int(request.form['distrito'])
                dpto = int(request.form['depto'])
                pcias = int(request.form['provincias'])
                nacionalidad = int(request.form['nacionalidad'])
                c_postal = request.form['c_postal']
				# formar lista con datos recibidos
                data = [nombre, tipo_dni, n_doc, sexo, f_nacimiento, e_civil, cuil, domicilio, distrito, dpto, pcias, nacionalidad, c_postal]
                # establecer la conección con base de datos
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                cursor = conn.cursor()
                # consulta
                sql = 'SELECT * FROM padron WHERE n_doc = (%s)'
                cursor.execute(sql, [n_doc])
                result = cursor.fetchone()
                # evaluar si el numero de documento ya se encuentra registrado en padron
                if result != None:            
                    flash('¡ATENCIÓN!... Éste D.N.I. ya se encuentra registrado') 
                    return redirect(url_for('insert_persona'))
                else:
                    sql = '''INSERT INTO padron (nombre, tipo_doc, n_doc, sexo, f_nacimiento, e_civil, cuil,
                        domicilio, fk_distrito_id, fk_depto_id, fk_pcia_id, fk_nacion_id, cod_postal)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                    cursor.execute(sql, data)
                    conn.commit()
                    conn.close()
                    flash('¡BUEN TRABAJO!... Datos de persona ingresado con éxito') 
                    return redirect(url_for('insert_persona'))
        except:
			# mensaje flash
            flash('¡ATENCIÓN!... Se produjo un error al registrar')
            return redirect(url_for('insert_persona'))


# ------------------------INGRESAR DE VEHICULOS POR DOMINIO. -----------------------------------------


@app.route("/insert_vehiculo/", methods=['GET', 'POST'])
def insert_vehiculo():
    '''
    Insertar datos de una persona que no se encuentra en base de datos padron_db
    '''
    if 'user' in session:
        try:
            if request.method == "GET":
                # Abrir conexion
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                cursor = conn.cursor()
                # Busqueda dinámica para formulario
				# crear lista marcas
                marcas = []
                cursor.execute("SELECT id, marca FROM marca_rodado")
                for marca in cursor:
                    marcas.append(marca)
				# crear lista modelos
                modelos = []
                cursor.execute("SELECT id, modelo FROM modelo_rodado")
                for modelo in cursor:
                    modelos.append(modelo)
                # cerrar la conexion
                conn.close()
                # llamar a formulario pasando lista para seleccion dinamica
                return render_template('insert_vehiculos_form.html', marcas=marcas, modelos=modelos)
        except:
			# mensaje flash
            flash('¡ATENCION!... Ha habido un problema al ingresar al formulario')
            return redirect(url_for('insert_persona'))
            
        try:
            if request.method == 'POST':
				# recibir datos de formulario
                dominio = request.form['dominio']
                marca = request.form['marca']
                modelo = request.form['modelo']
				# formar lista
                rodado = [dominio, marca, modelo]
                # Abrir conexion
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                cursor = conn.cursor()
                # consulta
                sql = '''
                        INSERT INTO rodado (patente, fk_marca_id, fk_modelo_id)
                        VALUES (%s,%s,%s)
                        '''
                # ejecutar la query
                cursor.execute(sql, rodado)
                conn.commit()
                # cerrar conexion
                conn.close()
                flash('¡BUEN TRABAJO!... Datos de vehículo ingresado con éxito') 
                return redirect(url_for('insert_vehiculo'))
        except:
            flash('¡ATENCIÓN!... Se ha producido un error al registrar el vehículo')
            return redirect(url_for('insert_vehiculo'))


# ------------------------MAPA ACCIDENTOLOGICO -----------------------------------------


@app.route("/accidentologia/mapa/", methods=['GET', 'POST'])
def map():
    '''
    Módulo para formar mapa accidentológico entre dos numeros de accidentes dados.
    '''
    if 'user' in session:
        try:       
            if request.method == 'GET':
				# llamar a formulario 
                return render_template('map_form.html')

            if request.method == 'POST':
				# recibir datos de formulario
                n_inicial = request.form['n_inicial']
                n_final = request.form['n_final']
				# formar lista con numeros de accidentes
                lista_geo = query_acc_db.mapa_accidentologico(int(n_inicial), int(n_final))
				# FORMAR MAPA CON GEOLOCALIZACION DE ACCIDENTES
				# Extraer cuantos accidentes hay por cada localización
                lista_geo = collections.Counter(lista_geo)   
				# extraer el valor mas alto de cantidad de accidentes
                v_max = max([v for k, v in lista_geo.items()])
                some_map = folium.Map(location=[-32.9853509, -68.7877007], zoom_start=15, titles='localización de puntos de accidentes')
				# ubicar accidentes
                for k, v in lista_geo.items():
					# Distribución de accidentes
                    if v < (v_max * 0.3333334) :
                        folium.Circle(k, popop='<i>The Waterfront</i>', radius=30, fill=True, color='green',  tooltip=v).add_to(some_map)
                    elif v >= (v_max * 0.3333334) and v < (v_max * 0.6666667):
                        folium.CircleMarker(k, popop='<i>The Waterfront</i>', radius=30, fill=True, color='orange',  tooltip=v).add_to(some_map)
                    else:
                        folium.CircleMarker(k, popop='<i>The Waterfront</i>', radius=30, fill=True, color='red',  tooltip=v).add_to(some_map)
				# imprimir mapa en pantalla	
                return some_map._repr_html_()
        except:
            flash('¡ATENCIÓN!... Se ha producido un error al imprimir mapa, verifique los numeros de accidentes solicitados')
            return redirect(url_for('map'))
			

# --------------------------------------------ESTADÍSITICAS-------------------------------------------------------


@app.route("/accidentologia/estadisticas/", methods=['GET', 'POST'])
def consultas_criterios():
    '''
    Consultas según diferentes criterios
    '''
    try:
        if 'user' in session:
            if request.method == 'GET':
                # llamar a formulario consultas_form.html
                return render_template('estadisticas_form.html')

            if request.method == 'POST':
                # obtener datos para generar los criterios
                id_consulta = int(request.form['consultas'])
                n_inicial = int(request.form['n_inicial'])
                n_final = int(request.form['n_final'])
                # procesar el requerimiento según la solicitud recibida
                if id_consulta == 1:
                    data = estadisticas.por_distrito(n_inicial, n_final)
                    unique, counts = data_process(data)
                    title = "Clasificación por distrito"
                    # graficar
                    fig = plt.figure()
                    fig.suptitle(title)
                    ax = fig.add_subplot()
                    ax.bar(unique, counts, label='Cantidad de accidentes')
                    ax.set_facecolor('whitesmoke')
                    plt.xticks(rotation=30, size=8)  # atributos de etiquetas del eje x
                    ax.legend()
                elif id_consulta == 2:
                    data = estadisticas.por_tipo(n_inicial, n_final)
                    unique, counts = data_process(data)
                    title = "Clasificación por tipo de accidente"
                    # graficar
                    fig = plt.figure()
                    fig.suptitle(title)
                    ax = fig.add_subplot()
                    ax.bar(unique, counts, label='Cantidad de accidentes')
                    ax.set_facecolor('whitesmoke')
                    plt.xticks(rotation=30, size=8)  # atributos de etiquetas del eje x
                    ax.legend()
                elif id_consulta == 3:
                    data = estadisticas.por_lugar_de_denuncia(n_inicial, n_final)
                    unique, counts = data_process(data)
                    title = "Clasificación por lugar de denuncia"
                    # graficar
                    fig = plt.figure()
                    fig.suptitle(title)
                    ax = fig.add_subplot()
                    ax.bar(unique, counts, label='Cantidad de accidentes')
                    ax.set_facecolor('whitesmoke')
                    plt.xticks(rotation=30, size=8)  # atributos de etiquetas del eje x
                    ax.legend()
                elif id_consulta == 4:
                    data = estadisticas.por_lesiones(n_inicial, n_final)
                    unique, counts = data_process(data)
                    title = "Clasificación por lesiones"
                    # graficar
                    fig = plt.figure()
                    fig.suptitle(title)
                    ax = fig.add_subplot()
                    ax.bar(unique, counts, label='Cantidad de accidentes')
                    ax.set_facecolor('whitesmoke')
                    plt.xticks(rotation=30, size=8)  # atributos de etiquetas del eje x
                    ax.legend()
                elif id_consulta == 5:
                    interval_q = estadisticas.por_horario(n_inicial, n_final)
                    # gráfico de accidentes por horarios
                    interval = ('00:00-02:01', '02:01-04:01', '04:01-06:01', '06:01-08:01', '08:01-10:01', '10:01-12:01', '12:01-14:01', '14:01-16:01', '16:01-18:01', '18:01-20:01', '20:01-22:01', '22:01-00:00')
                    interval_q = np.array(interval_q)
                    title = 'Distribución de accidentes por hora'
                    # graficar
                    fig = plt.figure()
                    fig.suptitle('Accidentes por horario', fontsize=12)
                    ax = fig.add_subplot()
                    ax.plot(interval, interval_q, marker='^', c='darkmagenta', label='cantidad de accidentes')
                    ax.set_facecolor('whitesmoke')
                    plt.xticks(rotation=30, size=8)
                    ax.grid('solid')
                    ax.legend()
                elif id_consulta == 6:
                    data = estadisticas.por_sexo(n_inicial, n_final)
                    unique, counts = data_process(data)
                    sum_counts = sum(counts)
                    title = "Clasificación por sexo de conductores - Registros:", sum_counts
                    # graficar
                    fig = plt.figure()
                    fig.suptitle(title)
                    ax = fig.add_subplot()
                    ax.pie(counts, labels=unique, autopct='%1.1f%%', shadow=True, startangle=90)
                    ax.set_facecolor('whitesmoke')
                    ax.axis('equal')
                elif id_consulta == 7:
                    data = estadisticas.por_franja_etaria(n_inicial, n_final)
                    unique, counts = data_process(data)
                    sum_counts = sum(counts)
                    title = 'Clasificación por franja etaria de conductores - Registros:', sum_counts          
                    # graficar
                    fig = plt.figure()
                    fig.suptitle(title)
                    ax = fig.add_subplot()
                    ax.pie(counts, labels=unique, autopct='%1.1f%%',shadow=True, startangle=90)
                    ax.set_facecolor('whitesmoke')
                    ax.axis('equal')
                elif id_consulta == 8:
                    data = estadisticas.por_test_alcoholemia(n_inicial, n_final)
                    test_0 = [+1 for test in data if test == 0]
                    test_1 = [+1 for test in data if test > 0 and test <= 0.50]
                    test_2 = [+1 for test in data if test > 0.50 and test <= 1]
                    test_3 = [+1 for test in data if test > 1 and test <= 2]
                    test_4 = [+1 for test in data if test > 2 and test <= 3]
                    test_5 = [+1 for test in data if test > 3]
                    # conteo por segmento
                    counts = (len(test_0), len(test_1), len(test_2), len(test_3), len(test_4), len(test_5))
                    sum_counts = sum(counts)
                    # gráfico
                    leyendas = ('0,00', '0,01-0,50', '0,51-1,00', '1,01-2,00', '2,01-3,00', '>3,00')
                    title = 'Clasificación por test de alcoholemia - Registros:', sum_counts          
                    fig = plt.figure()
                    fig.suptitle(title)
                    ax = fig.add_subplot()
                    ax.pie(counts, labels=leyendas, autopct='%1.1f%%',shadow=True, startangle=90)
                    ax.set_facecolor('whitesmoke')
                    ax.axis('equal')
                # convertir gráfico en imagen con canvas
                output = io.BytesIO()
                FigureCanvas(fig).print_png(output)
                return Response (output.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})


def data_process(data):
    '''
    Aplicar unique y counts de numpy
    '''
    try:
        # transformar en arrays
        data = np.array(data)
        # Agrupar por criterio
        unique, counts = np.unique(data, return_counts=True)
        # transformar array en lista
        unique = tuple(unique)
        return unique, counts
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/accidentologia/update_lat_lng/", methods=['GET', 'POST'])
def update_lat_lng():
    '''
    Update de latitud y longitud para la correccion de valores mal determinados 
    '''
    if request.method == "GET":
        return render_template('update_latitud_longitud_form.html')
    
    try:
        if request.method == 'POST':
            n_acc = int(request.form['n_accidente'])
            lat = float(request.form['latitud'])
            lng = float(request.form['longitud'])

            query_acc_db.update_lat_lng(n_acc, lat, lng)
            
            return 'cambio realizado'
    except:
        return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':

    app.run(debug=True)
