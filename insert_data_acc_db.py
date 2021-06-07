import sqlite3
import json

def insert_gral_data():
    '''
    Se ingresa un registro en la base de datos accidentologia_db, tabla gral_data
    '''
    
    # Obtener latitud y longitud     
        lat, lng = my_geo.adress_locations(adress)
    
    #imprimir la lista con los datos normalizados
    print(list_data)
    
    # Abrir base de datos
    conn = sqlite3.connect('accidentologia_db')
    cur = conn.cursor()
        
    # Registrar en base de datos
    cur.execute('''
                INSERT OR IGNORE INTO datos_grales 
                    (n_acc, fecha, hora, direccion, fk_distrito_id, fk_perito_id, 
                    fk_tomado_en_id, fk_tipo_id, fk_lesiones_id, obs, latitud, longitud)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?) 
                    ''', list_data)
    
    # conn.commit()
    # Cerrar base de datos
    conn.close()


def insert_participe():

    conn = sqlite3.connect('accidentologia_db')
    cur = conn.cursor()
    
    cur.execute('''
                INSERT INTO participe 
                    (n_acc, dtv, fk_n_doc_id, lic_conducir, fk_fran_etaria, fk_patente_id, alcoholemia) 
                    VALUES (?,?,?,?,?,?,?) 
                    ''', (list_data))
    print('Ingreso exitoso!!', list_data)

    # conn.commit()
    # cerrar base de datos
    conn.close()
