# *-* coding: utf-8 *-* 
import xlrd, xlwt
from Diccionario.Diccionario import Diccionario
from Sabana import *
import os

class ParserClaro:
	def __init__(self, sabana = None, nomSabana = ''):
		if nomSabana != '':
			self.nombreArchivo = unicode (nomSabana, "latin")
		else:
			self.nombreArchivo = unicode(sabana.nombreArchivo, "latin")
			self.book = xlrd.open_workbook(sabana.nombreArchivo)
			self.sabana = sabana
			temp = self.sabana.nombreArchivo.split('.xls')
			self.archivoTemporal = temp[0] + "_temp.xls"
			self.sheet[0] = self.book.sheet_by_index(0)
			self.sheet[1] = self.book.sheet_by_index(1)
			self.filas = self.sheet.nrows
			self.columnas = self.sheet.ncols
			self.index = 0
			self.diccionario = Diccionario()
			self.quitarEncabezado()

		
	def eliminarArchivoTemporal(self):
		#os.remove(str(self.archivoTemporal))
		pass
	def obtenerLineas(self):
		book = xlrd.open_workbook(self.archivoTemporal)
		sheet = book.sheet_by_index(0)
		columnas = sheet.ncols
		filas = sheet.nrows
		lineas = []
		for row in range(1, filas):
			linea = sheet.row_values(row,0,columnas)
			lineaAux = []
			for item in range(len(linea)):
				aux = linea[item].strip()
				lineaAux.append(aux)
			lineas.append(lineaAux)	
		return lineas
		
	
	def esSabanaClaro(self):
		esSabanaClaro = False
		if self.nombreArchivo.endswith(".xls"):
			self.book = xlrd.open_workbook(self.nombreArchivo)
			self.sheet = self.book.sheet_by_index(0)
			self.filas = self.sheet.nrows
			self.columnas = self.sheet.ncols
			self.index = 0
			self.quitarEncabezado()
			if self.index == 11 and self.sheet.cell_value(self.index, 0) == 'Nro. Llamante':
				esSabanaClaro = True

		return esSabanaClaro

#Lleva index hasta la linea donde comienza la informacion importante
#index ahora apunta a la linea con los titulos de columnas.
	def quitarEncabezado(self):
		bookNuevo = xlwt.Workbook()
		flag = True
		while flag:
			if self.sheet.cell_type(self.index, 1) != xlrd.XL_CELL_EMPTY:
				flag = False
			else:
				self.index = self.index + 1
		return self.index

#Devuelve una lista con todos los nombres de columnas de la tabla
	def obtenerEncabezados(self):
		encabezados = []
		for colums in range(self.columnas):
			listaAux = self.sheet.row_values(self.index,0,self.columnas)
		for item in listaAux:
			encabezados.append(item.strip())
		return encabezados
		
	
	def hhmmss(self, segundostotales):
		resultado = []
		if segundostotales != '':
			segundostotales = int(segundostotales)
			hh = segundostotales // 3600
			mm = (segundostotales % 3600)//60
			ss = (segundostotales %3600) %60
			resultado = [str(hh).zfill(2),str(mm).zfill(2),str(ss).zfill(2)]
		else:
			resultado = ['00', '00','00']
		return resultado
		
#Crea una sabana temporal donde aparecen todos los conceptos que se manejan
#Si la sabana no tiene informacion de los conceptos los deja en blanco
	def crearArchivoTemporal(self):
		fechaNull = '18000101'
		horaNull = '25:00:00'
		bookNuevo = xlwt.Workbook()
		sheetNuevo = bookNuevo.add_sheet('pagina 1')
		type = ""
		self.diccionario.listaConceptos.pop()
		self.diccionario.listaConceptos.append("nombreArchivo")
		for i in range(len(self.diccionario.listaConceptos)):
			sheetNuevo.row(0).write(i, self.diccionario.listaConceptos[i])
		
		encabezados = self.obtenerEncabezados()
		print encabezados
		fechaHora = encabezados.index('Fecha y Hora')
		duracionIndex = encabezados.index(unicode('Duración (Seg.)', "latin"))
		tipoLlamada = encabezados.index('Destino')
			
		for i in range(0, 1):		
			for row in range(self.index + 1, self.filas):
				for concept in range(len(self.sabana.listaTuplas)):
					if self.sabana.listaTuplas[concept][1][0] == "fecha" or self.sabana.listaTuplas[concept][1][0] == "hora":
						if self.sheet[i].cell_type(row, fechaHora) != xlrd.XL_CELL_EMPTY:
							fh = xlrd.xldate_as_tuple(self.sheet[i].cell_value(row, fechaHora), self.book.datemode)
							fecha = str(fh[0])+str(fh[1])+'0'+str(fh[2])
							hora = str(fh[3])+":"+str(fh[4])+":"+str(fh[5])
							sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index('fecha'), fecha)
							sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index('hora'), hora)
						else:
							sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index('fecha'), fechaNull)
							sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index('hora'), horaNull)
					elif self.sabana.listaTuplas[concept][1][0] == "duracion":
						aux = ":"
						segundos = self.sheet[i].cell_value(row, duracionIndex)
						segundos = self.hhmmss(segundos)
						duracion = aux.join(segundos)
						sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index('duracion'), duracion)
					elif self.sabana.listaTuplas[concept][1][0] == "tipoComunicacion":
						if self.sheet[i].cell_value(row, tipoLlamada).find("Mensajes") != -1:
							sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index('tipoComunicacion'), "Mensaje")
						else:
							sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index('tipoComunicacion'), "Llamada")
					else:
						sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index(self.sabana.listaTuplas[concept][1][0]),
						self.control(self.sheet[i].cell_value(row, encabezados.index(self.sabana.listaTuplas[concept][0]))))

				sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index("nombreArchivo"),
						unicode(self.sabana.nombreArchivo, "latin"))
			
		bookNuevo.save(self.archivoTemporal)

		
	def control(self, item):
		if isinstance(item, int) or isinstance(item, float):
			item = str(item)
			lista = item.split('.')
			item = lista[0]
			item.replace(" ", "")
		return item
