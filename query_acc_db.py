#!/usr/bin/env python
'''
.............
.............
---------------------------
Autor:
Version:

Descripcion: Querys
Programa creado...
'''

__author__ = "...."
__email__ = "...."
__version__ = "....."


import sqlite3
import geo
import mysql.connector
from datetime import datetime, timedelta


def q_por_numero_acc():

    try:
        n_acc = int(input('ingrese numero de accidente a buscar: '))
    except:
        print('numero no válido')

    conn = sqlite3.connect('accidentologia_db')
    cur = conn.cursor()
    cur.execute('ATTACH DATABASE padron_db AS p_db')
    cur.execute('ATTACH DATABASE vehiculos_db AS v_db')

    try:
        for datos_acc in cur.execute('''
                            SELECT g.fecha, g.hora, g.direccion, d.nombre, p.nombre,
                                    t.nombre, i.nombre, l.con_sin_les
                            FROM datos_grales AS g
                            INNER JOIN distrito AS d ON g.fk_distrito_id = d.id
                            INNER JOIN perito AS p ON g.fk_perito_id = p.id
                            INNER JOIN tomado_en AS t ON g.fk_tomado_en_id = t.id
                            INNER JOIN tipo AS i ON g.fk_tipo_id = i.id
                            INNER JOIN lesiones AS l ON g.fk_lesiones_id = l.id
                            WHERE g.n_acc = (?)''', [n_acc]):
            print(datos_acc)
    except sqlite3.Error as err:
        print(err)

    try:
        for datos_con in cur.execute('''
                            SELECT p.n_doc, p.nombre, d.patente, m.marca, l.modelo
                            FROM participe AS t
                            INNER JOIN padron AS p ON t.fk_n_doc_id = p.id
                            INNER JOIN dominio AS d ON t.fk_patente_id = d.id
                            INNER JOIN marca AS m ON d.fk_marca_id = m.id
                            INNER JOIN modelo AS l ON d.fk_modelo_id = l.id
                            WHERE t.n_acc = (?)''', [n_acc]):
            print(datos_con)
    except sqlite3.Error as err:
        print(err)

    conn.close()


def padron_dni(n_dni):

    # Abrir base de datos padron_db
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    # buscar los datos personlaes del DNI solicitado
    sql = '''SELECT p.n_doc, p.nombre, p.domicilio, d.n_distrito, t.n_departamento, v.provincia, p.sexo
            FROM padron AS p
            INNER JOIN distritos AS d ON p.fk_distrito_id = d.id
            INNER JOIN departamentos AS t ON p.fk_depto_id = t.id
            INNER JOIN provincias AS v ON p.fk_pcia_id = v.id
            WHERE n_doc = (%s)'''
    cursor.execute(sql, [n_dni])
    datos_padron = cursor.fetchone()

    if datos_padron is not None:
        # devuelve el id del DNI solicitado
        sql = 'SELECT id FROM padron WHERE n_doc = (%s)'
        cursor.execute(sql, [n_dni])
        try:
            id_dni = cursor.fetchone()
            id_doc = id_dni[0]
        except mysql.connector.Error as err:
            print(err)

        # saber numeros de accidentes en que el que ha sido participe
        sql = 'SELECT n_acc FROM participe WHERE fk_n_doc_id = (%s)'
        cursor.execute(sql,[id_doc])
        acc_part = cursor.fetchall()
        n_acc = []
        for accidente in acc_part:
            n_acc.append(accidente[0])

        print(n_acc)

        # armar una lista de tuplas para devolver al formulario los datos de los accidentes en que se ha sido partícipe
        datos_acc_list = []
        sql = 'SELECT n_acc, fecha, direccion FROM datos_grales_acc WHERE n_acc = (%s)'

        for accidente in n_acc:
            cursor.execute(sql, [accidente])
            datos_acc_list.append(cursor.fetchone())

            # datos = cursor.fetchall()
            # datos_acc_list.append(datos)
        print(datos_acc_list)

    else:
        datos_padron = []

    # cerrar conexion
    conn.close()

    return datos_padron, datos_acc_list


def search_dominio(dominio):

    # Abrir base de datos padron_db
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    sql = '''SELECT r.patente, m.marca, o.modelo
            FROM rodado AS r
            INNER JOIN marca_rodado AS m ON r.fk_marca_id = m.id
            INNER JOIN modelo_rodado AS o ON r.fk_modelo_id = o.id
            WHERE patente = (%s)'''
    cursor.execute(sql, [dominio])
    datos_dominio = cursor.fetchone()

    if datos_dominio is not None:
        # devuelve el id del dominio solicitado
        sql = 'SELECT id FROM rodado WHERE patente = (%s)'
        cursor.execute(sql, [dominio])
        try:
            id_dominio = cursor.fetchone()
            id_dominio = id_dominio[0]
        except mysql.connector.Error as err:
            print(err)

        # saber numeros de accidentes en que el que ha sido participe
        sql = 'SELECT n_acc FROM participe WHERE fk_rodado_id = (%s)'
        cursor.execute(sql,[id_dominio])
        acc_part = cursor.fetchall()
        n_acc = []
        for accidente in acc_part:
            n_acc.append(accidente[0])

        # armar una lista de tuplas para devolver al formulario los datos de los accidentes en que se ha sido partícipe
        datos_acc_list = []
        sql = 'SELECT n_acc, fecha, direccion FROM datos_grales_acc WHERE n_acc = (%s)'

        for accidente in n_acc:
            cursor.execute(sql, [accidente])
            datos_acc_list.append(cursor.fetchone())
    else:
        datos_dominio = None
        datos_acc_list = []

    # cerrar conexion
    conn.close()

    return datos_dominio, datos_acc_list


