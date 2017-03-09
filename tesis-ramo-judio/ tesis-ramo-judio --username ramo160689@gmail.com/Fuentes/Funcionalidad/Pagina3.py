import os

def listarAlias(listaAlias):
		resultado = []
		for item in listaAlias:
			resultado.append(item[0])
		return resultado
		
def aliasDuplicado(alias, listaAlias):
	resultado = True
	indice = 0
	while indice < len(listaAlias) and resultado:
		if listaAlias[indice][0] == alias:
			resultado = False
		indice += 1
			
	return resultado
	
	
def obtenerAlias(listaAlias, numero):
	resultado = 0
	indice = 0
	while indice < len(listaAlias) and resultado == 0:
		if listaAlias[indice][1] == numero:
			resultado = listaAlias[indice][0]
		indice += 1
	return resultado
	
def eliminarAlias(listaAlias, numero):
	resultado = 0
	indice = 0
	while indice < len(listaAlias) and resultado == 0:
		if listaAlias[indice][1] == numero:
			resultado = listaAlias.pop(indice)
		indice += 1
	
	
def obtenerNumero(listaAlias, alias):
	resultado = 0
	indice = 0
	while indice < len(listaAlias) and resultado == 0:
		if listaAlias[indice][0] == alias:
			resultado = listaAlias[indice][1]
		indice += 1
	return resultado

def dicCodigosArea(codigo):
	archivo = open(os.getcwd() + "//Fuentes//Funcionalidad//codigosArea.txt", "r").read().split("\n")
	resultado = []
	indice = 0
	flag = True
	while flag and indice < len(archivo):
		lista = archivo[indice].split("-")
		if lista:
			if lista[0] == codigo:
				numero = lista.pop(0)
				resultado = lista
				flag = False
		indice += 1
	return resultado