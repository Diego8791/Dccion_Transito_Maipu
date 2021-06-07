import traceback
from datetime import datetime
import mysql.connector
from flask import jsonify


def por_distrito(n_inicial, n_final):
    '''
    Devuelve accidentes por distrito
    '''
    try:
        # llamar a la funcion "numeros_accidentes_lista" para formar lista de accidentes a graficar
        nros_acc_list = numeros_accidentes_lista(n_inicial, n_final)
        # query
        sql = '''SELECT d.n_distritos_maipu
                    FROM distritos_maipu AS d
                    INNER JOIN datos_grales_acc AS g ON g.fk_distrito_maipu_id = d.id
                    WHERE n_acc = (%s);'''
        # llamar a la funcion run_query
        data = run_query(sql, nros_acc_list)
        return data
    except:
            return jsonify({'trace': traceback.format_exc()})


def por_tipo(n_inicial, n_final):
    '''
    Devuelve accidentes por tipo de accidente
    '''
    try:
        # llamar a la funcion "numeros_accidentes_lista" para formar lista de accidentes a graficar
        nros_acc_list = numeros_accidentes_lista(n_inicial, n_final)
        # query
        sql = '''SELECT t.acc_tipo
                    FROM tipo AS t
                    INNER JOIN datos_grales_acc AS g ON g.fk_tipo_id = t.id
                    WHERE n_acc = (%s);'''
        data = run_query(sql, nros_acc_list)
        return data
    except:
        return jsonify({'trace': traceback.format_exc()})


def por_lugar_de_denuncia(n_inicial, n_final):
    '''
    Devuelve accidentes por por donde se toma
    '''
    try:
        # llamar a la funcion "numeros_accidentes_lista" para formar lista de accidentes a graficar
        nros_acc_list = numeros_accidentes_lista(n_inicial, n_final)
        # query
        sql = '''SELECT t.lugar
                    FROM tomado_en AS t
                    INNER JOIN datos_grales_acc AS g ON g.fk_tomado_en_id = t.id
                    WHERE n_acc = (%s);'''
        data = run_query(sql, nros_acc_list)
        return data
    except:
            return jsonify({'trace': traceback.format_exc()})


def por_lesiones(n_inicial, n_final):
    '''
    Devuelve accidentes por donde se toma
    '''
    try:
        ## llamar a la funcion "numeros_accidentes_lista" para formar lista de accidentes a graficar
        nros_acc_list = numeros_accidentes_lista(n_inicial, n_final)
        # query
        sql = '''SELECT l.con_sin_les
                    FROM lesiones AS l
                    INNER JOIN datos_grales_acc AS g ON g.fk_lesiones_id = l.id
                    WHERE n_acc = (%s);'''
        data = run_query(sql, nros_acc_list)
        return data
    except:
            return jsonify({'trace': traceback.format_exc()})


def por_horario(n_inicial, n_final):
    '''
    Devuelve accidentes por horario de ocurrencia
    '''
    try:
        # llamar a la funcion "numeros_accidentes_lista" para formar lista de accidentes a graficar
        nros_acc_list = numeros_accidentes_lista(n_inicial, n_final)
        # query
        sql = 'SELECT hora FROM datos_grales_acc WHERE n_acc = (%s);'
        interval_q = run_query_horario(sql, nros_acc_list)
        return interval_q
    except:
            return jsonify({'trace': traceback.format_exc()})


def numeros_accidentes_lista(n_inicial, n_final):
    '''
    Formar lista de numeros de accidentes a evaluar
    '''
    try:
        # Se forma lista con números de accidentes del intervalo
        nros_acc_list = [nro_acc for nro_acc in range(n_inicial, n_final+1)]
        # Retorna lista confeccionada
        return nros_acc_list
    except:
        return jsonify({'trace': traceback.format_exc()})


def run_query(sql, nros_acc_list):
    '''
    Ejecutar la query correspondiente al requerimiento
    '''
    try:
        # establecer la conección
        conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
        # crear objeto cursor usando el método cursor()
        cursor = conn.cursor()
        # ejecutar la query
        data = []
        for nro_acc in nros_acc_list:
            cursor.execute(sql, [nro_acc])
            result = cursor.fetchone()[0]
            data.append(result)
        # cerrar conexion
        conn.close
        # llamar a función graphic
        return data
    except:
        return jsonify({'trace': traceback.format_exc()})


