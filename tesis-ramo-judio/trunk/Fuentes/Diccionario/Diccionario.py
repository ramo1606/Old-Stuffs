import os

class Diccionario:
	def __init__(self):		
		self.lista = []
		self.listaConceptos = []
		archivoConceptos = open(os.getcwd() + "\\Fuentes\\Diccionario\\conceptos.txt", "r")
		for linea in archivoConceptos:
			self.lista.append(linea.split("\n")[0].split(";"))
			self.listaConceptos.append(linea.split(";")[0])
		archivoConceptos.close()
		
	def sinonimoDe(self, sinonimo):
		flag = True
		i = 0
		resultado = ""
		while flag and i<len(self.lista):
			if sinonimo in self.lista[i]:
				flag = False
				#La primer palabra de cada linea es el concepto
				resultado = self.lista[i][0]
			else:
				i = i+1
		#El sinonimo no tiene nada asociado
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
		archivoConceptos = open("conceptos.txt", "r")
		lineas = archivoConceptos.readlines()
		lineas[posicion] = lineas[posicion].replace("\n", ";" + sinonimo + "\n")
		archivoConceptos.close()
		archivoConceptos = open("conceptos.txt", "w")
		archivoConceptos.writelines(lineas)
		archivoConceptos.close()
		
	def listadoPosibilidades(self, sinonimo):
		resultado = []
		posibilidad = self.sinonimoDe(sinonimo)
		if posibilidad != "":
			resultado.append(posibilidad)
		for item in self.lista:
			for sin in item:
				if sin.find(sinonimo) != -1:
					resultado.append(self.sinonimoDe(sin))
		# Elimino duplicados			
		resultado = set(resultado)
		resultado = list(resultado)
		return resultado
