# coding=utf-8
from app import app
from flask import render_template,request,redirect
from configuraciones import *

import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()


@app.route('/')

@app.route('/mascotas')
def mascotas():
	sql="""SELECT id, mascotas.nombre, tipo, sexo, raza, fecha_registro, clientes.nombre
			FROM mascotas LEFT JOIN clientes ON mascotas.cliente_rut = clientes.rut
			ORDER BY mascotas.id ASC"""
	cur.execute(sql)
	mascotas  = cur.fetchall()

	sql="select distinct fecha_registro from mascotas"
	cur.execute(sql)
	fechas  = cur.fetchall()

	return render_template("mascotas.html",mascotas = mascotas, fechas = fechas)

@app.route('/clientes')
def clientes():
	sql="select * from clientes"
	cur.execute(sql)
	clientes  = cur.fetchall()

	return render_template("clientes.html",clientes = clientes)

@app.route('/inventario')
def inventario():
	sql="""SELECT codigo, medicamentos.nombre, cantidad, tamano, tipo, laboratorios.nombre
			FROM medicamentos LEFT JOIN laboratorios ON medicamentos.lab_id = laboratorios.id
			ORDER BY codigo ASC"""
	cur.execute(sql)
	medicamentos  = cur.fetchall()
	
	sql="select distinct cantidad from medicamentos"
	cur.execute(sql)
	cantidads  = cur.fetchall()

	sql="select distinct tamano from medicamentos"
	cur.execute(sql)
	tamanos  = cur.fetchall()

	sql="select distinct tipo from medicamentos"
	cur.execute(sql)
	tipos  = cur.fetchall()

	return render_template("inventario.html", medicamentos = medicamentos, cantidads = cantidads, 
	tamanos = tamanos, tipos=tipos)

@app.route('/laboratorio')
def laboratorios():
	sql="select * from laboratorios"
	cur.execute(sql)
	laboratorios  = cur.fetchall()
	return render_template("laboratorios.html",nombre="nombre",laboratorios = laboratorios)

@app.route('/procedimientos')
def procedimientos():
	sql="select * from serviciosmedicos"
	cur.execute(sql)
	serviciosmedicos  = cur.fetchall()

	return render_template("procedimientos.html",serviciosmedicos = serviciosmedicos)

@app.route('/ventas')
def ventas():
	sql = """SELECT compra.cliente_rut, compra.codigo_medicamento, clientes.nombre, medicamentos.nombre, compra.fecha_compra
            FROM compra LEFT JOIN medicamentos ON compra.codigo_medicamento = medicamentos.codigo 
            LEFT JOIN clientes ON compra.cliente_rut = clientes.rut ORDER BY cliente_rut ASC"""
	cur.execute(sql)
	compras  = cur.fetchall()

	sql="select distinct fecha_compra from compra"
	cur.execute(sql)
	fechas  = cur.fetchall()

	return render_template("ventas.html",compras = compras, fechas = fechas)

@app.route('/suministra')
def pedidos():
	cur = conn.cursor()
	sql="""SELECT suministra.lab_id, suministra.codigo_medicamento, suministra.fecha_pedido, medicamentos.nombre, laboratorios.nombre
			FROM suministra LEFT JOIN medicamentos ON suministra.codigo_medicamento = medicamentos.codigo LEFT JOIN laboratorios
			ON suministra.lab_id = laboratorios.id"""
	cur.execute(sql)
	suministra  = cur.fetchall()

	sql="select distinct fecha_pedido from suministra"
	cur.execute(sql)
	fechas  = cur.fetchall()

	return render_template("pedidos.html",suministra = suministra,fechas=fechas)

@app.route('/visitas')
def asisten():
	
	cur = conn.cursor()
	sql = """SELECT cliente_rut, mascota_id, servicio_id, serviciosmedicos.nombre,fecha_atencion, descripcion_atencion
			FROM asisten LEFT JOIN serviciosmedicos ON asisten.servicio_id = serviciosmedicos.id """
	cur.execute(sql)
	asisten = cur.fetchall()
	conn.commit()
	cur.close()
	return render_template('visitas.html',asisten = asisten)

