#Server localhost
#Meterse a cd bd
#Para correr el server, en cmd usar: python -m flask run
#Antes poner en cd bd --> set FLASK_APP=server.py

from flask import Flask
from flask import render_template
from flask import request
import os
import psycopg2

app = Flask(__name__)

print('PostgreSQL database version:')
cur = conn.cursor()
cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()
print(db_version)

# close the communication with the PostgreSQL
cur.close()


@app.route("/")
def hello():
	return render_template('index.html')	


@app.route("/agregar")
def crear():
	if request.method == 'POST':
		Rut =  request.form['Rut']
		Nombre = request.form['Nombre']
		Telefono = request.form['Telefono']
		Direccion = request.form['Direccion']
		Email = request.form['Email']

		checkbox = request.form.get('checkbox')
		if checkbox:
			
			cur = conn.cursor()
			sql = """INSERT INTO clientes (rut,nombre,telefono,direccion,email) 
					VALUES (%s,%s,%s,%s,%s) ;""" %(Rut,Nombre,Telefono,Direccion,Email)
			cur.execute(sql)
			conn.commit()
			cur.close()


		Nombre_mascota = request.form['Nombre_mascota']
		Sexo = request.form['Sexo']
		Tipo = request.form['Tipo']
		Raza = request.form['Raza']
		Fecha_registro = request.form['Fecha_registro']

		
		cur = conn.cursor()
		sql = """INSERT INTO mascotas(nombre,sexo,tipo,raza,fecha_registro,cliente_rut) 
				VALUES (%s,%s,%s,%s,%s,%s) ;""" %(Nombre_mascota,Sexo,Tipo,Raza,Fecha_registro,Rut)
		cur.execute(sql)
		conn.commit()
		cur.close()


@app.route("/agregar/venta")
def crearventa():
	if request.method == 'POST':
		Rut =  request.form['Rut']
		Medicamento = request.form['Codigo_medicamento']
		Fecha = request.form['Fecha_compra']
		
		cur = conn.cursor()
		sql = """INSERT INTO compra(cliente_rut,codigo_medicamento,fecha_compra) 
				VALUES (%s,%s,%s) ;""" %(Rut,Medicamento,Fecha)
		cur.execute(sql)
		conn.commit()
		cur.close()

@app.route("/agregar/pedido")
def pedido():
	if request.method == 'POST':
		Lab =  request.form['Lab_id']
		Medicamento = request.form['Codigo_medicamento']
		Fecha = request.form['Fecha_pedido']
		
		cur = conn.cursor()
		sql = """INSERT INTO suministra(lab_id,codigo_medicamento,fecha_pedido) 
				VALUES (%s,%s,%s) ;""" %(Lab,Medicamento,Fecha)
		cur.execute(sql)
		conn.commit()
		cur.close()

@app.route("/agregar/procedimiento")
def procedimiento():
	if request.method == 'POST':
		Nombre =  request.form['Nombre']
		Descripcion = request.form['Descripcion']
		
		cur = conn.cursor()
		sql = """INSERT INTO serviciosmedicos(nombre,descripcion) 
				VALUES (%s,%s) ;""" %(Nombre,Descripcion)
		cur.execute(sql)
		conn.commit()
		cur.close()

@app.route("/modificar/inventario/")
def inventario_modificar():
	return render_template('inventario.html')


@app.route("/modificar/inventario/agregar")
def agregar_inventario():
	if request.method == 'POST':
		Nombre =  request.form['Nombre']
		Tipo = request.form['Tipo']
		Tamano = request.form['Tamano']
		Cantidad = request.form['Cantidad']
		Lab_id = request.form['Lab_id']
		 
		cur = conn.cursor()
		sql = """INSERT INTO medicamentos(nombre,tipo,tamano,cantidad,lab_id) 
				VALUES (%s,%s,%s,%s,%s) ;""" %(Nombre,Tipo,Tamano,Cantidad,Lab_id)
		cur.execute(sql)
		conn.commit()
		cur.close()


@app.route("/modificar/inventario/eliminar")
def eliminar_inventario():
	if request.method == 'POST':
		Codigo = request.form['Codigo_med']
		
		cur = conn.cursor()
		sql = """DELETE 
				FROM medicamentos
				WHERE codigo = %s"""%s(Codigo)
		cur.execute(sql)
		conn.commit()
		cur.close


@app.route("/clientes")
def clientes():
	
	cur = conn.cursor()
	sql = """SELECT DISTINCT *
			FROM clientes"""
	cur.execute(sql)
	row = cur.fetchall()
	conn.commit()
	cur.close()
	return render_template('mostrar.html',row = row)	

@app.route("/ventas")
def ventas():
	
	cur = conn.cursor()
	sql = """SELECT DISTINCT *
			FROM compra"""
	cur.execute(sql)
	row = cur.fetchall()
	conn.commit()
	cur.close()
	return render_template('mostrar.html',row = row)		


@app.route("/pedidos")
def pedidos():
	
	cur = conn.cursor()
	sql = """SELECT DISTINCT *
			FROM suministra"""
	cur.execute(sql)
	row = cur.fetchall()
	conn.commit()
	cur.close()
	return render_template('mostrar.html',row = row)

@app.route("/inventario")
def inventario():
	
	cur = conn.cursor()
	sql = """SELECT DISTINCT *
			FROM medicamentos"""
	cur.execute(sql)
	row = cur.fetchall()
	conn.commit()
	cur.close()
	return render_template('mostrar.html',row = row)


@app.route("/procedimientos")
def procedimientos():
	
	cur = conn.cursor()
	sql = """SELECT DISTINCT *
			FROM serviciosmedicos"""
	cur.execute(sql)
	row = cur.fetchall()
	conn.commit()
	cur.close()
	return render_template('mostrar.html',row = row)


@app.route("/mascotas")
def mascotas():
	
	cur = conn.cursor()
	sql = """SELECT DISTINCT *
			FROM mascotas
			ORDER BY fecha_registro DESC"""
	cur.execute(sql)
	row = cur.fetchall()
	conn.commit()
	cur.close()
	return render_template('mostrar.html',row = row)