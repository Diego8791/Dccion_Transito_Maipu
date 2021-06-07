#!/usr/bin/env python
'''
API Personas
---------------------------
Autor: .......
Version: 1.0

Descripcion:
Se utiliza .......

Ejecución: Lanzar el ..........


'''

__author__ = "Inove Coding School"
__email__ = "INFO@INOVE.COM.AR"
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
    Ingresar a home principal
    '''
    try:
        if 'user' in session:
            return render_template('home.html')
    except:
        return jsonify({'trace': traceback.format_exc()})


# -----------------------  ACCIDENTOLOGIA --------------------------------------------------

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

                adress = direccion + ', ' + distrito + ', Maipú, Mendoza, Argentina'                                                       # crear string para georeferenciación
                lat, lng = my_geo.adress_locations(adress)                                                                                 # obterner latitud y longitud

                # Abrir base de datos users_db
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                cursor = conn.cursor()

                sql = 'SELECT id FROM distritos_maipu WHERE n_distritos_maipu = (%s)'                                                       # obtener id de distrito
                cursor.execute(sql, [distrito])
                distrito = cursor.fetchone()[0]

                data = [n_acc, fecha, hora, direccion, distrito, perito, tomado_en, tipo, con_sin_les, obs, lat, lng]                        # registrar registro en base de datos accidentologia_db
                
                sql = '''INSERT INTO datos_grales_acc
                            (n_acc, fecha, hora, direccion, fk_distrito_maipu_id, fk_perito_id,
                            fk_tomado_en_id, fk_tipo_id, fk_lesiones_id, obs, latitud, longitud)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cursor.execute(sql, data)
                conn.commit()           

                # cerrar conexion
                conn.close()
                
                flash('¡BUEN TRABAJO!... se han cargado los datos generales!')                                                                                       # Mensaje de sesión cerrada
                return redirect(url_for('insert_data'))
    except:
        flash('¡ATENCIÓN!... Se ha producido un error al registrar los datos generales') 
        return redirect(url_for('insert_data'))    


@app.route("/accidentologia/insert_acc_gral_data/insert_participe/", methods=['GET', 'POST'])
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
            if test_alcoholemia == '':                                  #salvar cuando no se hace
                test_alcoholemia = 'no se realizó'
            f_etaria = int(request.form['f_etaria'])
            dominio = request.form['dominio']

            try:
                # Abrir base de datos dccion_transito_db
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                cursor = conn.cursor()
          
                sql = 'SELECT id FROM rodado WHERE patente = (%s)'                                                                    # Obtener id de dominio de vehículo
                cursor.execute(sql,[dominio])
                id_patente = cursor.fetchone()[0]

                sql = 'SELECT id FROM padron WHERE n_doc = (%s)'                                                                       # obtener id de dni
                cursor.execute(sql,[n_doc])
                id_n_doc = cursor.fetchone()[0]

                # Verificar que en n_doc no esté ya cargado en el numero de accidente
                sql = 'SELECT fk_n_doc_id FROM participe WHERE n_acc = (%s)'
                cursor.execute(sql,[n_acc])
                resultado = cursor.fetchall()
                # validación de d.n.i. para el número de accidente
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
                    flash('¡BUEN TRABAJO!... Partícipe registrado con éxito')                                                                                # mensaje de error
                    return redirect(url_for('insert_participe_accidentologia'))  
                else:
                    flash('¡ATENCIÓN!...El partícipe ya se encuentra registrado en ese accidente')                                                                                # mensaje de error
                    return redirect(url_for('insert_participe_accidentologia'))
            except:
                flash('¡ERROR AL REGISTRAR!... no se ha podido ingresar el partícipe')                                                                                # mensaje de error
                return redirect(url_for('insert_participe_accidentologia'))


# ------------------------------ CONSULTAS ----------------------------------------------------

@app.route("/accidentologia/search_menu/", methods=['GET', 'POST'])
# @login_required
def search_menu():
    '''
    Menu de consultas
        - Buscar por D.N.I.
        - Buscar por dominio
        - Buscar por accidente
        - Buscar por fecha de ocurrencia
    '''
    try:
        if 'user' in session:
            if request.method == "GET":
                return render_template('search_data_form.html')                                                             # llamar a formulario principal de consultas

            if request.method == "POST":
                opcion = int(request.form['consulta'])
                if opcion == 1:
                    data=[]
                    return render_template('search_dni_form.html', data=data)
                elif opcion == 2:
                    data = []
                    return render_template('search_dominio_form.html', data=data)
                elif opcion == 3:
                    datos_acc = []
                    participe = []
                    lat_long = [-32.9727, -68.8119]
                    return render_template('search_data_acc_form.html', datos_acc=datos_acc, participe=participe, lat_long=lat_long)
                else:
                    datos_acc = []
                    return render_template('search_date_acc_form.html', datos_acc=datos_acc)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/search_dni/", methods=['GET', 'POST'])