@app.route('/tiene')
def tiene():
	sql="select * from tiene"
	cur.execute(sql)
	tiene  = cur.fetchall()
	return render_template("tiene.html",tiene = tiene)
	

@app.route("/agregarmascota", methods=['GET','POST'])
def crear():
	if request.method == 'POST':
		Rut =  request.form['RUTCliente']
		checkbox = request.form.get('ELCLI')
		
		if checkbox == None:
			Nombre = request.form['NombreCliente']
			Telefono = request.form['FonoCliente']
			Direccion = request.form['DirecciónCliente']
			Email = request.form['MailCliente']
			cur = conn.cursor()
			sql = """INSERT INTO clientes (rut,nombre,telefono,direccion,email) 
					VALUES ('%s','%s','%s','%s','%s') ;""" %(Rut,Nombre,Telefono,Direccion,Email)
			cur.execute(sql)
			conn.commit()
			cur.close()

		Nombre_mascota = request.form['NombreMascota']
		Sexo = request.form['SexoMascota']
		Tipo = request.form['TipoMascota']
		Raza = request.form['RazaMascota']
		fecha = 'CURRENT_DATE'
		cur = conn.cursor()
		sql = """INSERT INTO mascotas(nombre,sexo,tipo,raza,cliente_rut,fecha_registro) 
				VALUES ('%s','%s','%s','%s','%s',%s) ;""" %(Nombre_mascota,Sexo,Tipo,Raza,Rut,fecha)
		cur.execute(sql)
		conn.commit()
		cur.close()
	return render_template("formulariomascota.html", nombre="nombre")
	


@app.route("/agregarmedicamento", methods=['GET', 'POST'])
def agregarmedicamento():
	if request.method == 'POST':
		checkbox = request.form.get('ELCLI')

		if checkbox == None:
			Nombre = request.form['NombreLab']
			Telefono = request.form['FonoLab']
			Direccion = request.form['DireccionLab']
			cur = conn.cursor()
			sql = """INSERT INTO laboratorios (nombre,telefono,direccion) 
					VALUES ('%s',%s,'%s') ;""" %(Nombre,Telefono,Direccion)
			cur.execute(sql)
			conn.commit()
			cur.close()

		cur = conn.cursor()
		sql = """SELECT max(id) FROM laboratorios;"""
		cur.execute(sql)
		Lab = cur.fetchone()
		Lab = int(Lab[0])
		conn.commit()
		cur.close()
		if checkbox == 'hola':
			print(checkbox)
			Lab = request.form['IDLab']

		Codigo = request.form['CodigoMed']
		Nombre =  request.form['NombreMed']
		Tipo = request.form['TipoMed']
		Tamano = request.form['TamanoMed']
		Cantidad = request.form['CantMed']
		cur = conn.cursor()
		sql = """INSERT INTO medicamentos(codigo,nombre,tipo,tamano,cantidad,lab_id) 
				VALUES (%s,'%s','%s','%s',%s,%s) ;""" %(Codigo,Nombre,Tipo,Tamano,Cantidad,Lab)
		cur.execute(sql)
		conn.commit()
		cur.close()

	return render_template("agregarinventario.html",nombre="nombre")

@app.route("/agregarvisita", methods=['GET','POST'])
def visitandoahora():
	if request.method == 'POST':
		Mascota =  request.form['IDMascota']
		Rut = request.form['RUTCliente']
		Servicio = request.form['IDServicio']
		Desc = request.form['DescAtencion']
		Fecha = 'CURRENT_DATE'
		cur = conn.cursor()
		sql = """INSERT INTO asisten(mascota_id,cliente_rut,servicio_id,fecha_atencion,descripcion_atencion) 
				VALUES (%s,'%s',%s,%s,'%s') ;""" %(Mascota,Rut,Servicio,Fecha,Desc)
		cur.execute(sql)
		conn.commit()
		cur.close()
	return render_template("agregarvisita.html")

