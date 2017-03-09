#!/usr/bin/env python
# *-* coding: utf-8 *-*

import Parser
from Diccionario.Diccionario import Diccionario

class Sabana():
	def __init__(self, nombreArchivo, nombreEmpresa, checked):
		self.nombreArchivo = nombreArchivo
		self.nombreEmpresa = nombreEmpresa
		self.checked = checked
		# control = 1 --> Error_Empresa
		# control = 2 --> Error_Concepto
		self.control = 0
		self.listaTuplas = []
		self.listaEncabezados = self.listarEncabezados()
		# self.cantidad = len(self.listaEncabezados)
		# self.listaEncabezadosVacia = False
		# self.listaTuplas = []
		
	def listarEncabezados(self):
		parser = Parser.Parser(self.nombreArchivo, self.nombreEmpresa)
		lista = parser.nombreColumnas()
		
		if lista == "ERROR_EMPRESA":
			self.control = 1
			lista = []
		return lista
		
	def insertarTupla(self, tupla):
		self.listaTuplas.append(tupla)
	
	def sacarTupla(self):
		if self.listaTuplas:
			return self.listaTuplas.pop()
		
	def aliasArchivo(self):
		alias = self.nombreArchivo
		return alias.split("/")[len(alias.split("/")) - 1]
	
	# Devuelve una lista de conceptos disponibles para asignar a una columna
	# de la sabana que matcheo con varios sinonimos a la vez.
	def conceptosDisponibles(self, coincidencias):
		asignados = []
		libres = []
		dic = Diccionario()
		libres = dic.listaConceptos
		for item in self.listaTuplas:
			if len(item[1]) == 1:
				asignados = asignados + item[1]
		libres = set(libres)
		asignados = set(asignados)
		libres = libres - asignados
		print "coincidencias"
		print coincidencias
		if not coincidencias:
			#-------------
			cantidad = len(asignados)
			asignados = set(asignados)
			if cantidad != len(asignados):
				print "Error en la asignacion de conceptos a las columnas"
				print "Arrancar el rastreo por conceptosDisponibles en Sabana.py"
			#-------------
			libres = list(libres - asignados)
		else:
			coincidencias = set(coincidencias)
			libres = list(coincidencias & libres)
					
		return libres
	
	# Al valor de la columna del archivo, le asigna el concepto pasado por parametro.
	def asignarConcepto(self, sinonimo):
		flag = True
		indice = 0
		while flag and indice < len(self.listaTuplas):
			if self.listaTuplas[indice][0] == sinonimo:
				self.listaTuplas[indice][1] = [sinonimo]
				flag = False
			indice = indice + 1
			#-------------
			if flag:
				print "Error en la busqueda del sinonimo"
				print "Funcion asignarConcepto, Sabana.py"
			#-------------
	
	# Devuelve True si todos los sinonimos tienen solo 1 concepto asignado
	def todoAsignado(self):
		flag = True
		for item in self.listaTuplas:
			if len(item[1]) != 1:
				flag = False
		return flag
	