def search_dni():
    '''
    Consultar datos por D.N.I.
    '''
    try:
        if 'user' in session:
            if request.method == "GET":
                datos_padron = ()
                datos_acc_list = ()
                return render_template('search_dni_form.html', data=datos_padron, datos_acc_list=datos_acc_list)

            if request.method == "POST":
                n_dni = request.form['n_dni']
                datos_padron, datos_acc_list = query_acc_db.padron_dni(n_dni)
                return render_template('search_dni_form.html', data=datos_padron, datos_acc_list=datos_acc_list)        
    except:    
        flash('D.N.I. no registrado')                                                                                # mensaje de que no está registrado el D.N.I.
        return redirect(url_for('search_dni'))                                                                     # validación icorrecta
        

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

            if datos_dominio is not None:
                return render_template('search_dominio_form.html', data=datos_dominio, datos_acc=datos_acc_list)
            else:          
                flash('Dominio no registrado')                                                                                # mensaje de que no está registrado el D.N.I.
                return redirect(url_for('select_dominio'))                                                                       # validación icorrecta         


@app.route("/accidentologia/data_acc_search/", methods=['GET', 'POST'])
def data_acc_search():
    '''
    Consultar datos generales de accidentes por fecha
    '''
    datos_acc = []
    participes = []
    lat_long = []
    try:
        if 'user' in session:
           
            if request.method == 'POST':
                n_acc = int(request.form['n_acc'])
                datos_acc, participes, lat_long = query_acc_db.data_search_acc(n_acc)
                print(lat_long)
            return render_template('search_data_acc_form.html', datos_acc=datos_acc, participes=participes, lat_long=lat_long)             
    except:
        flash('¡ATENCION!... Accidente no encontrado')                                                                   # mensaje de que no está registrado el D.N.I.
        return redirect(url_for('/accidentologia/data_acc_search/'))                                                                       # validación icorrecta 


@app.route("/accidentologia/date_search/", methods=['GET', 'POST'])
def date_search_acc():
    '''
    Consultar datos generales de accidentes por fecha
    '''
    # try:
    if 'user' in session:
        if request.method == "GET":

            return render_template('search_date_acc_form.html')

        if request.method == 'POST':

            fecha_inicio = request.form['fecha_inicio']
            fecha_final = request.form['fecha_final']

            data = query_acc_db.date_search_acc(fecha_inicio, fecha_final)

            return render_template('search_date_acc_form.html', data=data)


# ----------------------REGISTRAR PERSONAS EN PADRON -----------------------------------

@app.route("/insert_persona/", methods=['GET', 'POST'])
def insert_persona():
    '''
    Ingresar datos de una persona que no se encuentra en base de datos padron_db
    '''
    try:
        if 'user' in session:
            if request.method == "GET":

                # Abrir base de datos users_db
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                # crear objeto cursor usando el método cursor()
                cursor = conn.cursor()

                # seleción dinámica de distritos de todo el país para ingresar ciudadano a padron
                sql = "SELECT id, n_distrito FROM distritos"
                cursor.execute(sql)
                # bucle que lee los distritos disponibles
                distritos = []
                for distrito in cursor:
                    distritos.append(distrito)

                # seleción dinámica de departamentos para ingresar ciudadano a padron
                sql = "SELECT id, n_departamento FROM departamentos"
                cursor.execute(sql)
                # bucle que lee los departamentos
                departamentos = []
                for departamento in cursor:
                    departamentos.append(departamento)

                # seleción dinámica de provincias de todo el país para ingresar ciudadano a padron
                provincias = []
                sql = "SELECT id, provincia FROM provincias"
                cursor.execute(sql)
                # bucle que lee las provincias
                for provincia in cursor:
                    provincias.append(provincia)

                # seleción dinámica de nacionalidades de todo el país para ingresar ciudadano a padron
                nacionalidades = []
                sql = "SELECT id, nacionalidad FROM nacionalidades"
                cursor.execute(sql)
                # bucle que lee las provincias
                for nacionalidad in cursor:
                    nacionalidades.append(nacionalidad)

                # cerrar conexion
                conn.close()

                return render_template('insert_persona_form.html', distrit=distritos, dptos=departamentos, nacion=nacionalidades, pcias=provincias)

            if request.method == 'POST':

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

                data = [nombre, tipo_dni, n_doc, sexo, f_nacimiento, e_civil, cuil, domicilio, distrito, dpto, pcias, nacionalidad, c_postal]

                # establecer la conección
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                # crear objeto cursor usando el método cursor()
                cursor = conn.cursor()
                sql = 'SELECT * FROM padron WHERE n_doc = (%s)'
                cursor.execute(sql, [n_doc])
                result = cursor.fetchone()
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
        flash('¡ATENCIÓN!... Se produjo un error al registrar') 
        return redirect(url_for('insert_persona'))