@app.route('/agregarprocedimiento', methods=['GET', 'POST'])
def agregarprocedimiento():
	if request.method == 'POST':
		Nombre =  request.form['NombreProcedimiento']
		Descripcion = request.form['DescAtencion']
		cur = conn.cursor()
		sql = """INSERT INTO serviciosmedicos (nombre,descripcion) 
				values ('%s','%s') ;""" %(Nombre,Descripcion)
		cur.execute(sql)
		conn.commit()
		cur.close()

	return render_template("agregarprocedimiento.html",nombre="nombre",mascota="mascota")

@app.route('/agregarpedido', methods=['GET', 'POST'])
def agregarpedido():
	if request.method == 'POST':
		checkbox = request.form.get('ELCLI')

		if checkbox == None:
			Nombre = request.form['NombreLab']
			Telefono = request.form['FonoLab']
			Direccion = request.form['DireccionLab']
			cur = conn.cursor()
			sql = """INSERT INTO laboratorios (nombre,telefono,direccion) 
					VALUES ('%s',%s,'%s') ;""" %(Nombre,Telefono,Direccion)
			cur.execute(sql)
			conn.commit()
			cur.close()

		cur = conn.cursor()
		sql = """SELECT max(id) FROM laboratorios;"""
		cur.execute(sql)
		Lab = cur.fetchone()
		Lab = int(Lab[0])
		conn.commit()
		cur.close()
		if checkbox == 'hola':
			print(checkbox)
			Lab = request.form['IDLab']

		Medicamento = request.form['CodMedicamento']
		Fecha = 'CURRENT_DATE'
		cur = conn.cursor()
		sql = """INSERT INTO suministra(lab_id,codigo_medicamento,fecha_pedido) 
				VALUES (%s,%s,%s) ;""" %(Lab,Medicamento,Fecha)
		cur.execute(sql)
		conn.commit()
		cur.close()

		cur = conn.cursor()
		sql = """UPDATE medicamentos SET cantidad = cantidad + 1 
				WHERE codigo = (%s) ;""" %(Medicamento)
		cur.execute(sql)
		conn.commit()
		cur.close()
	return render_template("agregarpedidos.html",nombre="nombre",mascota="mascota")

@app.route('/agregarventa', methods=['GET', 'POST'])
def crearventa():
	if request.method == 'POST':
		Rut =  request.form['RUTCliente']
		checkbox = request.form.get('ELCLI')

		if checkbox == None:
			Nombre = request.form['NombreCliente']
			Telefono = request.form['FonoCliente']
			Direccion = request.form['DirecciónCliente']
			Email = request.form['MailCliente']
			cur = conn.cursor()
			sql = """INSERT INTO clientes (rut,nombre,telefono,direccion,email) 
					VALUES ('%s','%s','%s','%s','%s') ;""" %(Rut,Nombre,Telefono,Direccion,Email)
			cur.execute(sql)
			conn.commit()
			cur.close()

		Medicamento = request.form['CodMedicamento']
		Fecha = 'CURRENT_DATE'
		cur = conn.cursor()
		sql = """INSERT INTO compra(cliente_rut,codigo_medicamento,fecha_compra) 
				VALUES ('%s',%s,%s) ;""" %(Rut,Medicamento,Fecha)
		cur.execute(sql)
		conn.commit()
		cur.close()

		cur = conn.cursor()
		sql = """UPDATE medicamentos SET cantidad = cantidad - 1 
				WHERE codigo = (%s) ;""" %(Medicamento)
		cur.execute(sql)
		conn.commit()
		cur.close()

	return render_template("agregarventa.html",nombre="nombre",mascota="mascota")

