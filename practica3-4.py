# encoding: utf-8
import web
from web import form

from web.contrib.template import render_mako

import re

import dbm

import pymongo



db0 = dbm.open('datos.dat', 'c')

web.config.debug = False

urls = (	
	'/cuestionario', 'cuestionario',
	'/periodico/(.*)', 'periodico',
	'/logea', 'logea',
	'/registro', 'registro',
	'/acceder', 'acceder',
	'/salir', 'salir',
	'/muestradatosDBM/(.*)', 'muestradatosDBM',
	'/accederDBM', 'accederDBM',
	'/cambiadatosDBM/(.*)', 'cambiadatosDBM',
	'/muestradatos/(.*)', 'muestradatos',
	'/cambiadatos/(.*)', 'cambiadatos',
	'/rss', 'rss',
	'/buscadorRSS', 'buscadorRSS',
	'/graficas', 'graficas',
	'/mapas', 'mapas',
	'/buscamaps', 'buscamaps',
	'/buscatweet', 'buscatweet',
	'/tweetposicion', 'tweetposicion'
)

app = web.application(urls, globals())

sesion = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'usuario':''})                          
web.config._session = sesion

#Conexión con la BD de mongodb
try:
	conn=pymongo.MongoClient('mongodb://localhost:27017/')
	print "Conexión realizada con éxito."
except pymongo.errors.ConnectionFailure, e:
	print "No se pudo conectar a MongoDB: %s" % e
conn


db = conn.usuarios
db

col = db.datos
col
print conn.database_names()
print db.collection_names()


# Uso de plantillas mako			
plantillas = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8'
        )

#Expresiones regulares para los formularios
validatorEmail = form.regexp(r'\b[a-zA-Z\d._-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,4}\b', '* Correo electrónico no válido.')
validatorVISA = form.regexp(r'([\d]{4}) ([\d]{4}) ([\d]{4}) ([\d]{4})|([\d]{4})-([\d]{4})-([\d]{4})-([\d]{4})', '* Número tarjeta VISA no válido.')

