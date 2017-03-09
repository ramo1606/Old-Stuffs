#!/usr/bin/env python
# *-* coding: utf-8 *-*

import os

class Diccionario:
	def __init__(self):
		# Atributos
		self.lista = []							#Lista de listas [concepto, sin1, sin2, sin3, ...]
		self.listaConceptos = []
		self.listaTraducciones = []
		
		#Codigo Inicial
		# Trabajo con el archivo de conceptos
		# archivoConceptos = open(os.getcwd() + "\\Diccionario\\conceptos.txt", "r")
		archivoConceptos = open(os.getcwd() + "\\Fuentes\\Parsers\\Diccionario\\conceptos.txt", "r")
		# archivoConceptos = open("conceptos.txt", "r")
		for linea in archivoConceptos:
			listaAux = unicode(linea, 'latin').split("\n")[0].split(";")
			self.lista.append(listaAux)
			self.listaConceptos.append(linea.split(";")[0])
		archivoConceptos.close()
		
		# Trabajo con el archivo de traducciones
		# archivoTraducciones = open(os.getcwd() + "\\Diccionario\\traducciones.txt", "r")
		archivoTraducciones = open(os.getcwd() + "\\Fuentes\\Parsers\\Diccionario\\traducciones.txt", "r")
		# archivoTraducciones = open("traducciones.txt", "r")
		for linea in archivoTraducciones:
			tupla = (linea.split(";")[0], linea.split(";")[1].split("\n")[0])
			self.listaTraducciones.append(tupla)
		archivoTraducciones.close()
			
		
	#Devuelve el concepto relacionado con el nombre de columna
	def sinonimoDe(self, sinonimo):
		flag = True
		i = 0
		resultado = []
		for item in self.lista:
			if sinonimo in item:
				resultado.append(item[0])
		return resultado
	
	def posicionConcepto(self, concepto):
		flag = True
		i = 0
		resultado = -1
		while flag and i<len(self.lista):
			if concepto in self.lista[i]:
				resultado = i
				flag = False
			else:
				i = i+1
		return resultado
		
	def agregarSinonimo(self, concepto, sinonimo):
		posicion = self.posicionConcepto(concepto)
		archivoConceptos = open(os.getcwd() + "\\Fuentes\\Parsers\\Diccionario\\conceptos.txt", "r")
		lineas = archivoConceptos.readlines()
		lineas[posicion] = lineas[posicion].replace("\n", ";" + sinonimo.encode('latin') + "\n")
		archivoConceptos.close()
		archivoConceptos = open(os.getcwd() + "\\Fuentes\\Parsers\\Diccionario\\conceptos.txt", "w")
		archivoConceptos.writelines(lineas)
		archivoConceptos.close()
		
		
	#Devuelve una lista con posibles conceptos que matchean con el sinonimo
	def listadoPosibilidades(self, sinonimo):
		resultado = []
		resultado = self.sinonimoDe(sinonimo)
		if len(resultado) != 0:
			return resultado
		else:
			for item in self.lista:
				for sin in item:
					if sin.find(sinonimo) != -1:
						resultado.append(item[0])

						# Elimino duplicados
		resultado = set(resultado)
		resultado = list(resultado)
		return resultado
		
	def traduccionConceptos(self, lista):
		resultado = []
		if lista[0] in self.listaConceptos:
			aux1 = 0
			aux2 = 1
		else:
			aux1 = 1
			aux2 = 0	
			
		for item in lista:
			flag = False
			indice = 0
			while not flag and indice < len(self.listaTraducciones):
				if self.listaTraducciones[indice][aux1] == item:
					resultado.append(self.listaTraducciones[indice][aux2])
					flag = True
				indice += 1
		return resultado
		
	def esDescartable(self, sinonimo):
		descartables = self.lista[len(self.lista)-1]
		if sinonimo in descartables:
			return True
		return False