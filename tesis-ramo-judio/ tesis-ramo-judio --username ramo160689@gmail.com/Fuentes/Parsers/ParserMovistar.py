# *-* coding: utf-8 *-*
import os
import re
from Diccionario.Diccionario import Diccionario
from Sabana import *


class ParserMovistar:
	def __init__(self, sabana = None, nomSabana = ''):
		self.nombreSabana = nomSabana
		if sabana != None:
			self.listaTuplas = sabana.listaTuplas
			self.nombreSabana = sabana.nombreArchivo
		
	
	def esSabanaMovistar(self):
		sabana = open(self.nombreSabana, "r")
		flag = True
		contador = 0
		if str(self.nombreSabana).endswith(".txt"):
			while flag:
				linea = sabana.readline()
				if linea.find("-----------") != -1:
					contador += 1
				
				if (linea.find("Nro. Pagador") != -1 and
					linea.find("Nro. Destino") != -1):
					contador += 1
					flag = False
				
				if (linea.find("Esn/Imei") != -1 and
					linea.find("Dir.") != -1):
					contador += 1
					flag = False
			
			sabana.readline()
			if linea.find("-----------") != -1:
				contador += 1
			
			if contador > 2:
				sabana.close()
				return True
		return False
	
	def parserLineaEncabezados(self, linea):
		lista = linea.split("  ")
		resultado = []
		for item in lista:
			if len(item) == 1 and item != "\n":
				print "Algun encabezado quedo mal parseado"
				print lista
				break
			else:
				if item.find("Dir. Nro. Destino") != -1:
					resultado.append("Dir.")
					resultado.append("Nro. Destino")
				else:
					if len(item) > 0 and item != "\n":
						resultado.append(unicode(item.strip(), "latin"))
		if len(lista) == len(resultado) - 1:
			print "Se separo Dir."
		return resultado
		
	def obtenerEncabezados(self):
		flag = True
		sabana = open(str(self.nombreSabana), "r")
		while flag:
			linea = unicode(sabana.readline(), "latin")
			if linea.find("-----------") != -1:
				flag = False
		linea = sabana.readline()
		# En linea tengo la fila de encabezados
		listaEncabezados = self.parserLineaEncabezados(linea)
		sabana.close()
		return listaEncabezados

	def formatearEncabezados(self):
		encabezados = Diccionario().listaConceptos
		resultado = ";"
		resultado = resultado.join(encabezados)
		resultado = resultado + ";nombreArchivo\n"
		
		# i = 1
		# for item in encabezados:
			# if i == len(encabezados):
				# resultado = resultado + "nombreArchivo" + "\n"
			# else:
				# resultado = resultado + item + ";"
			# i += 1
		return resultado
		
	
		
	
	def formatearLinea(self, linea, encabezados):
		resultado = ""	
		numeroOrigen = ""
		numeroDestino = ""
		tipoComunicacion = ""
		exp = '(\s*)(\d{2})/(\d{2})/(\d{4})(\s*)(\d{2}):(\d{2}):(\d{2})(\s*)([0-9]+)(\s*)([S|T|E]+)(\s*)([*0-9]+)(\s*)(\d{2}):(\d{2}):(\d{2})(\s*)([0-9]+)(\s*)'
		exp1 = '(\s*)(\d{2})/(\d{2})/(\d{4})(\s*)(\d{2}):(\d{2}):(\d{2})(\s*)([0-9]+)(\s*)([S|T|E]+)(\s*)([*0-9]+)(\s*)(\d{2}):(\d{2}):(\d{2})(\s*)'
		
		flag = False
		if re.match(exp, linea):
			grupo = re.match(exp, linea)
			flag = True
			lista = grupo.group().split()
		elif re.match(exp1, linea):
			grupo = re.match(exp1, linea)
			lista = grupo.group().split()
		else: 
			return -1
		
		if lista[3] == "S":
			tipoComunicacion = "Llamada"
			numeroOrigen = lista[2]
			numeroDestino = lista[4]
		elif  lista[3] == "E":	
			tipoComunicacion = "Llamada"
			numeroOrigen = lista[4]
			numeroDestino = lista[2]
		else:
			tipoComunicacion = "Mensaje"
			numeroOrigen = lista[2]
			numeroDestino = lista[4]
			
		#Acomodamos segun el tipo de llamada
		for item in encabezados:
			
			#Sabemos en que ubicacion se encuentra cada dato
			if item == "numeroOrigen":
				resultado = resultado + numeroOrigen + ";"
			elif item == "numeroDestino":
				resultado = resultado + numeroDestino + ";"
			elif item == "fecha":
				resultado = resultado + self.parserFecha(lista[0]) + ";"
			elif item == "hora":
				resultado = resultado + lista[1] + ";"
			elif item == "tipoComunicacion":
				resultado = resultado + tipoComunicacion + ";"
			elif item == "duracion":
				resultado = resultado + lista[5] + ";"
			elif item == "numeroImei":
				if flag:
					resultado = resultado + lista[6] + ";"
				else:
					resultado = resultado + "" + ";"
			else:
				#no es un concepto que este en las sabanas movistar
				resultado = resultado + "" + ";"
		
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
			linea = entrada.readline()
			if linea.find("-------") != -1:
				# Paso la segunda "-------"
				linea = entrada.readline()
				linea = entrada.readline()
				if linea.find("-------") != -1:
					flag = False
				else:
					print "Error CrearArchivoTemporal Movistar"
		# En linea tengo los encabezados originales, de ahi
		# para abajo son todos datos crudos.
		entrada = unicode(entrada.read(), "latin").split("\n")
		#Preparo los encabezados para comparar
		encabezados = encabezados.split(";")
		encabezados.pop()
		encabezados.pop()
		
		for linea in entrada:
			if linea.find("------------------") == -1:
				renglon = self.formatearLinea(linea, encabezados)
				if renglon != -1:
					salida.write(renglon)
				else:
					salida.write("-1\n")
			else:
				break
		salida.close()
	
	# Recibe Fecha y Hora y devuelve por separado
	# cada uno de ellos
	# 21/09/2009 18:33:11
	# Retorna una lista [fecha, hora] en formato listo para sql
	def parserFecha(self, fecha):
		#Al usar ER no puede ser vacio
		fecha = fecha.split("/")
		fecha.reverse()
		aux = ""
		aux = aux.join(fecha)
		return aux
		
	
	# Eliminar el archivo temporal creado	
	def eliminarArchivoTemporal(self):
		os.remove(str(self.nombreSabana) + "_")
	
	def obtenerLineas(self):
		resultado = []
		entrada = open(self.nombreSabana + "_", "r")
		entrada.readline()
		entrada = unicode(entrada.read(), "latin").split("\n")
		# entrada = entrada.read().split("\n")
		for item in entrada:
			if len(item)>0:
				resultado.append(item.split(";"))
		return resultado
		