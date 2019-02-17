from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))


cur = conn.cursor()
sql ="""DROP SCHEMA public CASCADE;
CREATE SCHEMA public;"""

cur.execute(sql)

sql ="""
CREATE TABLE clientes(
    rut varchar(40) NOT NULL PRIMARY KEY, 
    nombre varchar(40), 
    telefono integer, 
    direccion varchar(100),
    email varchar(100)
    );
"""
cur.execute(sql)

sql ="""
CREATE TABLE mascotas(
    id serial NOT NULL PRIMARY KEY, 
    nombre varchar(40), 
    sexo varchar(40), 
    tipo varchar(40),
    raza varchar(40),
    fecha_registro date,
    cliente_rut varchar(40)
    );
"""
cur.execute(sql)

sql ="""
CREATE TABLE medicamentos(
    codigo integer NOT NULL PRIMARY KEY, 
    nombre varchar(40),
    cantidad integer, 
    tamano varchar(40),
    tipo varchar(40),
    lab_id integer
    );
"""
cur.execute(sql)

sql ="""
CREATE TABLE laboratorios(
    id serial NOT NULL PRIMARY KEY, 
    nombre varchar(40),
    direccion varchar(100),
    telefono integer
    );
"""
cur.execute(sql)

sql ="""
CREATE TABLE serviciosmedicos(
    id serial NOT NULL PRIMARY KEY, 
    nombre varchar(40), 
    descripcion varchar(255)
    );
"""
cur.execute(sql)

sql ="""
CREATE TABLE suministra(
    lab_id integer, 
    codigo_medicamento integer, 
    fecha_pedido date
    );
"""
cur.execute(sql)

sql ="""
CREATE TABLE compra(
    cliente_rut varchar(40), 
    codigo_medicamento integer, 
    fecha_compra date 
    );
"""
cur.execute(sql)

sql ="""
CREATE TABLE tiene(
    cliente_rut varchar(40),
    mascota_id integer
    );
"""
cur.execute(sql)

sql ="""
CREATE TABLE asisten(
    cliente_rut varchar(40),
    mascota_id integer,
    servicio_id integer,
    fecha_atencion date,
    descripcion_atencion varchar(255)   
    );
"""
cur.execute(sql)

conn.commit()
cur.close()
conn.close()