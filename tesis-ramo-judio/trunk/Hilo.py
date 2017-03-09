from PyQt4 import QtCore, QtGui
from threading import Thread, Condition
from Fuentes.Diccionario.Diccionario import Diccionario


class Hilo(Thread):
	def __init__(self, consumidor, conceptosLista, condicion, archivoLabel, nombreArchivo, sinonimoLinea):
		Thread.__init__(self)
	
	
		self.nombreArchivo = nombreArchivo
		self.archivoLabel = archivoLabel
		self.conceptosLista = conceptosLista
		self.consumo = consumidor
		self.condicion = condicion
		self.sinonimoLinea = sinonimoLinea
		self.fin = False
		self.dic = Diccionario()
						
						
						
		if len(self.consumo) > 0:
			self.archivoLabel.setText(self.nombreArchivo)
			sinonimo = self.consumo.pop(0)
			self.conceptosLista.clear()
			self.conceptosLista.addItems(self.dic.listadoPosibilidades(sinonimo))
			self.sinonimoLinea.setText(sinonimo)
		
	
	def run(self):
		self.condicion.acquire()
		while not self.fin:
			self.condicion.wait()
			if len(self.consumo) > 0:
				self.archivoLabel.setText(self.nombreArchivo)
				if self.consumo:
					sinonimo = self.consumo.pop(0)
					self.conceptosLista.clear()
					self.conceptosLista.addItems(self.dic.listadoPosibilidades(sinonimo))
					self.sinonimoLinea.setText(sinonimo)
				else:
					print "se trato de hacer un pop vacio"
				
		self.condicion.release()
		
		

		
