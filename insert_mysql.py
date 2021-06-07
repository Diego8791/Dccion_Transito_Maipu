#!/usr/bin/env python
'''
.............
.............
---------------------------
Autor:
Version:

Descripcion:
Programa creado para ingresar datos a las bases mysql
'''

__author__ = "...."
__email__ = "...."
__version__ = "....."

import csv
import mysql.connector


def insert_users():

    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='users_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    print('ingresar tipo o usuarios')
    opcion = int(input('tipo = 1 / usuario = 2:' ))
    if opcion == 1:
        try:
            # ingresar tipos de usuarios
            tipo_usuario = input('Tipo de usuario: ')
            sql = '''INSERT INTO type_users (type_users)
                VALUES (%s)'''
            cursor.execute(sql, [tipo_usuario])
            conn.commit()
            print('Tipo de usuario ingresado satisfactoriamente')
        except:
            print('Tipo de usuario no ingresado')
    else:
        try:
            # ingresar usuarios
            name = input('Nombre de usuario: ')
            password = input('Password: ')
            e_mail = input('e_mail: ')
            type_user = input('admin / 2 = Usuario')
            data = [name, password, e_mail, type_user]
            # sql de ingreso
            sql = '''INSERT INTO users (name, password, e_mail, fk_type_user_id)
                VALUES (%s, %s, %s, %s)'''
            # ejecutar la query
            cursor.execute(sql, data)
            conn.commit()
            print('Usuario ingresado satisfactoriamente')
        except:
            print('no ha podido ingresarse el usuario')

    # cerrar la conección
    conn.close()


def select_users():

    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='users_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    opcion = int(input('ver tabla type_users(1) o users(2): '))
    if opcion == 1:
        sql = 'SELECT * FROM type_users'
    else:
        sql = 'SELECT * FROM users'
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)

    # cerrar la conección
    conn.close()


