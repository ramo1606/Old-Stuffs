



#Modificar inicio informacion
#de ahi sacar el valor self.listaTuplas

from ..Diccionario.Diccionario import Diccionario
import os

#formato de listaConceptos [(concepto, sinonimo), ....]

class ParserClaro:
	def __init__(self, nomSabana):
		self.listaTuplas = []
		self.sabana = nomSabana
		self.sabanaTemp = nomSabana.split(".")[0] + "Temp.tmp"
		self.inicioDatos = self.inicioInformacion()
		self.nomTabla = "ejemplo"
		#self.conceptoUbi = self.conceptoUbicacion()

		
		
	#metodo que retorna el valor en bytes desde donde comienza la
	#informacion reelevante.
	def inicioInformacion(self):
		dic = Diccionario()
		archSabana = open(self.sabana, "r")
		flag = True
		resultado = 0
		#Siempre debe haber un telefono de origen.
		while flag:
			linea = archSabana.readline().split(";")
			for item in linea:
				if dic.sinonimoDe(item) == "numeroOrigen":
					flag = False
			resultado = resultado + 1	
		archSabana.close()
		return resultado - 1
	
	#Metodo que retorna una lista de tuplas de la forma 
	#[(concepto, ubicacion)], donde ubicacion seria la columna.
	def conceptoUbicacion(self):
		archSabana = open(self.sabana, "r")
		#Nos posicionamos en la linea de inicio de informacion
		for i in range(0,fin):
			archSabana.readline().split(";")
		#Elimino el \n del final
		encabezados = archSabana.readline().split("\n")[0].split(";")
		i = 0
		lista = []
		for item in encabezados:
			j = 0
			flag = True
			while flag and j < len(self.listaTuplas):
				if item == self.listaTuplas[j][1]:
					tupla = (self.listaTuplas[j][0], i)
					lista.append(tupla)
					flag = False
					i = i + 1		
				j = j + 1
			if flag:
				if item != "":
					print "Concepto del sinonimo '" + item +  "' no encontrado"
				else:
					print "Sinonimo vacio"
		archSabana.close()
		return lista
		
	def get_ubucacion(self, concepto):
		flag = True
		index = 0
		resultado = -1
		while flag and index < len(self.conceptoUbi):
			if self.conceptoUbi[0] == concepto:
				flag = False
				resultado = self.conceptoUbi[1]
			else:
				index = index + 1
		return resultado
	
	#INSERT INTO `esquema`.`tabla` (`col1`,`col2`) VALUES ('val1','val2');	
	#INSERT INTO table_name
	#VALUES (value1, value2, value3,...)	
	#[(concepto, ubicacion)] tupla de trabajo
	def armarConsulta(self):
		listaConUbi = self.conceptoUbi
		self.prepararArchivo()
		archSabana = open(self.sabanaTemp, "r")
		cons = ""
		for linea in archSabana:
			columnas = "("
			valores = "("
			index = 0
			linea = linea.split("\n")[0].split(";")
			#lista de concepto valor para crear la consulta
			while len(linea) > 1 and index < len(listaConUbi):
				if index == len(listaConUbi) - 1:
					columnas = columnas + listaConUbi[index][0] + ")"
					valores = valores + "'" + linea[listaConUbi[index][1]] + "'" + ")"
				else:
					if listaConUbi[index][0].find("fecha") != -1:
						fechaCompleta = self.parseFechaHora(linea[listaConUbi[index][1]], listaConUbi[index][0])
						for item in fechaCompleta:
							columnas = columnas + item[0] + ","
							valores = valores + "'" + item[1] + "'" + ","
					elif listaConUbi[index][0] == "antenaDireccion":
						dirCompleta = self.parseDireccionAntena(linea[listaConUbi[index][1]])
						for item in dirCompleta:
							columnas = columnas + item[0] + ","
							valores = valores + "'" + item[1] + "'" + ","
					else:		
						columnas = columnas + listaConUbi[index][0] + ","
						valores = valores + "'" + linea[listaConUbi[index][1]] + "'" + ","
				index = index + 1
			if len(linea) > 1:
				cons = cons + "INSERT INTO " + self.nomTabla + columnas
				cons = cons + " VALUES " + valores + ";\n"
		archSabana.close()
		os.remove(self.sabanaTemp)
		return cons

	def prepararArchivo(self):
		archSabana = open(self.sabana, "r")
		archSabana.seek(self.inicioDatos, 0)
		archSalida = open(self.sabanaTemp, "w")
		archSabana.readline()
		for linea in archSabana:
			linea = linea.replace(" .", "")
			archSalida.write(linea)
		
		
		archSalida.close()
		archSabana.close()
	
	
	
	
	# Celda (NOMBRE[ORIENTACION]<>UBICACION<>DIRECCION)
			
	#Metodo que retorna una lista de tuplas (concepto, valor) lista
	#para ser cargada en la BD
	def parseDireccionAntena(self, direccion):
		result = ""
		if direccion != "":
			dirAntena = direccion.split("<>")
			antenaLocalidad = dirAntena[2].split("-")[1]
			antenaDireccion = dirAntena[0] + dirAntena[2].split("-")[0]
			antenaProvincia = dirAntena[1]
			antenaLocalidad.replace(" ", "")
			antenaProvincia.replace(" ", "")
			result =  [("antenaLocalidad", antenaLocalidad), ("antenaDireccion", antenaDireccion), ("antenaProvincia", antenaProvincia)]
		else:
			result =  [("antenaLocalidad", ""), ("antenaDireccion", ""), ("antenaProvincia", "")]
		return result
	
	def parseFechaHora(self, hs, concepto):
		result = ""
		if len(hs) > 0:
			hora = hs.split(" ")[1]
			fecha = hs.split(" ")[0]
			fecha = fecha.split("/")
			fecha.reverse()
			fecha = fecha[0] + "/" + fecha[1]+ "/" + fecha[2]
			if concepto.find("Inicio") != -1:
				result =  [("fechaInicio", fecha), ("horaInicio", hora)]
			elif concepto.find("Fin") != -1:
				result =  [("fechaFin", fecha), ("horaFin", hora)]		
		else:
			if concepto.find("Inicio") != -1:
				result =  [("fechaInicio", "25:00:00"), ("horaInicio", "25:00:00")]
			elif concepto.find("Fin") != -1:
				result =  [("fechaFin", ""), ("horaFin", "")]
		return result
		
	""""CREATE TABLE example (
         id INT,
         data VARCHAR(100)
       );"""
	def metodoejemplo(self, lista):
		create = "CREATE TABLE `sabanas`.`ejemplo` ("
		for item in lista:
			if item[0].find("fecha") != -1:
				create = create + item[0] + " DATE,"
			elif item[0].find("hora") != -1:
				create = create + item[0] + " TIME,"
			else:
				create = create + item[0] + " TEXT,"
				
		create = create + ");"
		open("borrar.txt", "w").write(create)

		
	def nombresColumnas(self):
		return ["Nro. Pagador", "Destino", "Fecha I.", "Fecha-Hora Recibido", "Dir. Orig.", "Celda (NOMBRE[ORIENTACION]<>UBICACION<>DIRECCION)", "Celda localidad"]
	

# dic = Diccionario()
#archSabana = open("sabanaClaro.csv", "r")
# archSabana.close()


# archSabana = open("sabanaClaro.csv", "r")
# archSabana.seek(162, 0)
# Elimino el \n del final
# encabezados = archSabana.readline().split("\n")[0].split(";")
# i = 0
# lista = []
# dic = Diccionario()
# for item in encabezados:
	# tupla = (dic.sinonimoDe(item), item)
	# lista.append(tupla)

		
# archSabana.close()


#a = ParserClaro('sabanaClaro.csv')


# arch = open("consulta.txt", "w")
# a.prepararArchivo()

# a.metodoejemplo(lista)
# arch.write(a.armarConsulta())
