#!/usr/bin/env python
# *-* coding: utf-8 *-*





from PyQt4 import QtSql, QtGui
import sys, os
from Diccionario.Diccionario import Diccionario


class dbManager:
	def __init__ (self, filename = ""):
		self.nombreTabla = "prueba"
		self.listaConsultas = []
		self.diccionario = Diccionario()
		if filename != "":
			self.db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
			self.db.setDatabaseName(filename)			
			self.db.setHostName("localhost")
			self.db.setUserName("root")
			self.db.setPassword("root")
			if not self.db.open():
				QtGui.QMessageBox.warning(None, "Error!",
				"Error en la Base de Datos: " + self.db.lastError().text())
				sys.exit(1)
			
			consulta = "CREATE TABLE `sabanas`.`prueba` ("
			for item in range(len(self.diccionario.listaConceptos) - 1):
				if self.diccionario.listaConceptos[item] == "fecha":
					consulta = consulta + self.diccionario.listaConceptos[item] + " DATE, "
				elif self.diccionario.listaConceptos[item] == "hora":
					consulta = consulta + self.diccionario.listaConceptos[item] + " TIME, "
				else:
					consulta = consulta + self.diccionario.listaConceptos[item] + " TEXT, "
			consulta = consulta + "nombreArchivo TEXT)"
			query = query = QtSql.QSqlQuery()
			query.exec_(consulta)
			
			
			
	def insertarRegistroDB(self, listaDatos):
		indice = 0
		consulta = "INSERT INTO `sabanas`.`prueba` ("
		for item in range(len(self.diccionario.listaConceptos) - 1):
			consulta = consulta + self.diccionario.listaConceptos[item] + ", "
		consulta = consulta + "nombreArchivo) VALUES("
	
		if len(listaDatos) == len(self.diccionario.listaConceptos):
			for item in listaDatos:
				if indice == len(listaDatos) - 1:
					consulta = consulta + "'" + item + "'" + ")"
				else:
					consulta = consulta + "'" + item + "'" + ","
				indice += 1
		else:
			print "Error enla cantidad de datos a llenar en la DB"
		query = QtSql.QSqlQuery()
		query.exec_(consulta)
		return query.numRowsAffected()
		
	def obtenerAutocompletar(self, concepto, opcion = 0):	
		query = QtSql.QSqlQuery()
		consulta = "SELECT DISTINCT " + concepto + " FROM " + self.nombreTabla
		query.exec_(consulta)

		lista = []
		while query.next():
			# resultado = unicode(query.value(0).toString()).encode('utf-8')
			resultado = query.value(0).toString()
			if resultado != "":
				lista.append(resultado)
				# print "el resultado: " + resultado
		
		if opcion == 0:
			return QtGui.QCompleter(lista)
		else:
			return lista

			
	def eliminarDB(self):
		query = QtSql.QSqlQuery()
		query.exec_("DROP TABLE `sabanas`.`prueba`")
		pass
	
	def armarLikes(self, item, esUltimo):
		aux = ""
		cod = item[3] + "%"
		if not esUltimo:
			if item[1] == "distinto":
				if item[2] == 0:
					aux = ("(numeroOrigen NOT LIKE '0%s' AND numeroOrigen NOT LIKE '%s' AND numeroOrigen NOT LIKE '00549%s' AND numeroOrigen NOT LIKE '0054%s'") % (cod, cod, cod, cod)
					aux = ("%s AND numeroDestino NOT LIKE '0%s' AND numeroDestino NOT LIKE '%s' AND numeroDestino NOT LIKE '00549%s' AND numeroDestino NOT LIKE '0054%s') AND ") % (aux, cod, cod, cod, cod)
				elif item[2] == 1:
					aux = ("(numeroOrigen NOT LIKE '0%s' AND numeroOrigen NOT LIKE '%s' AND numeroOrigen NOT LIKE '00549%s' AND numeroOrigen NOT LIKE '0054%s') AND ") % (cod, cod, cod, cod)
				else: #entonces solo queda item[2] == 2
					aux = ("(numeroDestino NOT LIKE '0%s' AND numeroDestino NOT LIKE '%s' AND numeroDestino NOT LIKE '00549%s' AND numeroDestino NOT LIKE '0054%s') AND ") % (cod, cod, cod, cod)
			else: # Entonces es igual
				if item[2] == 0:
					aux = ("(numeroOrigen LIKE '0%s' OR numeroOrigen LIKE '%s' OR numeroOrigen LIKE '00549%s' OR numeroOrigen LIKE '0054%s'") % (cod, cod, cod, cod)
					aux = ("%s OR numeroDestino LIKE '0%s' OR numeroDestino LIKE '%s' OR numeroDestino LIKE '00549%s' OR numeroDestino LIKE '0054%s') AND ") % (aux, cod, cod, cod, cod)
				elif item[2] == 1:
					aux = ("(numeroOrigen LIKE '0%s' OR numeroOrigen LIKE '%s' OR numeroOrigen LIKE '00549%s' OR numeroOrigen LIKE '0054%s') AND ") % (cod, cod, cod, cod)
				else: #entonces solo queda item[2] == 2
					aux = ("(numeroDestino LIKE '0%s' OR numeroDestino LIKE '%s' OR numeroDestino LIKE '00549%s' OR numeroDestino LIKE '0054%s') AND ") % (cod, cod, cod, cod)
		else:
			if item[1] == "distinto":
				if item[2] == 0:
					aux = ("(numeroOrigen NOT LIKE '0%s' AND numeroOrigen NOT LIKE '%s' AND numeroOrigen NOT LIKE '00549%s' AND numeroOrigen NOT LIKE '0054%s'") % (cod, cod, cod, cod)
					aux = ("%s AND numeroDestino NOT LIKE '0%s' AND numeroDestino NOT LIKE '%s' AND numeroDestino NOT LIKE '00549%s' AND numeroDestino NOT LIKE '0054%s')") % (aux, cod, cod, cod, cod)
				elif item[2] == 1:
					aux = ("(numeroOrigen NOT LIKE '0%s' AND numeroOrigen NOT LIKE '%s' AND numeroOrigen NOT LIKE '00549%s' AND numeroOrigen NOT LIKE '0054%s')") % (cod, cod, cod, cod)
				else: #entonces solo queda item[2] == 2
					aux = ("(numeroDestino NOT LIKE '0%s' AND numeroDestino NOT LIKE '%s' AND numeroDestino NOT LIKE '00549%s' AND numeroDestino NOT LIKE '0054%s')") % (cod, cod, cod, cod)
			else: # Entonces es igual
				if item[2] == 0:
					aux = ("(numeroOrigen LIKE '0%s' OR numeroOrigen LIKE '%s' OR numeroOrigen LIKE '00549%s' OR numeroOrigen LIKE '0054%s'") % (cod, cod, cod, cod)
					aux = ("%s OR numeroDestino LIKE '0%s' OR numeroDestino LIKE '%s' OR numeroDestino LIKE '00549%s' OR numeroDestino LIKE '0054%s')") % (aux, cod, cod, cod, cod)
				elif item[2] == 1:
					aux = ("(numeroOrigen LIKE '0%s' OR numeroOrigen LIKE '%s' OR numeroOrigen LIKE '00549%s' OR numeroOrigen LIKE '0054%s')") % (cod, cod, cod, cod)
				else: #entonces solo queda item[2] == 2
					aux = ("(numeroDestino LIKE '0%s' OR numeroDestino LIKE '%s' OR numeroDestino LIKE '00549%s' OR numeroDestino LIKE '0054%s')") % (cod, cod, cod, cod)
		return aux
		
		
	def busqueda(self, listaBusqueda, listaSalida):
		listaSalida.pop()
		query = QtSql.QSqlQuery()
		consulta = "SELECT "
		indice = 0
		for item in listaSalida:
			consulta = consulta + item + ", "
		
		consulta = consulta + "nombreArchivo "
		consulta = consulta + "FROM " + self.nombreTabla + " WHERE "
		
		indice = 0
		for item in listaBusqueda:
			if indice != len(listaBusqueda) - 1:
				if item[0] in {"fecha", "duracion", "hora"}:
					consulta = consulta + item[0] + " BETWEEN " + "'" + item[1] + "'" + " AND "+ "'" + item[2] + "'" + " AND "
				elif item[0] == "codigoArea":
					consulta = consulta + self.armarLikes(item, False)
				else:
					consulta = consulta + item[0] + " = " + "'" + item[1] + "'" + " AND "
			else:
				if item[0] in {"fecha", "duracion", "hora"}:
					consulta = consulta + item[0] + " BETWEEN " + "'" + item[1] + "'" + " AND "+ "'" + item[2] + "'"
				elif item[0] == "codigoArea":
					consulta = consulta + self.armarLikes(item, True)
				else:
					consulta = consulta + item[0] + " = " + "'" + item[1] + "'"
			indice = indice + 1
		
		
		if consulta in self.listaConsultas:
			print "Pasamos por aca pero no devuelvo -1"
			return -1
		self.listaConsultas.append(consulta)
		query.exec_(consulta)
		listaSalida.append("nombreArchivo")
		return query
	
	def eliminarHistorialConsultas(self):
		self.listaConsultas = []
	
	
	def reestriccionesAnteriores(self):
		resultado = []
		for item in self.listaConsultas:
			resultado.append(item.split("WHERE ")[1])
		return resultado
			
	
	def refinarBusqueda(self, listaBusqueda, listaSalida, cantRef):
		consulta = "SELECT "
		for item in listaSalida:
			consulta = consulta + item + ", "
		consulta = consulta + "nombreArchivo"
		
		consulta = consulta + " FROM ("
		
		if cantRef == 1:
			#Subconsulta
			subconsulta = "SELECT *"
			listaAux = self.reestriccionesAnteriores()
			subconsulta = subconsulta + " FROM " + self.nombreTabla
			subconsulta = subconsulta + " WHERE " 
			for indice in range(len(listaAux) - 1):
				subconsulta = subconsulta + "(" + listaAux[indice] + ")" + " OR "
			subconsulta = subconsulta + "(" + listaAux[len(listaAux) - 1] + ")"
		else:
			aux = ", "
			listaSalida.append("nombreArchivo")
			aux = aux.join(listaSalida)
			subconsulta = self.listaConsultas[0]
			subconsulta = subconsulta.replace(aux, "*")
			listaSalida.pop()
					
		consulta = consulta + subconsulta + ") AS S WHERE "	
		indice = 0
		for item in listaBusqueda:
			if indice != len(listaBusqueda) - 1:
				if item[0] in {"fecha", "duracion", "hora"}:
					consulta = consulta + item[0] + " BETWEEN " + "'" + item[1] + "'" + " AND "+ "'" + item[2] + "'" + " AND "
				else:
					consulta = consulta + item[0] + " = " + "'" + item[1] + "'" + " AND "
			else:
				if item[0] in {"fecha", "duracion", "hora"}:
					consulta = consulta + item[0] + " BETWEEN " + "'" + item[1] + "'" + " AND "+ "'" + item[2] + "'"
				else:
					consulta = consulta + item[0] + " = " + "'" + item[1] + "'"
			indice = indice + 1
		
		query = QtSql.QSqlQuery()
		self.eliminarHistorialConsultas()
		self.listaConsultas.append(consulta)
		query.exec_(consulta)
		print "La consulta refinada"
		print consulta
		return query