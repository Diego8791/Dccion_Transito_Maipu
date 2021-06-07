#!/usr/bin/env python
'''
.............
.............
---------------------------
Autor: 
Version: 

Descripcion:
Programa creado...
'''

__author__ = "...."
__email__ = "...."
__version__ = "....."


import mysql.connector


def create_databases():

    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    # eliminar bases de datos si existen
    cursor.execute('DROP DATABASE IF EXISTS dccion_transito_db')
    cursor.execute('DROP DATABASE IF EXISTS users_db')
    
    # crea bases de datos
    cursor.execute('CREATE DATABASE dccion_transito_db')   
    cursor.execute('CREATE DATABASE users_db')

    # cerrar la conección
    conn.close()

def create_schema_datos_grales_acc_db():

    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='dccion_transito_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()
      
    # Eliminar tablas si existen
    cursor.execute('DROP TABLE IF EXISTS `datos_grales`')
    
    
    # cursor.execute('DROP TABLE IF EXISTS `departamentos`')
    # cursor.execute('DROP TABLE IF EXISTS `distritos`')
    # cursor.execute('DROP TABLE IF EXISTS `distritos_maipu`')
    # cursor.execute('DROP TABLE IF EXISTS `fran_etaria`')
    # cursor.execute('DROP TABLE IF EXISTS `lesiones`')
    # cursor.execute("DROP TABLE IF EXISTS `marca_rodado`")
    # cursor.execute("DROP TABLE IF EXISTS `modelo_rodado`")
    # cursor.execute('DROP TABLE IF EXISTS `nacionalidades`')
    # cursor.execute('DROP TABLE IF EXISTS `perito`')
    # cursor.execute('DROP TABLE IF EXISTS `provincias`')
    # cursor.execute('DROP TABLE IF EXISTS `tipo`')
    # cursor.execute('DROP TABLE IF EXISTS `tomado_en`')
    cursor.execute('DROP TABLE IF EXISTS `participe`')
    # cursor.execute('DROP TABLE IF EXISTS `padron`')
    # cursor.execute('DROP TABLE IF EXISTS `rodado`')
    # cursor.execute('DROP TABLE IF EXISTS `datos_grales_acc`')

    # crear tabla departamentos
    sql = '''CREATE TABLE IF NOT EXISTS `departamentos` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `n_departamento` VARCHAR(100) NOT NULL,
        `region` VARCHAR(100) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)

    # crear tabla distritos
    sql = '''CREATE TABLE IF NOT EXISTS `distritos` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `n_distrito` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)
    
    # crear tabla distritos_maipu
    sql = '''CREATE TABLE IF NOT EXISTS `distritos_maipu` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `n_distritos_maipu` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)

    # crear tabla fran_etaria
    sql = '''CREATE TABLE IF NOT EXISTS `fran_etaria` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `franja` VARCHAR(40) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)

    # crear tabla lesiones
    sql = '''CREATE TABLE IF NOT EXISTS `lesiones` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `con_sin_les` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)
    
    # crear tabla marca_rodado  
    sql = '''CREATE TABLE IF NOT EXISTS `marca_rodado` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `marca` VARCHAR(30) NOT NULL,
            PRIMARY KEY (`id`))
            ENGINE = InnoDB;'''
    cursor.execute(sql)
   
    # Crear tabla modelo_rodado
    sql = '''CREATE TABLE IF NOT EXISTS `modelo_rodado` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `modelo` VARCHAR(100) NOT NULL,
            PRIMARY KEY (`id`))
            ENGINE = InnoDB;'''
    cursor.execute(sql)
    
    # crear tabla nacionalidades
    sql = '''CREATE TABLE IF NOT EXISTS `nacionalidades` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `nacionalidad` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)
    
    # crear tabla perito
    sql = '''CREATE TABLE IF NOT EXISTS `perito` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `perito` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)

    # crear tabla provincias
    sql = '''CREATE TABLE IF NOT EXISTS `provincias` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `provincia` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)
    
    # crear tabla tipo
    sql = '''CREATE TABLE IF NOT EXISTS `tipo` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `acc_tipo` VARCHAR(100) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)

     # crear tabla tomado_en
    sql = '''CREATE TABLE IF NOT EXISTS `tomado_en` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `lugar` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)
    
    # crear tabla padron
    sql = '''CREATE TABLE IF NOT EXISTS `padron` (
        `id` INT AUTO_INCREMENT,
        `nombre` VARCHAR(45) NOT NULL,
        `tipo_doc` VARCHAR(10) NOT NULL,
        `n_doc` INT NOT NULL,
        `sexo` VARCHAR(2) NOT NULL,
        `f_nacimiento` VARCHAR(10) NOT NULL,
        `e_civil` INT NOT NULL,
        `cuil` VARCHAR(15),
        `domicilio` VARCHAR(70) NOT NULL,
        `fk_distrito_id` INT,
        `fk_depto_id` INT,
        `fk_pcia_id` INT,
        `fk_nacion_id` INT,
        `cod_postal` VARCHAR(15) NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `fk_distrito_id`
            FOREIGN KEY (`fk_distrito_id`)
            REFERENCES `distritos` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_depto_id`
            FOREIGN KEY (`fk_depto_id`)
            REFERENCES `departamentos` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_pcia_id`
            FOREIGN KEY (`fk_pcia_id`)
            REFERENCES `provincias` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_nacion_id`
            FOREIGN KEY (`fk_nacion_id`)
            REFERENCES `nacionalidades` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;'''
    cursor.execute(sql)
    
    # crear tabla rodado
    sql = '''CREATE TABLE IF NOT EXISTS `rodado` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `patente` VARCHAR(15) NOT NULL,
            `fk_marca_id` INT NOT NULL,
            `fk_modelo_id` INT NOT NULL,
            PRIMARY KEY (`id`),
            CONSTRAINT `fk_marca_id`
                FOREIGN KEY (`fk_marca_id`)
                REFERENCES `marca_rodado` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
            CONSTRAINT `fk_modelo_id`
                FOREIGN KEY (`fk_modelo_id`)
                REFERENCES `modelo_rodado` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
            ENGINE = InnoDB;'''
    cursor.execute(sql)
    
    # crear tabla participe
    sql = '''CREATE TABLE IF NOT EXISTS `participe` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `n_acc` INT NOT NULL,
        `dtv` VARCHAR(2) NOT NULL,
        `lic_conducir` VARCHAR(30) NULL,
        `fk_n_doc_id` INT NOT NULL,
        `fk_fran_etaria` INT NOT NULL,
        `fk_rodado_id` INT NULL,
        `alcoholemia` VARCHAR(30) NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `fk_fran_etaria`
            FOREIGN KEY (`fk_fran_etaria`)
            REFERENCES `fran_etaria` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_n_doc_id`
            FOREIGN KEY (`fk_n_doc_id`)
            REFERENCES `padron` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_rodado_id`
            FOREIGN KEY (`fk_rodado_id`)
            REFERENCES `rodado` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;'''
    cursor.execute(sql)

    # crear tabla datos_grales_acc
    sql = '''CREATE TABLE IF NOT EXISTS `datos_grales_acc` (
        `n_acc` INT NOT NULL,
        `fecha` VARCHAR(10) NOT NULL,
        `hora` VARCHAR(6) NOT NULL,
        `direccion` VARCHAR(100) NOT NULL,
        `fk_distrito_maipu_id` INT NOT NULL,
        `fk_perito_id` INT NOT NULL,
        `fk_tomado_en_id` INT NOT NULL,
        `fk_tipo_id` INT NOT NULL,
        `fk_lesiones_id` INT NOT NULL,
        `obs` VARCHAR(150) NULL,
        `latitud` FLOAT NULL,
        `longitud` FLOAT NULL,
        PRIMARY KEY (`n_acc`),
        CONSTRAINT `fk_distrito_maipu_id`
            FOREIGN KEY (`fk_distrito_maipu_id`)
            REFERENCES `distritos_maipu` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_perito_id`
            FOREIGN KEY (`fk_perito_id`)
            REFERENCES `perito` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_tomado_en_id`
            FOREIGN KEY (`fk_tomado_en_id`)
            REFERENCES `tomado_en` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_lesiones_id`
            FOREIGN KEY (`fk_lesiones_id`)
            REFERENCES `lesiones` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_tipo_id`
            FOREIGN KEY (`fk_tipo_id`)
            REFERENCES `tipo` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;'''
    cursor.execute(sql)
    
    # cerrar la conección
    conn.close()


def create_schema_users_db():

    # establecer la conección
    conn = mysql.connector.connect(user='username', password='password', host='localhost', database='users_db')
    # crear objeto cursor usando el método cursor()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS `users`')
    cursor.execute('DROP TABLE IF EXISTS `type_users`')

    # crear tabla type_users
    sql = '''CREATE TABLE IF NOT EXISTS `type_users` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `type_users` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`))
        ENGINE = InnoDB;'''
    cursor.execute(sql)

    # crear tabla users
    sql = '''CREATE TABLE IF NOT EXISTS `users` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(30) NOT NULL,
        `password` VARCHAR(30) NOT NULL,
        `e_mail` VARCHAR(100) NOT NULL,
        `fk_type_user_id` INT NOT NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `fk_type_user_id`
            FOREIGN KEY (`fk_type_user_id`)
            REFERENCES `type_users` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;'''
    cursor.execute(sql)

    # cerrar la conección
    conn.close()
    

if __name__ == '__main__':

    # create_databases()
    create_schema_datos_grales_acc_db()
    # create_schema_users_db()