def mapa_accidentologico(n_inicial, n_final):
    '''
    Se toma el número inicial de accidente seleccionado y el número final, se abre la base de datos accidentologia_db,
    y se extraen los datos numero de accidente, latitud y longitud correspondiente a cada acciente en el intervalo
    seleccionado.
    '''
    while True:
        # Se evalúa si el n_inicial es menor a n_final (condición necesaria)
        if n_inicial > n_final:
            print('Ha ingresado un numero inicial menor al final')
        else:
            # Se forma lista con números de accidentes del intervalo
            
            print(n_inicial, n_final)
            
            list_n_acc = [n_acc for n_acc in range(n_inicial, n_final+1)]

            # Abrir base de datos datos_grales_acc_db
            conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
            # crear objeto cursor usando el método cursor()
            cursor = conn.cursor()

            # Se forma lista lista de listas con numero de accidente, latitud y longitud de todo el intérvalo
            lista_geo = []
            # query
            sql = '''SELECT g.latitud, g.longitud
                        FROM datos_grales_acc AS g
                        WHERE g.n_acc = (%s)'''
            for accidente in list_n_acc:
                cursor.execute(sql, [accidente])
                result = cursor.fetchone()
                if result is not None:
                    lista_geo.append(result)

            # Se cierra base de datos
            conn.close()
            
            return lista_geo
           

def date_search_acc(fecha_inicio, fecha_final):

    # transformar string en datetime
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d').date()

    # crear lista con el intervalo completo de fechas
    date_list = []
    while fecha_inicio <= fecha_final:
        date_list.append(datetime.strftime(fecha_inicio, '%Y-%m-%d'))
        # se suma dia a dia
        fecha_inicio += timedelta(days=1)

    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    sql = '''SELECT g.fecha, g.n_acc, g.hora, g.direccion, d.n_distritos_maipu, p.perito, t.lugar, i.acc_tipo, l.con_sin_les
                FROM datos_grales_acc AS g
                INNER JOIN distritos_maipu AS d ON g.fk_distrito_maipu_id = d.id
                INNER JOIN perito AS p ON g.fk_perito_id = p.id
                INNER JOIN tomado_en AS t ON g.fk_tomado_en_id = t.id
                INNER JOIN tipo AS i ON g.fk_tipo_id = i.id
                INNER JOIN lesiones AS l ON g.fk_lesiones_id = l.id
                WHERE fecha = (%s)'''
    # formar lista de tuplas con los registros
    data = []
    for date in date_list:
        cursor.execute(sql, [date])
        info_list = cursor.fetchall()
        for element in info_list:
            data.append(element)

    # cerrar la conección
    conn.close()
    # ordenar por numero de accidente decreciente ¡gran lambda!
    data.sort(key=lambda n_acc: n_acc[1], reverse=True)
    return data


def data_search_acc(n_acc):
    '''
    Se extraen de la data base datos generales de un accidente y sus participes.
    '''
    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    sql = '''SELECT g.fecha, g.n_acc, g.hora, g.direccion, d.n_distritos_maipu, p.perito, t.lugar, i.acc_tipo, l.con_sin_les, g.obs
                FROM datos_grales_acc AS  g
                INNER JOIN distritos_maipu AS d ON g.fk_distrito_maipu_id = d.id
                INNER JOIN perito AS p ON g.fk_perito_id = p.id
                INNER JOIN tomado_en AS t ON g.fk_tomado_en_id = t.id
                INNER JOIN tipo AS i ON g.fk_tipo_id = i.id
                INNER JOIN lesiones AS l ON g.fk_lesiones_id = l.id
                WHERE n_acc = (%s)'''
    cursor.execute(sql, [n_acc])
    datos_acc = cursor.fetchone()
    
    # query de latitud y longitud
    sql = 'SELECT g.latitud, g.longitud FROM datos_grales_acc AS g WHERE n_acc = (%s)'
    cursor.execute(sql, [n_acc])
    lat_long = cursor.fetchone()

    sql = '''SELECT p.n_doc, p.nombre, t.alcoholemia, d.patente, m.marca, l.modelo
                FROM participe AS t
                INNER JOIN padron AS p ON t.fk_n_doc_id = p.id
                INNER JOIN rodado AS d ON t.fk_rodado_id = d.id
                INNER JOIN marca_rodado AS m ON d.fk_marca_id = m.id
                INNER JOIN modelo_rodado AS l ON d.fk_modelo_id = l.id
                WHERE t.n_acc = (%s)'''
    cursor.execute(sql, [n_acc])
    participes = cursor.fetchall()

    # cerrar conección
    conn.close()

    return datos_acc, participes, lat_long


def update_lat_lng(n_acc, lat, lng):
    '''
    Update de latitud y longitud.
    '''
    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()
    
    data = (lat, lng, n_acc)
    
    # update de latitud y longitud
    sql = 'UPDATE datos_grales_acc SET latitud = (%s), longitud = (%s) WHERE n_acc = (%s)'
    cursor.execute(sql, data)
    conn.commit()
    # cerrar coneccion
    conn.close()
