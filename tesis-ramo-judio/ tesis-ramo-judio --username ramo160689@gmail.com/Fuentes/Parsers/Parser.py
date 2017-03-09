
from ParserPersonal import *
from DBmanager import*
from ParserClaro import *
from ParserNextel import *
from ParserMovistar import *
from ParserPropio import *
from DBmanager import *



class Parser:
	def __init__ (self, nombreArchivo = '', nombreEmpresa = ''):
		self.nombreEmpresa = nombreEmpresa
		self.nombreArchivo = nombreArchivo
			
	
	def nombreColumnas(self):
		if self.nombreEmpresa=="Personal":
			parsePersonal = ParserPersonal(nomSabana = self.nombreArchivo)
			if parsePersonal and parsePersonal.esSabanaPersonal():
				return parsePersonal.obtenerEncabezados()
			else:
				return "ERROR_EMPRESA"
		elif self.nombreEmpresa == "Movistar":
			parseMovistar = ParserMovistar(nomSabana = self.nombreArchivo)
			if parseMovistar.esSabanaMovistar():
				return parseMovistar.obtenerEncabezados()
			else:
				return "ERROR_EMPRESA"
		elif self.nombreEmpresa=="Claro":
			parseClaro = ParserClaro(nomSabana = self.nombreArchivo)
			if parseClaro.esSabanaClaro():
				return parseClaro.obtenerEncabezados()
			else:
				return "ERROR_EMPRESA"
		elif self.nombreEmpresa == "Nextel":
			parseNextel = ParserNextel(nomSabana = self.nombreArchivo)
			if parseNextel.esSabanaNextel():
				return parseNextel.obtenerEncabezados()
			else:
				return "ERROR_EMPRESA"
		elif self.nombreEmpresa=="Resultado Anterior":
			parsePropio = ParserPropio(nomSabana = self.nombreArchivo)
			if parsePropio.esSabanaPropio():
				return parsePropio.obtenerEncabezados()
			else:
				return "ERROR_EMPRESA"
		else:
			print ("No existe la empresa %s", self.nombreEmpresa)


	def parsear(self, cjtoSabanas):
		db = dbManager()
		for item in cjtoSabanas.listaSabanas:
			if item.nombreEmpresa == "Personal":
				parsePersonal = ParserPersonal(item)
				parsePersonal.crearArchivoTemporal()
				lista = parsePersonal.obtenerLineas()
				for item in lista:
					db.insertarRegistroDB(item)
				parsePersonal.eliminarArchivoTemporal()
			elif item.nombreEmpresa == "Movistar":
				parseMovistar = ParserMovistar(item)
				parseMovistar.crearArchivoTemporal()
				lista = parseMovistar.obtenerLineas()
				flag = False
				for item in lista:
					if item != ["-1"]:
						db.insertarRegistroDB(item)
					else:
						flag = True
				parseMovistar.eliminarArchivoTemporal()
				if flag:
					return -1
			elif item.nombreEmpresa=="Nextel":
				parseNextel = ParserNextel(item)
				parseNextel.crearArchivoTemporal()
				lista = parseNextel.obtenerLineas()
				for item in lista:
					db.insertarRegistroDB(item)
				parseNextel.eliminarArchivoTemporal()
			elif item.nombreEmpresa=="Claro":
				parseClaro = ParserClaro(item)
				parseClaro.crearArchivoTemporal()
				lista = parseClaro.obtenerLineas()
				for item in lista:
					db.insertarRegistroDB(item)
				parseClaro.eliminarArchivoTemporal()
			else:
				parsePropio = ParserPropio(item)
				parsePropio.crearArchivoTemporal()
				lista = parsePropio.obtenerLineas()
				for item in lista:
					db.insertarRegistroDB(item)
				parsePropio.eliminarArchivoTemporal()