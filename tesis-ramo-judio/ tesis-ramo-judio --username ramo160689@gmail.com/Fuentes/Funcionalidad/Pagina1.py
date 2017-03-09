#!/usr/bin/env python
# *-* coding: utf-8 *-*

from Fuentes.Parsers.Diccionario.Diccionario import Diccionario

def verificarColumnas(cjtoSabanas):
	dic = Diccionario()
	conceptosUsados = []
	listaAsignados = []
	for item in cjtoSabanas.listaSabanas:
		if not item.checked:
			for col in item.listaEncabezados:
				posibilidades = dic.listadoPosibilidades(col)
				if len(posibilidades) == 1:
					listaAsignados.append(posibilidades[0])
				tupla = (col, posibilidades)
				item.insertarTupla(tupla)
			aux = []
			for tupla in item.listaTuplas:
				if len(tupla[1]) > 1:
					for elem in tupla[1]:
						if elem in listaAsignados:
							indice = tupla[1].index(elem)
							tupla[1].pop(indice)		
				if (len(tupla[1]) > 1) | (len(tupla[1]) == 0):
					item.control = 2
			if item.control == 0:
				item.checked = True
		else:
			asignados = []
			for elem in item.listaTuplas:
				if len(elem[1]) == 1:
					asignados.append(elem[1][0])
			
			cantidad = len(asignados)
			asignados = set(asignados)
			asignados = list(asignados)
			if len(asignados) != cantidad:
				print "Error, conceptos repetidos..."
				print "verificarColumnas en pagina1.py"
				