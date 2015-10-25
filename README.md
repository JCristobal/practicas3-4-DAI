practicas3-4-DAI
================

Prácticas 3 y 4 de la asignatura Desarrollo de Aplicaciones Web (DAI) de la [ETSIIT, Granada](http://etsiit.ugr.es/).

***

Contendrá los contenidos de las prácticas 3:

* Formularios “Avanzados”
* Plantillas (con mako)
* Manejo de Sesiones
* Persistencia Sencilla: dbm
* Persistencia NO-SQL: MongoDB

y de la práctica 4:

* Analizar RSS de varias formas, e integrarlo en esta web
* Uso e integración del servicio de [Highcharts](http://www.highcharts.com/)
* Uso e integración de Google Maps
* Integración sencilla de Twitter
* Python Twitter: [Tweepy](http://pythonhosted.org/tweepy/html/)
* "Mashup" (aplicación web híbrida, en mi caso Tweeter con geolocalización)
* Uso de jQuery y AJAX

* Framework web para Python [web.py](http://webpy.org/). 


***

Para usar la aplicación, si no tienes intalado web.py, pymongo, mako o tweepy ejecutar:

`sudo apt-get install python-setuptools`

`sudo easy_install web.py`

`sudo easy_install pymongo`

`sydo apt-get install python-pip`

`sudo pip install Mako`

`sudo pip install tweepy`

`sudo pip install feedparser`


Para mongo: instalalo con `sudo apt-get install mongodb`, ejecuta `sudo rm  /var/lib/mongodb/mongod.lock` y `sudo service mongodb restart`


Para usar la aplicación  hay que ejecutar en consola `python practica3-4.py` y se podrá ver dentro del navegador en http://0.0.0.0:8080/periodico/

***

Autor:
J. Cristóbal López Zafra, @JCristobal en GitHub y con correo de contacto tobas92@gmail.com

Licencia: GPLv2
