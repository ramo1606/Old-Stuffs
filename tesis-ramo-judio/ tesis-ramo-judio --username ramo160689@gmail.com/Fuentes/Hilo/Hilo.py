#!/usr/bin/env python
# *-* coding: utf-8 *-*

from PyQt4 import QtCore, QtGui
from threading import Thread, Condition
from Fuentes.Parsers.Diccionario.Diccionario import Diccionario


class Hilo(Thread):
	def __init__(self, consumidor, condicion, sinonimoLinea, conceptosLista):
		Thread.__init__(self)
		self.dic = Diccionario()
		self.condicion = condicion
		self.consumidor = consumidor
		self.sinonimoLinea = sinonimoLinea
		self.conceptosLista = conceptosLista
		self.fin = False
		
		
	
	def run(self):
		self.condicion.acquire()
		while not self.fin:
			if self.consumidor:
				tupla = self.consumidor.pop()
				sinonimo = tupla[0]
				self.conceptosLista.clear()
				lista = self.dic.traduccionConceptos(tupla[1])
				lista.sort()
				self.conceptosLista.addItems(lista)
				self.sinonimoLinea.setText(sinonimo)
			else:
				print "se trato de hacer un pop vacio"
			self.condicion.wait()
		self.condicion.release()