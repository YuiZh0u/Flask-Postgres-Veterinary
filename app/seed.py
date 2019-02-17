# coding=utf-8
from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()

sql ="""
INSERT INTO clientes(rut,nombre,telefono,direccion,email) 
values ('19990099-9','First',54535251,'Street 31','first@iron.cl');
INSERT INTO clientes(rut,nombre,telefono,direccion,email) 
values ('9876543-2','Saurfang',998877661,'Street 11','saur@fang.g');
INSERT INTO clientes(rut,nombre,telefono,direccion,email) 
values ('19480440-K','Emilio de la Horda',984287771,'Street 66','emilio@ast.gg');
INSERT INTO clientes(rut,nombre,telefono,direccion,email) 
values ('15550330-8','Shakira Card Raptor',80110987,'Street 7','shakira@card.raptor');
INSERT INTO clientes(rut,nombre,telefono,direccion,email) 
values ('11010110-1','Free the Calo',75620011,'Street 10','free@the.calo');
INSERT INTO clientes(rut,nombre,telefono,direccion,email) 
values ('18927838-1','Khal Drogo',855893821,'Street 117','ilove@daenerys.ever');
INSERT INTO clientes(rut,nombre,telefono,direccion,email) 
values ('9899770-K','Jhon Teaborta',93301100,'Street 33','jhon.teaborta@gmail.com');
"""
cur.execute(sql)



sql ="""INSERT INTO mascotas(nombre,sexo,tipo,raza,fecha_registro,cliente_rut) values 
('Luna','Hembra','Gato','Bombay','2018-11-08','19990099-9');
INSERT INTO mascotas(nombre,sexo,tipo,raza,fecha_registro,cliente_rut) values 
('Thrall','Macho','Perro','Shiba Inu','2018-08-12','19480440-K');
INSERT INTO mascotas(nombre,sexo,tipo,raza,fecha_registro,cliente_rut) values 
('Anastacio','Macho','Gato','Sphynx','2018-08-19','9876543-2');
INSERT INTO mascotas(nombre,sexo,tipo,raza,fecha_registro,cliente_rut) values 
('Lala','Hembra','Perro','Labrador','2018-08-18','11010110-1');
INSERT INTO mascotas(nombre,sexo,tipo,raza,fecha_registro,cliente_rut) values 
('Malfurion','Macho','Perro','Shiba Inu','2018-08-19','11010110-1');
INSERT INTO mascotas(nombre,sexo,tipo,raza,fecha_registro,cliente_rut) values 
('Tyrande','Hembra','Gato','Sphynx','2018-08-20','11010110-1');
INSERT INTO mascotas(nombre,sexo,tipo,raza,fecha_registro,cliente_rut) values 
('Balto','Macho','Perro','Husky siberiano','2018-08-15','15550330-8');
INSERT INTO mascotas(nombre,sexo,tipo,raza,fecha_registro,cliente_rut) values 
('Zico Killer','Macho','Gato','Ragdoll','2018-08-15','9899770-K');
"""
cur.execute(sql)


sql ="""INSERT INTO serviciosmedicos(nombre,descripcion) values 
('Procedimientos Quirurgicos','Cirugia');
INSERT INTO serviciosmedicos(nombre,descripcion) 
values ('Esterilizacion','Extirpación de organos sexuales');
INSERT INTO serviciosmedicos(nombre,descripcion) values
('Vacuna','Vacuna antirrabica');
INSERT INTO serviciosmedicos(nombre,descripcion) values
('Consulta','Servcio de consulta para animales');"""
cur.execute(sql)

sql="""INSERT INTO medicamentos(codigo,nombre,tipo,tamano,cantidad,lab_id) 
values (1,'Antirrabica','Vacuna','25 mL', 3 ,1);
"""
cur.execute(sql)

sql="""INSERT INTO laboratorios(nombre,direccion,telefono) 
values ('Laboratorios Rankawaii','Street 15',981238765);"""
cur.execute(sql)

sql="""INSERT INTO tiene(cliente_rut,mascota_id) values ('11010110-1',4);
INSERT INTO tiene(cliente_rut,mascota_id) values ('11010110-1',5);
INSERT INTO tiene(cliente_rut,mascota_id) values ('11010110-1',6); 
INSERT INTO tiene(cliente_rut,mascota_id) values ('9876543-2',3);
INSERT INTO tiene(cliente_rut,mascota_id) values ('19480440-K',2);
INSERT INTO tiene(cliente_rut,mascota_id) values ('19990099-9',1);
INSERT INTO tiene(cliente_rut,mascota_id) values ('15550330-8',7);
INSERT INTO tiene(cliente_rut,mascota_id) values ('9899770-K',8);
"""
cur.execute(sql)

sql="""INSERT INTO asisten(cliente_rut,mascota_id,servicio_id,fecha_atencion,descripcion_atencion) 
values ('19990099-9',1,2,'2018-11-08','Esterilizacion de gata');
INSERT INTO asisten(cliente_rut,mascota_id,servicio_id,fecha_atencion,descripcion_atencion) 
values ('9876543-2',3,3,'2018-08-19','Vacuna antirrabica para gato');
INSERT INTO asisten(cliente_rut,mascota_id,servicio_id,fecha_atencion,descripcion_atencion) 
values ('19990099-9',1,4,'2018-11-19','Revision de Esterilización');
INSERT INTO asisten(cliente_rut,mascota_id,servicio_id,fecha_atencion,descripcion_atencion) 
values ('9876543-2',3,1,'2018-08-20','Operacion de rinon');
INSERT INTO asisten(cliente_rut,mascota_id,servicio_id,fecha_atencion,descripcion_atencion) 
values ('9876543-2',3,4,'2018-08-19','Revision del riñon');
"""
cur.execute(sql)

sql="""INSERT INTO compra(cliente_rut,codigo_medicamento,fecha_compra) values
('11010110-1',1,'2018-08-18');
"""
cur.execute(sql)

sql="""INSERT INTO suministra(lab_id,codigo_medicamento,fecha_pedido) 
values (1,1,'2018-08-12');
"""
cur.execute(sql)

conn.commit()
cur.close()
conn.close()