@app.route('/mascota/<id>', methods=['GET', 'POST'])
def modificarmascotas(id):
	if request.method == 'POST':
		nombre =  request.form['NombreMascota']
		sexo =  request.form['SexoMascota']
		animal =  request.form['TipoMascota']
		raza =  request.form['RazaMascota']
		sql = """ update mascotas set nombre = '%s', sexo = '%s',tipo = '%s',raza = '%s'
		where id = %s """%(nombre,sexo,animal,raza,id)
		cur.execute(sql)
		conn.commit()
	else:
		sql ="""
		select *
		from mascotas,clientes
		where mascotas.cliente_rut = clientes.rut
		and mascotas.id = %s order by id desc
		"""%(id)
		print(sql)
		cur.execute(sql)
		mascota  = cur.fetchone()
		return render_template("modificarmascota.html",mascota= mascota) 
	return redirect("/mascotas")

@app.route('/cliente/<rut>', methods=['GET', 'POST'])
def modificarcliente(rut):
	if request.method == 'POST':
		nombre =  request.form['NombreCliente']
		fono =  request.form['FonoCliente']
		direccion =  request.form['DireccionCliente']
		email =  request.form['MailCliente']
		sql = """ update clientes set nombre = '%s', telefono = '%s',direccion = '%s',email = '%s'
		where rut = '%s' """%(nombre,fono,direccion,email,rut)
		cur.execute(sql)
		conn.commit()
	else:
		sql ="""
		select *
		from clientes
		where clientes.rut = '%s'
		"""%(rut)
		print(sql)
		cur.execute(sql)
		cliente  = cur.fetchone()
		return render_template("modificarcliente.html",cliente= cliente) 
	return redirect("/clientes")

@app.route('/inventario/<codigo>', methods=['GET', 'POST'])
def modificarmedicamento(codigo):
	if request.method == 'POST':
		nombre =  request.form['NombreMed']
		cantidad =  request.form['CantMed']
		tamano =  request.form['TamanoMed']
		tipo =  request.form['TipoMed']
		labid = request.form['IDLab']
		sql = """ update medicamentos set nombre = '%s', cantidad = '%s',tamano = '%s',tipo = '%s',lab_id = '%s'
		where codigo = %s """%(nombre,cantidad,tamano,tipo,labid,codigo)
		cur.execute(sql)
		conn.commit()
	else:
		sql ="""
		select *
		from medicamentos
		where medicamentos.codigo = %s order by codigo desc
		"""%(codigo)
		print(sql)
		cur.execute(sql)
		inventario  = cur.fetchone()
		return render_template("modificarinventario.html",inventario= inventario)
	return redirect("/inventario")

@app.route('/laboratorio/<id>', methods=['GET', 'POST'])
def modificarlab(id):
	if request.method == 'POST':
		nombre =  request.form['NombreLab']
		direccion =  request.form['DireccionLab']
		telefono =  request.form['FonoLab']
		sql = """ update laboratorios set nombre = '%s', direccion = '%s',telefono = '%s'
		where id = %s """%(nombre,direccion,telefono,id)
		cur.execute(sql)
		conn.commit()
	else:
		sql ="""
		select *
		from laboratorios
		where laboratorios.id = %s order by id desc
		"""%(id)
		print(sql)
		cur.execute(sql)
		laboratorio  = cur.fetchone()
		return render_template("modificarlaboratorio.html",laboratorio= laboratorio)
	return redirect("/laboratorio")

@app.route('/procedimiento/<id>', methods=['GET', 'POST'])
def modificarprocedimiento(id):
	if request.method == 'POST':
		nombre =  request.form['NombreProcedimiento']
		desc =  request.form['DescAtencion']
		sql = """ update serviciosmedicos set nombre = '%s', descripcion = '%s'
		where id = %s """%(nombre,desc,id)
		cur.execute(sql)
		conn.commit()
	else:
		sql ="""
		select *
		from serviciosmedicos
		where serviciosmedicos.id = %s order by id desc
		"""%(id)
		print(sql)
		cur.execute(sql)
		procedimiento  = cur.fetchone()
		return render_template("modificarprocedimiento.html",procedimiento= procedimiento)
	return redirect("/procedimientos")


