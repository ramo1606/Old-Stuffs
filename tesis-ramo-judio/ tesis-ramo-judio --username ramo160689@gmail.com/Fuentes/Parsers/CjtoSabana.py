#!/usr/bin/env python
# *-* coding: utf-8 *-*

class ConjuntoSabanas():
	def __init__(self):
		self.listaSabanas = []
		self.cantidadSabanas = 0

	
	def insertarSabana(self, sabana):
		self.listaSabanas.append(sabana)
		self.cantidadSabanas += 1
		
		
	def sacarSabana(self):
		if self.listaSabanas:
			self.cantidadSabanas -= 1
			return self.listaSabanas.pop()
			
	def sacarSabanaN(self, indice):
		if indice < self.cantidadSabanas:
			self.cantidadSabanas -= 1
			return self.listaSabanas.pop(indice)
		else:
			return -1
	
	def todoVerificado(self):
		flag = True
		indice = 0
		while flag and indice < self.cantidadSabanas:
			if not self.listaSabanas[indice].checked:
				flag = False
			indice += 1
		return flag
	
	def buscarSabana(self, nombreArchivo):
		flag = False
		indice = 0
		while not flag and indice < self.cantidadSabanas:
				if (nombreArchivo == self.listaSabanas[indice].nombreArchivo):
						flag = True
						return indice
				indice += 1
		return -1
	