def insert_data():

    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    print('indicar que se desea ingresar: ')

    opcion = int(input('''
                        1 - distrito de maipu
                        2 - perito
                        3 - tipo de accidente
                        4 - franja etaria
                        5 - lesiones
                        6 - tomado en
                        7 - nacionalidades
                        8 - departamentos
                        9 - provincias
                        10 - distritos
                        11 - marcas
                        12 - modelos
                        13 - vehiculos
                        14 - padron
                        '''))
    if opcion == 1:
        print('ingresar distrito')
        try:
            # ingresar tipos de accidentes
            distrito = input('Ingresar distrito de maipu: ')
            sql = '''INSERT INTO distritos_maipu (n_distritos_maipu)
                       VALUES (%s)'''
            cursor.execute(sql, [distrito])
            conn.commit()
            print('Distrito ingresado satisfactoriamente')
        except:
            print('Distrito no ingresado')
    if opcion == 2:
        print('ingresar perito')
        try:
            # ingresar peritos
            perito = input('perito: ')
            sql = '''INSERT INTO perito (perito)
                VALUES (%s)'''
            cursor.execute(sql, [perito])
            conn.commit()
            print('perito ingresada satisfactoriamente')
        except:
            print('perito no ingresado')
    if opcion == 3:
        print('ingresar tipo de accidentes')
        try:
            # ingresar tipos de accidentes
            tipo_accidente = input('Tipo de accidente: ')
            sql = '''INSERT INTO tipo (acc_tipo)
                VALUES (%s)'''
            cursor.execute(sql, [tipo_accidente])
            conn.commit()
            print('Tipo de accidente ingresado satisfactoriamente')
        except:
            print('Tipo de accidentologia no ingresado')
    if opcion == 4:
        print('ingresar franja etaria')
        try:
            # ingresar tipos de accidentes
            franja_etaria = input('Franja etaria: ')
            sql = '''INSERT INTO fran_etaria (franja)
                VALUES (%s)'''
            cursor.execute(sql, [franja_etaria])
            conn.commit()
            print('Franja etaria ingresada satisfactoriamente')
        except:
            print('Franja etaria no ingresado')
    if opcion == 5:
        print('ingresar lesiones')
        try:
            # ingresar tipos de lesiones
            lesiones = input('lesiones: ')
            sql = '''INSERT INTO lesiones (con_sin_les)
                VALUES (%s)'''
            cursor.execute(sql, [lesiones])
            conn.commit()
            print('Lesion ingresada satisfactoriamente')
        except:
            print('Lesion etaria no ingresado')
    if opcion == 6:
        print('ingresar tomado en')
        try:
            # ingresar lugar
            tomado_en = input('tomado en : ')
            sql = '''INSERT INTO tomado_en (lugar)
                VALUES (%s)'''
            cursor.execute(sql, [tomado_en])
            conn.commit()
            print('ingresada satisfactoriamente')
        except:
            print('no ingresado')
    if opcion == 7:
        with open ('naciones.csv') as csvFile:
            data = list(csv.reader(csvFile))
        # cerrar conexion con archivo csv
        csvFile.close()

        sql = '''INSERT INTO nacionalidades (id, nacionalidad)
                VALUES (%s,%s) '''

        for row in data:
            cursor.execute(sql, row)
            conn.commit()
    if opcion == 8:
        with open ('deptos.csv') as csvFile:
            data = list(csv.reader(csvFile))
        # cerrar conexion con archivo csv
        csvFile.close()

        sql = '''INSERT INTO departamentos (id, n_departamento, region)
                VALUES (%s, %s, %s) '''

        for row in data:
            cursor.execute(sql, row)
            conn.commit()
    if opcion == 9:
        with open ('provincs.csv') as csvFile:
            data = list(csv.reader(csvFile))
        # cerrar conexion con archivo csv
        csvFile.close()

        sql = '''INSERT INTO provincias (id, provincia)
                VALUES (%s, %s) '''

        for row in data:
            cursor.execute(sql, row)
            conn.commit()
    if opcion == 10:
        with open ('distrits.csv') as csvFile:
            data = list(csv.reader(csvFile))
        # cerrar conexion con archivo csv
        csvFile.close()

        sql = '''INSERT INTO distritos (id, n_distrito)
                VALUES (%s, %s) '''

        for row in data:
            cursor.execute(sql, row)
            conn.commit()
    if opcion == 11:
        with open ('marcas.csv') as csvFile:
            data = list(csv.reader(csvFile))
        # cerrar conexion con archivo csv
        csvFile.close()

        sql = '''INSERT INTO marca_rodado (marca)
                VALUES (%s) '''

        for row in data:
            cursor.execute(sql, [row[1]])
            conn.commit()
    if opcion == 12:
        with open ('modelos.csv') as csvFile:
            data = list(csv.reader(csvFile))
        # cerrar conexion con archivo csv
        csvFile.close()

        sql = '''INSERT INTO modelo_rodado (modelo)
                VALUES (%s) '''

        for row in data:
            modelo = row[0]
            cursor.execute(sql, [modelo])
            conn.commit()
    if opcion == 13:
        with open ('vehiculos.csv') as csvFile:
            data = list(csv.reader(csvFile))
        # cerrar conexion con archivo csv
        csvFile.close()

        sql_marca = 'SELECT id FROM marca_rodado WHERE marca = (%s)'
        sql_modelo = 'SELECT id FROM modelo_rodado WHERE modelo = (%s)'
        sql = '''INSERT INTO rodado (patente, fk_marca_id, fk_modelo_id)
                    VALUES (%s,%s,%s)'''

        for row in data:
            # print(row)

            marca = row[1]
            # print(marca)
            cursor.execute(sql_marca, [marca])
            id_marca = cursor.fetchall()[0]
            id_marca = id_marca[0]
            # print(id_marca)

            try:
                modelo = row[2]
                # print(modelo)
                cursor.execute(sql_modelo, [modelo])
                id_modelo = cursor.fetchall()[0]
                id_modelo = id_modelo[0]
                # print(id_modelo)
            except:
                print("pasar")

            vehiculo = [row[0], id_marca, id_modelo]
            print(vehiculo)
            cursor.execute(sql, vehiculo)
            conn.commit()

    if opcion == 14:

        with open ('padron_ordenado_0.csv') as csvFile:
            data = list(csv.reader(csvFile))
        # cerrar conexion con archivo csv
        csvFile.close()

        try:
            fails = 0
            for row in data:
                try:
                    row[2] =int(row[2])
                    row[8] = int(row[8])
                    if row[8] < 742 or row[8] > 935:
                        row[8] = 0
                    row[9] = int(row[9])
                    if row[9] < 724 or row[9] > 741:
                        row[9] = 0
                    row[10] = int(row[10])
                    if row[10] < 192 or row[10] > 215:
                        row[10] = 0
                    row[11] = int(row[11])
                    if row[11] < 0 or row[11] > 191:
                        row[11] = 0
                    print(row)

                    sql = '''INSERT INTO padron (nombre, tipo_doc, n_doc, sexo, f_naciomiento,
                                    e_civil, cuil, domicilio, fk_distrito_id, fk_depto_id,
                                    fk_pcia_id, fk_nacion_id, cod_postal)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                            '''
                    cursor.execute(sql, row)
                    print(row)
                    # conn.commit()
                except:
                    fails += 1
                    print('error: ', fails)
        except:
            print('error')


    # cerrar la conección
    conn.close()



def select_data():

    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    print('indicar que se desea consultar: ')

    opcion = int(input('''
                        1 - distrito de maipu
                        2 - perito
                        3 - tipo de accidente
                        4 - franja etaria
                        5 - lesiones
                        6 - tomado en
                        7 - nacionalidades
                        8 - departamentos
                        9 - provincias
                        10 - distritos
                        11 - marcas
                        12 - modelos
                        13 - vehiculos
                        14 - padron
                        15 - accidentologia
                        16 - participe
                        '''))

    if opcion == 1:
        sql = 'SELECT * FROM distritos_maipu'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 2:
        sql = 'SELECT * FROM perito'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 3:
        sql = 'SELECT * FROM tipo'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 4:
        sql = 'SELECT * FROM fran_etaria'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 5:
        sql = 'SELECT * FROM lesiones'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 6:
        sql = 'SELECT * FROM tomado_en'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 7:
        sql = 'SELECT * FROM nacionalidades'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 8:
        sql = 'SELECT * FROM departamentos'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 9:
        sql = 'SELECT * FROM provincias'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 10:
        sql = 'SELECT * FROM distritos'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 11:
        sql = 'SELECT * FROM marca_rodado'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 12:
        sql = 'SELECT * FROM modelo_rodado'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 13:
        sql = 'SELECT * FROM rodado'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 14:
        sql = 'SELECT * FROM padron'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 15:
        sql = 'SELECT * FROM datos_grales_acc'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    if opcion == 16:
        sql = 'SELECT * FROM participe'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)

    # cerrar la conección
    conn.close()


if __name__ == '__main__':

    # insert_users()
    # select_users()
    insert_data()
    # select_data()