import xlrd, xlwt
import mysql.connector
from ..Diccionario.Diccionario import Diccionario


class ParserClaro:
	def __init__(self, nomSabana):
		self.book = xlrd.open_workbook(nomSabana)
		self.sheet = self.book.sheet_by_index(0)
		self.filas = self.sheet.nrows
		self.columnas = self.sheet.ncols
		self.index = 0
		self.diccionario = Diccionario()
		self.listaConceptos = self.diccionario.listaConceptos
		self.conceptosSabana = []

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

#Devuelve una lista con todos los nombres de columnas de la tabla y ademas
#genera otra con los conceptos equivalentes en el mismo orden
	def nombresColumnas(self):
		for colums in range(self.columnas):
			self.encabezados = self.sheet.row_values(self.index,0,self.columnas)

		for i in range(len(self.encabezados)):
			concepto = self.diccionario.sinonimoDe(self.encabezados[i])
			self.conceptosSabana.append(concepto)

#Crea una sabana temporal donde aparecen todos los conceptos que se manejan
#Si la sabana no tiene informacion de los conceptos los deja en blanco
	def nuevaSabana(self, dbName):
		bookNuevo = xlwt.Workbook()
		sheetNuevo = bookNuevo.add_sheet('pagina 1')
		for i in range(len(self.listaConceptos)):
			sheetNuevo.row(0).write(i, self.listaConceptos[i])

		fechaHora = self.conceptosSabana.index('fechaInicio')
				
		for row in range(self.index + 1, self.filas):
			for concept in range(len(self.conceptosSabana)):
				if self.conceptosSabana[concept] != 'fechaInicio':
					fh = sheetNuevo.cell_value(row, concept)
					listaFH = fh.split()

					sheetNuevo.row(row-self.index).write(self.listaConceptos.index('fechaInicio'), listaFH[0])
					sheetNuevo.row(row-self.index).write(self.listaConceptos.index('horaInicio'), listaFH[1])
				else:	
					sheetNuevo.row(row-self.index).write(self.listaConceptos.index(self.conceptosSabana[concept]),
					self.sheet.cell_value(row, concept))

		bookNuevo.save('temp.xls')



class ParserPersonal:
	def __init__(self, nomSabana):
		self.book = xlrd.open_workbook(nomSabana)
		self.sheet = self.book.sheet_by_index(0)
		self.filas = self.sheet.nrows
		self.columnas = self.sheet.ncols
		self.index = 0
		self.diccionario = Diccionario()
		self.listaConceptos = self.diccionario.listaConceptos
		self.conceptosSabana = []


	def quitarEncabezado(self):
		bookNuevo = xlwt.Workbook()
		flag = True
		while flag:
			if self.sheet.cell_type(self.index, 0) != xlrd.XL_CELL_EMPTY:
				flag = False
			else:
				self.index = self.index + 1
		return self.index


	def nombresColumnas(self):
		for colums in range(self.columnas):
			self.encabezados = self.sheet.row_values(self.index,0,self.columnas)

		for i in range(len(self.encabezados)):
			concepto = self.diccionario.sinonimoDe(self.encabezados[i])
			self.conceptosSabana.append(concepto)

	def lineasTotales(self,col):
		index1 = self.index + 1
		lista = []
		for rows in range(index1, self.filas - 1):
			linea = self.sheet.cell_value(rows,col)
			if not(linea in lista):
				lista.append(self.linea)
		return lista

	def nuevaSabana(self):
		bookNuevo = xlwt.Workbook()
		sheetNuevo = bookNuevo.add_sheet('pagina 1')
		for i in range(len(self.listaConceptos)):
			sheetNuevo.row(0).write(i, self.listaConceptos[i])

		tipoLlamada = self.conceptosSabana.index('')
		linea = self.conceptosSabana.index('numeroOrigen')
		otro = self.conceptosSabana.index('numeroDestino')
		numeroOrig = self.listaConceptos.index('numeroOrigen')
		numeroDest = self.listaConceptos.index('numeroDestino')
				
		for row in range(self.index + 1, self.filas):
			for concept in range(len(self.conceptosSabana)):
				if self.conceptosSabana[concept] != '':
					if self.sheet.cell_value(row, tipoLlamada) == 'E':
						if self.conceptosSabana[concept] == 'numeroOrigen':
							sheetNuevo.row(row-self.index).write(numeroOrig, self.sheet.cell_value(row, otro))
						elif self.conceptosSabana[concept] == 'numeroDestino':
							sheetNuevo.row(row-self.index).write(numeroDest, self.sheet.cell_value(row, linea))
						else:	
							sheetNuevo.row(row-self.index).write(self.listaConceptos.index(self.conceptosSabana[concept]),
							self.sheet.cell_value(row, concept))
					else:	
						sheetNuevo.row(row-self.index).write(self.listaConceptos.index(self.conceptosSabana[concept]),
						self.sheet.cell_value(row, concept))

		bookNuevo.save('temp.xls')


	def armarConsulta(self, server, user, password, dataBase):
		archSabana = xlrd.open_workbook('temp.xls')
		sheet = archSabana.sheet_by_index(0)
		index = 0
		
		cnx = mysql.connector.connect(user=user, password=password, host=server, database=dataBase)
		cursor = cnx.cursor()

		encabezados = sheet.row_values(index,0,sheet.ncols)

		crear = "CREATE TABLE IF NOT EXISTS Sabana ("

		for i in range(len(encabezados)-1):
			if encabezados[i] == 'fechaInicio' or encabezados[i] == 'fechaFin':
				crear = crear + encabezados[i] + " DATE, "
			elif encabezados[i] == 'horaInicio' or encabezados[i] == 'horaFin':
				crear = crear + encabezados[i] + " TIME, "
			else:
				crear = crear + encabezados[i] + " TEXT, "
		crear = crear + encabezados[i+1] + " TEXT" + ')'
		
		cursor.execute(crear)
		
		for fila in range(1, sheet.nrows):
			index = index + 1
			row = sheet.row_values(index, 0, sheet.ncols)
			valores = "("
			for dato in range(0, len(row)):
				if dato != len(row)-1:
					if str(row[dato]) == '':
						valores = valores + "'NULL'" + ","
					else:	
						valores = valores + "'" + str(row[dato]) + "'" + ","
				else:
					if str(row[dato]) == '':
						valores = valores + "'NULL'" + ")"
					else:
						valores = valores + "'" + str(row[dato]) + "'" + ")"
			insertar = "INSERT INTO " + "Sabana" + " VALUES" + valores
			print insertar
			cursor.execute(insertar)
			cnx.commit()


#sabana = ParserPersonal('sabana.xls')
#sabana.quitarEncabezado()
#sabana.nombresColumnas()
#print sabana.conceptosSabana
#sabana.nuevaSabana()
#sabana.armarConsulta("localhost", "root", "root", "Sabanas")