def run_query_horario(sql, nros_acc_list):
    '''
    Ejecutar la query correspondiente al requerimiento de horarios
    '''
    print(nros_acc_list)
    try:
        # establecer la conección
        conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
        # crear objeto cursor usando el método cursor()
        cursor = conn.cursor()
        # ejecutar la query
        data = []
        for nro_acc in nros_acc_list:
            try:
                cursor.execute(sql, [nro_acc])
                result = cursor.fetchone()[0]
                print(result)
                data.append(datetime.strptime(result, '%H:%M').time())
            except:
                continue
        # cerrar conexion
        conn.close
        # horarios para límites de intervalos
        interval = ['00:00:00', '02:00:00', '04:00:00', '06:00:00', '08:00:00', '10:00:00', '12:00:00', '14:00:00', '16:00:00','18:00:00','20:00:00', '22:00:00', '23:59:00']
        interval_q = []
        # Contar accidentes por horario
        for x in range(12):
            interval_q.append(len([hora for hora in data if hora > datetime.strptime(interval[x],'%H:%M:%S').time() and hora <= datetime.strptime(interval[x+1],'%H:%M:%S').time()]))

        # llamar a función graphic
        print(interval_q)
        return interval_q

        # make_graph_line(interval_q, title)
    except:
        return jsonify({'trace': traceback.format_exc()})


def por_sexo(n_inicial, n_final):
    '''
    Ejecutar la query correspondiente al requerimiento por sexo
    '''
    nros_acc_list = numeros_accidentes_lista(n_inicial, n_final)
    print(nros_acc_list)    
    try:
        # establecer la conección
        conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
        # crear objeto cursor usando el método cursor()
        cursor = conn.cursor()
        # ejecutar la query
        data = []
        sql = '''SELECT sexo FROM padron AS p
                    INNER JOIN participe AS t ON t.fk_n_doc_id = p.id
                    WHERE t.n_acc = (%s);
                '''
        for nro_acc in nros_acc_list:
            cursor.execute(sql, [nro_acc])
            result = cursor.fetchall()
            for res in result:
                data.append(res[0])
        # cerrar conexion
        conn.close
        return data
    except:
        return jsonify({'trace': traceback.format_exc()})


def por_franja_etaria(n_inicial, n_final):
    '''
    Ejecutar la query correspondiente al requerimiento por franja_etaria
    '''
    nros_acc_list = numeros_accidentes_lista(n_inicial, n_final)
    try:
        # establecer la conección
        conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
        # crear objeto cursor usando el método cursor()
        cursor = conn.cursor()
        # ejecutar la query
        data = []
        sql = '''SELECT f.franja
                    FROM fran_etaria AS f
                    INNER JOIN participe AS p ON p.fk_fran_etaria = f.id
                    WHERE n_acc = (%s);'''
        for nro_acc in nros_acc_list:
            cursor.execute(sql, [nro_acc])
            result = cursor.fetchall()
            for res in result:
                data.append(res[0])
        return data
    except:
        return jsonify({'trace': traceback.format_exc()})     


def por_test_alcoholemia(n_inicial, n_final):
    '''
    Ejecutar la query correspondiente al requerimiento por test de alcoholemia
    '''
    nros_acc_list = numeros_accidentes_lista(n_inicial, n_final)
    try:
        # establecer la conección
        conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
        # crear objeto cursor usando el método cursor()
        cursor = conn.cursor()
        # ejecutar la query
        data = []
        sql = 'SELECT alcoholemia FROM participe WHERE n_acc = (%s);'''
        for nro_acc in nros_acc_list:
            cursor.execute(sql, [nro_acc])
            result = cursor.fetchall()
            print(result)
            for res in result:
                if res[0] != 'no se realizó':
                    data.append(float(res[0]))
        return data
    except:
         return jsonify({'trace': traceback.format_exc()})     