@app.route('/visita/<rut>/<mascota>/<servicio>/<fecha>', methods=['GET', 'POST'])
def stemen(rut,mascota,servicio,fecha):
	return render_template('modificarvisita.html')

@app.route('/visita/modificar',methods=['GET', 'POST'])
def modificarvisitas():
	if request.method == 'POST':
		Mascota =  request.form['IDMascota']
		Rut = request.form['RUTCliente']
		Servicio = request.form['IDServicio']
		Desc = request.form['DescAtencion']
		Fecha = request.form['FechaAten']
		conn = psycopg2.connect("dbname=veterinaria user=postgres password=lalilulelo1994")
		cur = conn.cursor()
		sql = """UPDATE asisten set cliente_rut = '%s', mascota_id = %s, servicio_id = %s, fecha_atencion = '%s',
				descripcion_atencion = ('%s')
				WHERE asisten.cliente_rut ='%s' and asisten.mascota_id = %s and asisten.fecha_atencion = '%s'
				  ;""" %(Rut,Mascota,Servicio,Fecha,Desc,Rut,Mascota,Fecha)

		print(sql)
		cur.execute(sql)
		conn.commit()
		cur.close()
		return redirect("/mascotas")
	
@app.route('/mascotaborrar/<id>', methods=['GET', 'POST'])
def mascotaborrar(id):
	sql ="""
		delete from mascotas where id = %s
	"""%(id)
	print sql
	cur.execute(sql)
	conn.commit()
	return  redirect(request.referrer)

@app.route('/procedimientoborrar/<id>', methods=['GET', 'POST'])
def procedimientoborrar(id):
	sql ="""
		delete from serviciosmedicos where id = %s
	"""%(id)
	print sql
	cur.execute(sql)
	conn.commit()
	return  redirect(request.referrer)

@app.route('/inventarioborrar/<id>', methods=['GET', 'POST'])
def inventarioborrar(id):
	sql ="""
		delete from medicamentos where codigo = %s
	"""%(id)
	print sql
	cur.execute(sql)
	conn.commit()
	return  redirect(request.referrer)

@app.route('/ventaborrar/<rut>/<codigo>', methods=['GET', 'POST'])
def ventaborrar(rut,codigo):
	sql ="""
		delete from compra where cliente_rut = '%s' and codigo_medicamento = %s
	"""%(rut,codigo)
	print sql
	cur.execute(sql)
	conn.commit()
	return  redirect(request.referrer)

@app.route('/pedidoborrar/<labid>/<codigo>', methods=['GET', 'POST'])
def pedidoborrar(labid,codigo):
	sql ="""
		delete from suministra where lab_id = %s and codigo_medicamento = %s
	"""%(labid,codigo)
	print sql
	cur.execute(sql)
	conn.commit()
	return  redirect(request.referrer)

@app.route('/visitasborrar/<rut>/<mascotaid>/<servicioid>/<fecha>', methods=['GET', 'POST'])
def visitasborrar(rut,mascotaid,servicioid,fecha):
	sql ="""
		delete from asisten where cliente_rut = '%s' and mascota_id = %s and servicio_id = %s and fecha_atencion = '%s'
	"""%(rut,mascotaid,servicioid,fecha)
	print sql
	cur.execute(sql)
	conn.commit()
	return  redirect(request.referrer)

@app.route('/visita/<id>', methods=['GET', 'POST'])
def vervisitas(id):
	cur = conn.cursor()
	sql = """SELECT cliente_rut, mascota_id, servicio_id, serviciosmedicos.nombre,fecha_atencion, descripcion_atencion
			FROM asisten LEFT JOIN serviciosmedicos ON asisten.servicio_id = serviciosmedicos.id 
			WHERE asisten.mascota_id = %s"""%(id)
	cur.execute(sql)
	asisten = cur.fetchall()
	conn.commit()
	cur.close()
	return render_template('visitas.html',asisten = asisten)