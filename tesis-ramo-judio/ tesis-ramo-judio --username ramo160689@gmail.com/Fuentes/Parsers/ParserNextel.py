#!/usr/bin/env python
# *-* coding: utf-8 *-*
import os
from Diccionario.Diccionario import Diccionario
from CjtoSabana import *
from Sabana import *



#formato de listaConceptos [(concepto, sinonimo), ....]

class ParserNextel:
	def __init__(self, sabana = None, nomSabana = ''):
		self.listaEncabezados = []
		self.nombreSabana = nomSabana
		if sabana != None:
			self.sabana = sabana
			self.listaEncabezados = sabana.listaEncabezados
			self.listaTuplas = sabana.listaTuplas
			self.nombreSabana = sabana.nombreArchivo
		
		self.separador = ";"
		
		
	def inicioInformacion(self):
		if str(self.nombreSabana).find(".csv") != -1:
			archivo = open(self.nombreSabana, 'r')
			flag = True
			indice = 0
			contador = 0
			dic = Diccionario()
			while flag:
				linea1 = archivo.readline().split(self.separador)
				linea2 = archivo.readline().split(self.separador)
				linea3 = archivo.readline().split(self.separador)
				if (len(linea1) == len(linea2) and
					len(linea2) == len(linea3) and len(linea1) > 10):
					flag = False
					if dic.listadoPosibilidades(linea1[0]):
						contador += 1
						if dic.listadoPosibilidades(linea1[1]):
							contador += 1
							if dic.listadoPosibilidades(linea1[2]):
								contador += 1
								if dic.listadoPosibilidades(linea1[3]):
									contador += 1
				indice += 1
				# Verificamos que sea lo buscado
				
			if contador > 2:
				# como leo de a 3 lineas y solo sirve la primera
				self.inicInformacion = (indice * 3) - 2
				archivo.close()
				return (indice * 3) - 2
			archivo.close()
		# Error, tal vez no es una sabana nextel		
		return -1
		
	def esSabanaNextel(self):
		if self.inicioInformacion() != -1:
			return True
		else:
			return False
		
	def obtenerEncabezados(self):
		flag = False
		archivo = open(self.nombreSabana, "r")
		for i in range(self.inicInformacion):
			linea = archivo.readline()
			# Saco el \n del final
			linea = linea.split("\n")[0].split(self.separador)
		#Eliminamos aquellos que son descartables
		dic = Diccionario()		
		for item in linea:
			if not dic.esDescartable(item):
				self.listaEncabezados.append(item)
		linea = self.listaEncabezados
		archivo.close()
		return linea
	
	def parserLinea(self, linea):
		salida = ""
		aux = linea.split(self.separador)
		
		for item in aux:
			if item.find("\n") != -1:
				salida = salida + item.replace(" .", "")
			else:
				salida = salida + item.replace(" .", "") + ";"
		return salida
	
	def formatearEncabezados(self):
		encabezados = Diccionario().listaConceptos
		#Saco descartables
		encabezados.pop()
		
		resultado = ";"		
		resultado = resultado.join(encabezados)
		resultado = resultado + ";nombreArchivo" + "\n"
		
		return resultado
		
	def crearSinConcepUbic(self, linea):
		listaAux = []
		for item in self.listaTuplas:
			indice = 0
			for sin in linea:
				if item[0] == sin:
					listaAux.append((item[0], item[1], indice))
					break
				indice += 1
		self.sinConcUbi = listaAux
		
	def hhmmss(self, segundostotales):
		resultado = []
		if segundostotales != '':
			segundostotales = int(segundostotales)
			hh = segundostotales // 3600
			mm = (segundostotales % 3600)//60
			ss = (segundostotales %3600) %60
			resultado = [str(hh).zfill(2),str(mm).zfill(2),str(ss).zfill(2)]
		else:
			resultado = ['00', '00','00']
		return resultado
	
	def formatearLinea(self, linea, encabezados):
		resultado = ""	
		fechaHora = ""
		duracion = ""
	
		#Preparamos las fechas
		for item in self.sinConcUbi:
			if item[1][0] in {"fecha","hora"}:
				fechaHora = self.parserFecha(linea[item[2]])
			elif item[1][0] == "duracion":
				aux = ":"
				segundos = linea[item[2]].replace(" .", "")
				segundos = self.hhmmss(segundos)
				duracion = aux.join(segundos)
			else:
				pass		
		for item in encabezados:
			indice = 0
			flag = True
			if item == "fecha":
				resultado = resultado + fechaHora[0] +";"
				flag = False
			elif item == "hora":
				resultado = resultado + fechaHora[1] +";"
				flag = False
			elif item == "duracion":
				resultado = resultado + duracion + ";"
				flag = False
			else:
				while flag and indice < len(self.sinConcUbi):
					if item == self.sinConcUbi[indice][1][0]:
						if linea[self.sinConcUbi[indice][2]] != "":
							resultado = resultado + linea[self.sinConcUbi[indice][2]] + ";"
							flag = False
					indice += 1
				if flag: # No lo encontro, entonces lleva vacio
					resultado = resultado + "" + ";"
		resultado = resultado.replace(" .", "")
		resultado = resultado + self.nombreSabana + "\n"
		return resultado
	
	
	def crearArchivoTemporal(self):
		nombreSalida = self.nombreSabana + "_"
		salida = open(nombreSalida, "w")
		encabezados = self.formatearEncabezados()
		salida.write(encabezados)
		entrada = open(self.nombreSabana, "r")
		flag = True
		while flag:
			linea = entrada.readline().split("\n")[0].split(";")
			if (len(linea) > len(self.listaEncabezados) - 3 and
				len(linea) < len(self.listaEncabezados) + 3):
				for item in self.listaEncabezados:
					if item in linea:
						flag = False
		self.crearSinConcepUbic(linea)
		# En linea tengo los encabezados originales, de ahi
		# para abajo son todos datos crudos.
		# entrada = unicode(entrada.read(), "latin").split("\n")
		entrada = entrada.read().split("\n")
		#Preparo los encabezados para comparar
		encabezados = encabezados.split(";")
		encabezados.pop()
		for linea in entrada:
			if len(linea) >= len(self.sinConcUbi):
				salida.write(self.formatearLinea(linea.split(";"), encabezados))

		salida.close()
		

	# Recibe Fecha y Hora y devuelve por separado
	# cada uno de ellos
	# 21/09/2009 18:33:11
	# Retorna una lista [fecha, hora] en formato listo para sql
	def parserFecha(self, fechaHora):
		if fechaHora != "":
			aux = fechaHora.replace(" .","")
			fecha = aux.split(" ")[0]
			hora = aux.split(" ")[1]
			fecha = fecha.split("/")
			fecha.reverse()
			aux = ""
			aux = aux.join(fecha)
			return [aux, hora]
		else:
			#Fecha y hora invalida
			return ["18000101", "25:00:00"]
		
			
	# Eliminar el archivo temporal creado	
	def eliminarArchivoTemporal(self):
		os.remove(str(self.nombreSabana) + "_")
		pass
	
	def obtenerLineas(self):
		resultado = []
		entrada = open(self.nombreSabana + "_", "r")
		entrada.readline()
		entrada = unicode(entrada.read(), "utf-8").split("\n")
		# entrada = entrada.read().split("\n")
		for item in entrada:
			if len(item)>0:
				resultado.append(item.split(self.separador))
		return resultado