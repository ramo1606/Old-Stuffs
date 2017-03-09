import xlrd, xlwt
from Diccionario.Diccionario import Diccionario
from Sabana import *
import os


class ParserPropio:
	def __init__(self, sabana = None, nomSabana = ''):
		if nomSabana != '':
			self.nombreArchivo = unicode(nomSabana, "latin")
		else:
			self.book = xlrd.open_workbook(sabana.nombreArchivo)
			self.sabana = sabana
			temp = self.sabana.nombreArchivo.split('.xls')
			self.archivoTemporal = temp[0] + "_temp.xls"
			self.sheet = self.book.sheet_by_index(0)
			self.filas = self.sheet.nrows
			self.columnas = self.sheet.ncols
			self.index = 0
			self.diccionario = Diccionario()
			self.quitarEncabezado()
		

	
	def eliminarArchivoTemporal(self):
		os.remove(str(self.archivoTemporal))
	
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
	
		
	def esSabanaPropio(self):
		esSabanaPropio = False
		if self.nombreArchivo.endswith(".xls"):
			self.sheet = self.book.sheet_by_index(0)
			self.filas = self.sheet.nrows
			self.columnas = self.sheet.ncols
			self.index = 0
			self.diccionario = Diccionario()
			self.quitarEncabezado()
			if self.index == 0:
				esSabanaPropio = True
				
		return esSabanaPropio

	def quitarEncabezado(self):
		flag = True
		while flag:
			if self.sheet.cell_type(self.index, 0) != xlrd.XL_CELL_EMPTY:
				flag = False
			else:
				self.index = self.index + 1
		return self.index


	def obtenerEncabezados(self):
		for colums in range(self.columnas):
			encabezados = self.sheet.row_values(self.index,0,self.columnas)
		return encabezados
		

	def lineasTotales(self,col):
		index1 = self.index + 1
		lista = []
		for rows in range(index1, self.filas - 1):
			linea = self.sheet.cell_value(rows,col)
			if not(linea in lista):
				lista.append(self.linea)
		return lista

	def crearArchivoTemporal(self):
		bookNuevo = xlwt.Workbook()
		sheetNuevo = bookNuevo.add_sheet('pagina 1')
		self.diccionario.listaConceptos.pop()
		self.diccionario.listaConceptos.append("nombreArchivo")
		for i in range(len(self.diccionario.listaConceptos)):
			sheetNuevo.row(0).write(i, self.diccionario.listaConceptos[i])

		encabezados = self.obtenerEncabezados()
						
		for row in range(self.index + 1, self.filas):
			for concept in range(len(self.sabana.listaTuplas)):
				sheetNuevo.row(row-self.index).write(self.diccionario.listaConceptos.index(self.sabana.listaTuplas[concept][1][0]),
				self.control(self.sheet.cell_value(row, concept)))
			
		bookNuevo.save(self.archivoTemporal)


	def control(self, item):
		if isinstance(item, int) or isinstance(item, float):
			item = str(item)
			lista = item.split('.')
			item = lista[0]
			item.replace(" ", "")
		return item