# ------------------------INGRESAR DE VEHICULOS POR DOMINIO. -----------------------------------------

@app.route("/insert_vehiculo/", methods=['GET', 'POST'])
def insert_vehiculo():
    '''
    Insertar datos de una persona que no se encuentra en base de datos padron_db
    '''
    try:
        if 'user' in session:
            if request.method == "GET":

                # Abrir conexion
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                # crear objeto cursor usando el método cursor()
                cursor = conn.cursor()

                # Busqueda dinámica para formulario
                marcas = []
                cursor.execute("SELECT id, marca FROM marca_rodado")
                for marca in cursor:
                    marcas.append(marca)

                modelos = []
                cursor.execute("SELECT id, modelo FROM modelo_rodado")
                for modelo in cursor:
                    modelos.append(modelo)

                # cerrar la conexion
                conn.close()

                # llamar a formulario pasando lista para seleccion dinamica
                return render_template('insert_vehiculos_form.html', marcas=marcas, modelos=modelos)

            if request.method == 'POST':

                dominio = request.form['dominio']
                marca = request.form['marca']
                modelo = request.form['modelo']

                rodado = [dominio, marca, modelo]
                # Abrir conexion
                conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
                # crear objeto cursor usando el método cursor()
                cursor = conn.cursor()

                # query
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
    Se selecciona el intérvalo de accidentes para producir mapa accidentológico.
    n_inicial es el número de accidente inicial y n_final es el último número de accidente a considerar.
    Ej: n_inicial: 200127; n_final: 200137, se seleccionarán los números 127, 128, 129, 130, 131, 132,
    133, 134, 135, 136 y 137 del año 2020.
    Para formar la lista de accidentes se utilizará el módulo mapa_accidentologico del archivo query_acc_db
    '''

    try:
        if 'user' in session:
            if request.method == 'GET':

                return render_template('map_form.html')

            if request.method == 'POST':

                n_inicial = request.form['n_inicial']
                n_final = request.form['n_final']

                lista_geo = query_acc_db.mapa_accidentologico(int(n_inicial), int(n_final))
    
        # Extraer cuantos accidentes hay por cada localización
        lista_geo = collections.Counter(lista_geo)
            
        # extraer el valor mas alto de cantidad de accidentes
        v_max = max([v for k, v in lista_geo.items()])
        
        some_map = folium.Map(location=[-32.9853509, -68.7877007], zoom_start=15, titles='localización de puntos de accidentes')
        
        for k, v in lista_geo.items():
            # Distribución de accidentes
            if v < (v_max * 0.3333334) :
                folium.Circle(k, popop='<i>The Waterfront</i>', radius=30, fill=True, color='green',  tooltip=v).add_to(some_map)
            elif v >= (v_max * 0.3333334) and v < (v_max * 0.6666667):
                folium.CircleMarker(k, popop='<i>The Waterfront</i>', radius=30, fill=True, color='orange',  tooltip=v).add_to(some_map)
            else:
                folium.CircleMarker(k, popop='<i>The Waterfront</i>', radius=30, fill=True, color='red',  tooltip=v).add_to(some_map)
            
        return some_map._repr_html_()
    except:
        return "<h1>No hay accidentes a mostrar<h1>"


# -----------------------------------------------------------------------------------------------------------------------------


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
                    interval = ('00:00-02:00', '02:01-04:00', '04:01-06:00', '06:01-08:00', '08:01-10:00', '10:01-12:00', '12:01-14:00', '14:01-16:00', '16:01-18:00', '18:01-20:00', '20:01-22:00', '22:01-23:59')
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
