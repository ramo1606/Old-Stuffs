#!/usr/bin/env python
# *-* coding: utf-8 *-*

from PyQt4 import QtSql
nombreTabla = "ejemplo"

def obtenerAutocompletar(concepto):
	query = QtSql.QSqlQuery()
	consulta = "SELECT DISTINCT " + concepto + " FROM " + nombreTabla
	query.exec_(consulta)
	print query
	
def traducirDuracion(texto):	
	if texto == "0 seg.":
		return "00:00:00"
		
	elif texto == "30 seg.":
		return "00:00:30"
	elif texto == "1 min.":
		return "00:01:00"
	elif texto == "2 min.":
		return "00:02:00"
	elif texto == "3 min.":
		return "00:03:00"
	elif texto == "4 min.":
		return "00:04:00"
	elif texto == "5 min.":
		return "00:05:00"
	elif texto == unicode("más de 5 min.", "latin"):
		return "23:59:59"
	else:
		return "Error en la traduccion de la duracion"
	