login = form.Form(
	form.Textbox('nombre',required=True,description = "Nombre del usuario:"),
	form.Textbox('apellidos',required=True, description = "Apellidos:"),
	form.Textbox('DNI',required=True),
	form.Textbox('correo_electronico',validatorEmail,required=True, description = "Correo electronico:"),
	form.Dropdown('Dia_de_nacimiento', [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')],required=True, description = "Dia de nacimiento:"),

	form.Dropdown('Mes_de_nacimiento', [('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Ocutbre'), ('11', 'Noviembre'), ('12', 'Diciembre')],required=True, description = "Mes de nacimiento:" ),

	form.Dropdown('Anio_de_nacimiento', [('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'),('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002')],required=True, description = "Anio de nacimiento:"),
	form.Radio('Forma_de_pago', ['contra reembolso ', 'tarjeta VISA', 'paypal'],required=True, description = "Forma de pago:"),
	form.Textbox('numeroVisa',validatorVISA,required=True, description = "Numero de VISA:"),
	form.Textarea('Direccion',required=True),
	form.Password('password',required=True, max_length=7, description = "Introduzca una contrasenia:"),
	form.Password('password2',required=True, description = "Repita la contrasenia:"),
	form.Checkbox("accept_license",
		form.Validator("Acepta las clausulas", lambda i: i == 'true'),
		value='true', description = "Acepta los terminos"
	),
	form.Button('Mandar formulario', type="submit"),
	validators = [form.Validator("Passwords didn't match.", lambda i: i.password == i.password2)],

)


login2 = form.Form(
	form.Textbox('usuario'),
	form.Password('contrasenia'),
	form.Button('Loguearse', type="submit")
	
)


# No la llegamos a llamar, se usaría cuando solicitemos una página a la que no tenemos asociada ninguna clase
class fallo:        
	def GET(self, name):
			return """Error al devolver la pagina, %s no existe  """ % name 




class cuestionario: 
	def GET(self): 
		form = login()
		return """<html><body>
		<form name="input" action="/cuestionario" method="post">
		%s
		</form>
		</body></html>
		""" % (form.render())

	def POST(self): 
		form = login() 
		if not form.validates(): 
			return """<html><body>
			<form name="input" action="/cuestionario" method="post">
			%s
			</form>
			</body></html>
			""" % (form.render())
		else:
			db0["%s"%(form.d.nombre)] = "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % ((form.d.nombre, form.d.apellidos,form.d.password, form.d.DNI, form['correo_electronico'].value, form['Dia_de_nacimiento'].value, form['Mes_de_nacimiento'].value, form['Anio_de_nacimiento'].value, form.d.Direccion, form['Forma_de_pago'].value, form.d.numeroVisa))
			datos = db0["%s"%(form.d.nombre)].split('|')
			#db0.close()
			return """<html><body>
			<form name="input" action="/periodico/" method="post">
			<p> %s  </p>
			<a href="../periodico/%s"> Vuelve a portada</a>
			</form>
			</body></html>
			""" % (str(datos), form.d.nombre)


class muestradatosDBM: 
	def GET (self,name):
		datos = db0[name].split('|')
		return """<html><body>
		<form name="input" action="/periodico/" method="post">
		<p> %s (la contrasenia es %s) </p>
		<a href="../periodico/%s"> Vuelve a portada</a>
		</form>
		</body></html>
		""" % (str(datos), str(datos[2]),name)


class accederDBM:
	def GET(self): 
		form = login2()
		return """<html><body>
		<form name="input" action="/accederDBM" method="post">
		%s
		</form>
		</body></html>
		""" % (form.render())

	def POST(self):
		form = login2()
		if not form.validates():
			return form.render()
		usuario = form.d.usuario
		password = form.d.contrasenia
		
		nuevo = db0[usuario].split('|')

		if password == nuevo[2]:

			return """<html><body>
			<form name="input" action="/accederDBM" method="post">
			<p> %s te has logueado con la contrasenia %s </p>
			<a href="../periodico/%s"> Vuelve a portada</a>
			</form>
			</body></html>
			""" % (usuario, password,usuario)
		else:
			return """<html><body>
			<form name="input" action="/accederDBM" method="post">
			<p> Contrasenia %s incorrecta </p>
			<a href="../periodico/"> Vuelve a portada</a>
			</form>
			</body></html>
			""" % (password)

class cambiadatosDBM: 
	def GET(self, name): 
		form = login()
		datos = db0[name].split('|')
		form.DNI.value = datos[3]
		form.nombre.value = datos[0]
		form.apellidos.value = datos[1]
		return """<html><body>
		<form name="input" action="/cuestionario" method="post">
		<p>Datos actuales son: %s </p> %s
		</form>
		</body></html>
		""" % (str(datos), form.render())

	def POST(self): 
		form = login() 
		if not form.validates(): 
			return """<html><body>
			<form name="input" action="/cuestionario" method="post">
			%s
			</form>
			</body></html>
			""" % (form.render())
		else:
			db0["%s"%(form.d.nombre)] = "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % ((form.d.nombre, form.d.apellidos,form.d.password, form.d.DNI, form['correo_electronico'].value, form['Dia_de_nacimiento'].value, form['Mes_de_nacimiento'].value, form['Anio_de_nacimiento'].value, form.d.Direccion, form['Forma_de_pago'].value, form.d.numeroVisa))
			datos = db0["%s"%(form.d.nombre)].split('|')
			#db0.close()
			return """<html><body>
			<form name="input" action="/periodico/" method="post">
			<p> Nuevos datos: %s  </p>
			<a href="../periodico/%s"> Datos cambiados correctamente, vuelve a portada</a>
			</form>
			</body></html>
			""" % (str(datos), form.d.nombre)




class logea: 
	def GET(self): 
		form = login2()
		return """<html><body>
		<form name="input" action="/logea" method="post">
		%s
		</form>
		</body></html>
		""" % (form.render())

	def POST(self): 
		form = login2() 
		if not form.validates(): 
			return """<html><body>
			<form name="input" action="/logea" method="post">
			%s
			</form>
			</body></html>
			""" % (form.render())
		else:
	
			return """<html><body>
			<form name="input" action="/logea" method="post">
			<p> %s te has logueado con la contrasenia %s </p>
			<a href="../periodico/%s"> Vuelve a portada</a>
			</form>
			</body></html>
			""" % (form.d.usuario, form.d.contrasenia, form.d.usuario)



class periodico:
    def GET(self, name):
        return plantillas.inicio(nombre=name)



def existe_usuario(usuario):
	cursor = col.find({"nombre": usuario})
	return cursor.count()


def comprueba_password(usuario):
	cursor = col.find({"nombre": usuario})
	password = cursor[0]["password"]
	return password 


# Logueo de un usuario de nuestra BD
class acceder:
	def GET(self): 
		form = login2()
		return """<html><body>
		<form name="input" action="/acceder" method="post">
		%s
		</form>
		</body></html>
		""" % (form.render())

	def POST(self):
		form = login2()
		if not form.validates():
			return form.render()
		usuario = form.d.usuario
		password = form.d.contrasenia
		existe = existe_usuario(usuario)
		if existe == 0:
			return """<html><body>
			<form name="input" action="/acceder" method="post">
			<p> El usuario %s no existe </p>
			<a href="../periodico/"> Vuelve a portada</a>
			</form>
			</body></html>
			""" % (form.d.usuario)
		else:
			if password == comprueba_password(usuario):
				sesion.usuario = usuario
				#return web.seeother("http://0.0.0.0:8080/periodico/") 
				return """<html><body>
				<form name="input" action="/acceder" method="post">
				<p> %s te has logueado con la contrasenia %s </p>
				<p> Valor de sesion.usuario: %s</p>
				<a href="../periodico/%s"> Vuelve a portada</a>
				</form>
				</body></html>
				""" % (form.d.usuario, form.d.contrasenia, sesion.usuario, form.d.usuario)

				
			else:
				return """<html><body>
				<form name="input" action="/logea" method="post">
				<p> Contrasenia %s incorrecta </p>
				<a href="http://0.0.0.0:8080/periodico/"> Vuelve a portada</a>
				</form>
				</body></html>
				""" % (form.d.contrasenia)




class registro:
	def GET(self):
		form = login()
		return """<html><body>
		<form name="input" action="/registro" method="post">
		%s
		</form>
		</body></html>
		""" % (form.render())
	def POST(self):
		form = login()
		if not form.validates():
			return form.render()
		else:
			existe = existe_usuario(form.d.nombre)
			usuario = form.d.nombre
			if existe > 1:
				return "Ya existe un usuario con ese nombre"
			else:
				col.insert({"nombre":form.d.nombre,
					"apellidos":form.d.apellidos,
					"DNI":form.d.DNI,
					"password": form.d.password,
					"correo_electronico":form.d.correo_electronico,
					"Dia_de_nacimiento":form['Dia_de_nacimiento'].value,
					"Mes_de_nacimiento":form['Mes_de_nacimiento'].value,
					"Anio_de_nacimiento":form['Anio_de_nacimiento'].value,
					"Direccion":form.d.Direccion,
					"Forma_de_pago":form['Forma_de_pago'].value,
					"numeroVisa":form.d.numeroVisa})

				sesion.usuario = form.d.nombre
				form = login2()
				return """<html><body>
				<form name="input" action="/periodico" method="post">
				<p> %s te has registrado correctamente </p>
				<a href="../periodico/%s"> Vuelve a portada</a>
				</form>
				</body></html>
				""" % (sesion.usuario,  sesion.usuario)

class muestradatos:
	def GET(self, name):
		cursor = col.find_one({"nombre": name})
		nombre = cursor["nombre"]
		password = cursor["password"]
		DNI = cursor["DNI"]
		apellidos = cursor["apellidos"]
		correo = cursor["correo_electronico"]
		Dia_de_nacimiento = cursor["Dia_de_nacimiento"]
		Mes_de_nacimiento = cursor["Mes_de_nacimiento"]
		Anio_de_nacimiento = cursor["Anio_de_nacimiento"]
		numeroVisa = cursor["numeroVisa"]
		Direccion = cursor["Direccion"]
		Forma_de_pago = cursor["Forma_de_pago"]

		return """<html><body>
		<form name="input" action="/periodico/" method="post">
		<p> Tus datos:  </p>
		<p> Nombre y apelledios %s %s DNI: %s </p>
		<p> Direccion: %s, correo: %s y fecha nacimiento: %s-%s-%s </p>
		<p> Pagara %s y su VISA es %s </p>
		<a href="../periodico/%s"> Vuelve a portada</a>
		</form>
		</body></html>
		""" % (nombre,apellidos,DNI,Direccion,correo,Dia_de_nacimiento, Mes_de_nacimiento, Anio_de_nacimiento, Forma_de_pago, numeroVisa, name)



class cambiadatos:

	def GET(self, name):
		cursor = col.find_one({"nombre": name})
		nombre = cursor["nombre"]
		password = cursor["password"]
		DNI = cursor["DNI"]
		apellidos = cursor["apellidos"]
		correo = cursor["correo_electronico"]
		Dia_de_nacimiento = cursor["Dia_de_nacimiento"]
		Mes_de_nacimiento = cursor["Mes_de_nacimiento"]
		Anio_de_nacimiento = cursor["Anio_de_nacimiento"]
		numeroVisa = cursor["numeroVisa"]
		Direccion = cursor["Direccion"]
		Forma_de_pago = cursor["Forma_de_pago"]

		form = login()
		form.nombre.value = nombre
		form.password.value = password 
		form.DNI.value = DNI
		form.apellidos.value = apellidos
		form.correo_electronico.value = correo
		form.numeroVisa.value = numeroVisa
		form.Dia_de_nacimiento.value = Dia_de_nacimiento
		form.Mes_de_nacimiento.value = Mes_de_nacimiento
		form.Anio_de_nacimiento.value = Anio_de_nacimiento
		form.Direccion.value = Direccion
		form.Forma_de_pago.value = Forma_de_pago
		return """<html><body>
		<form name="input" action="/cambiadatos/"  method="post">
		%s
		</form>
		</body></html>
		""" % (form.render())

	def POST(self, name):
		form = login()
		if not form.validates(): 
			return """<html><body>
			<form name="input" action="/cuestionario" method="post">
			%s
			</form>
			</body></html>
			""" % (form.render())
		else:
			col.update({"nombre":form.d.nombre},{"$set":{
			"nombre":form.d.nombre,
			"apellidos":form.d.apellidos,
			"password":form.d.password,
			"correo_electronico":form.d.correo_electronico,
			"numeroVisa":form.d.numeroVisa,
			"Dia_de_nacimiento":form.d.Dia_de_nacimiento,
			"Mes_de_nacimiento":form.d.Mes_de_nacimiento,
			"Anio_de_nacimiento":form.d.Anio_de_nacimiento,
			"Direccion":form.d.Direccion,
			"Forma_de_pago":form.d.Forma_de_pago,
			}})
			#return web.seeother('/periodico/')
			return """<html><body>
			<form name="input" action="/periodico/" method="post">
			<p> Datos cambiados con exito </p>
			<a href="../periodico/%s"> Vuelve a portada</a>
			</form>
			</body></html>
			""" % (form.d.nombre)

# Clase para gestionar el logout de usuario
class salir:
	def GET(self):
		sesion.kill()
		return """<html><body>
		<form name="input" action="/periodico" method="post">
		<p> Logout logrado con exito </p>
		<a href="http://0.0.0.0:8080/periodico/"> Vuelve a portada</a>
		</form>
		</body></html>
		""" 


#Parseador RSS: Sax Parser
'''
from lxml import etree
import sys

class ParseRssNews ():                      #Usando lxml “Sax Parser”
	def __init__ (self):
		print ('----------------------------- Principio del archivo')
			
	#def start (self, tag, attrib):            # Etiquetas de inicio
	#	print ('<%s>' % tag)		
	#	for k in attrib:
	#		print ('%s = "%s"' % (k,attrib[k]))
		
	#def end (self, tag):                      # Etiquetas de fin
	#	print ('</%s>' % tag)
		


	def data (self, data):                    # buscador texto   
		if(data.find(sys.argv[1]) != -1):
			print ('-%s-' % data)
			print ('\n-----------------------------')



	def close (self):
		print ('------------------------------------ Fin del archivo')
			
parser = etree.XMLParser (target=ParseRssNews ())
etree.parse ('http://ep00.epimg.net/rss/ccaa/andalucia.xml', parser)
'''



#Integración de parseador RSS a la esta web
buscador = form.Form(
	form.Textbox('elementorss',required=True,description = "Buscar en el RSS: "),
	form.Button('Buscar', type="submit")
	
)

class buscadorRSS:
	def GET(self): 
		form = buscador()
		return """<html><body>
		<form name="input" action="/buscadorRSS" method="post">
		%s
		</form>
		</body></html>
		""" % (form.render())
	def POST(self):
		form = buscador()
		if not form.validates(): 
			return """<html><body>
			<form name="input" action="/buscadorRSS" method="post">
			%s
			</form>
			</body></html>
			""" % (form.render())
		else:
			return """<html><body>
			<form name="input" action="/buscadorRSS" method="post">
			<p> %s </p>

			<a href="../periodico/"> Vuelve a portada</a>
			</form>
			</body></html>
			""" %(str(form.d.elementorss))




# Parseador RSS: etree Parser
'''
from lxml import etree                              # Usando lxml “etree Parser”

tree = etree.parse('http://ep00.epimg.net/rss/ccaa/andalucia.xml' )

# Root element
rss = tree.getroot()

# Los elementos funcionan como listas
# First child
channel = rss[0]
for e in channel:
	if (e.tag == 'item'):
		e.set('modificado', 'hoy')
		# Los atributos funcionan como diccionarios
		print (e.keys(), e.get('modificado'))
		otro = etree.Element('otro')
		otro.text = 'Texto de otro'
		e.insert(0, otro)
		print (etree.tounicode(rss, pretty_print=True))
'''


# Parsear RSS: Uso de Bibliotecas Especializadas
import feedparser                                    

class rss:
	def GET(self):  

		rss = feedparser.parse("http://ep00.epimg.net/rss/ccaa/andalucia.xml")
		#print len(rss['entries']) 
		return plantillas.rss(mirss=rss)
				



fgrafico = form.Form(
	form.Textbox('elemento1',required=True,description = "Dato para Firefox: "),
	form.Textbox('elemento2',required=True,description = "Dato para Internet Explorer:"),
	form.Textbox('elemento3',required=True,description = "Dato para Chrome: "),
	form.Button('Generar graficos', type="submit")
	
)


# Para generar gráficas
class graficas:
	def GET(self): 
		form = fgrafico()
		return """<html><body>
		<form name="input" action="/graficas" method="post">
		%s
		<a href="../periodico/">  Vuelve a portada</a>
		</form>
		</body></html>
		""" % (form.render())
	def POST(self):
		form = fgrafico()
		if not form.validates(): 
			return """<html><body>
			<form name="input" action="/graficas" method="post">
			%s
			<a href="../periodico/">  Vuelve a portada</a>
			</form>
			</body></html>
			""" % (form.render())
		else:
			li = [form.d.elemento1, form.d.elemento2, form.d.elemento3] 
			return plantillas.graficas(milista=li)


# Para el apartado de mapas
class mapas:
	def GET(self):  
		return plantillas.mapas()


fmap = form.Form(
	form.Textbox('lat',required=True,description = "Latitud: "),
	form.Textbox('long',required=True,description = "Longitud:"),
	form.Button('Buscar con Google Maps', type="submit")
	
)

class buscamaps:
	def GET(self): 
		form = fmap()
		return """<html><body>
		<form name="input" action="/buscamaps" method="post">
		%s
		<a href="../periodico/">  Vuelve a portada</a>
		</form>
		</body></html>
		""" % (form.render())
	def POST(self):
		form = fmap()
		if not form.validates(): 
			return """<html><body>
			<form name="input" action="/buscamaps" method="post">
			%s
			<a href="../periodico/">  Vuelve a portada</a>
			</form>
			</body></html>
			""" % (form.render())
		else:
			latitud = form.d.lat
			longitud = form.d.long
			return plantillas.buscamaps(milat=latitud, milong=longitud)


# Uso de Tweepy

import tweepy

# Consumer keys and access tokens, used for OAuth
consumer_key = 'LR858vtfM5vxFgyyq4z6MyRug'
consumer_secret = '4IWw9duemh3NTgVOjIUPxBYGDsrd5QT5H77wSXO30iOXBUyCat'
access_token = '275200279-hfwcoJqYpNIEpcQpacs7TqJMN1GaN9t12FxVotU1'
access_token_secret = 'iM6GeLwvGpQRqDJLjkELuw1rVDqH9TKogx490nEJbK1Po'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
#api = tweepy.API(auth)

# https://dev.twitter.com/docs/api/1.1/get/search/tweets
#tweets = api.search(q='Granada', count=1)

# Mostramos los campos del objeto Tweet
#print dir(tweets[0])

# Mostramos los campos del objeto author del Tweet
#print dir(tweets[0].author)

# Mostramos el nombre del Autor del Tweet.
#print tweets[0].author.name

# Mostramos el texto del tweet
#print tweets[0].text

# Mostramos el id del tweet
#print tweets[0].id




ftweet = form.Form(
	form.Textbox('elementotweet',required=True,description = "Busca una palabra en twitter: "),
	form.Button('Buscar', type="submit")
	
)
class buscatweet:
	def GET(self): 
		form = ftweet()
		return """<html><body>
		<form name="input" action="/buscatweet" method="post">
		%s
		<a href="../periodico/">  Vuelve a portada</a>
		</form>
		</body></html>
		""" % (form.render())
	def POST(self):
		form = ftweet()
		if not form.validates(): 
			return """<html><body>
			<form name="input" action="/buscatweet" method="post">
			%s
			<a href="../periodico/">  Vuelve a portada</a>
			</form>
			</body></html>
			""" % (form.render())
		else:
			# Creation of the actual interface, using authentication
			api = tweepy.API(auth)

			# https://dev.twitter.com/docs/api/1.1/get/search/tweets
			tweets = api.search(q=form.d.elementotweet, count=1)

			return plantillas.buscatweet(mitweet=tweets, mipalabra=form.d.elementotweet)



class tweetposicion:
	def GET(self):  
		return plantillas.tweetposicion()



if __name__=="__main__":
	app.run()


