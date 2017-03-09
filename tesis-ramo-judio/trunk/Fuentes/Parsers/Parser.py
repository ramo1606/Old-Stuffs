import ParserPersonal, ParserClaro


class Parser(object):
	
	# tupla es de la forma (archivo, empresa)
	def listaEncabezados(self, tupla):
		lista = ["Nro. Pagador", "Destino", "Fecha I.", "Fecha-Hora Recibido", "Dir. Orig.", "Celda (NOMBRE[ORIENTACION]<>UBICACION<>DIRECCION)", "Celda localidad"]
		empresa = tupla[1]
		# lista = []
		# if empresa==Personal:
			# pPersonal = ParserPersonal(archivo)
			# lista = pPersonal.nombresColumnas()			
		# elif empresa==Movistar:
			# pMovistar = ParserMovistar(self, archivo)
			# lista = pMovistar.nombresColumnas()
		# elif empresa==Claro:
			# pClaro = ParserClaro(self, archivo, encabezados)
			# lista = pClaro.nombresColumnas()
		# elif empresa==Nextel:
			# pNextel = ParserNextel(self, archivo)
			# lista = pNextel.nombresColumnas()
		# else
			# print ("No existe la empresa %s", empresa)
	
		if empresa=="Personal":
			print "Personal"
		elif empresa=="Movistar":
			print "Movistar"
		elif empresa=="Claro":
			print "Claro"
		elif empresa=="Nextel":
			print "Nextel"
		else:
			print ("No existe la empresa %s", empresa)
		return lista
	# def parse(self, empresa, archivo, encabezados):
		# if empresa=Personal:
			# parserPersonal(self, archivo, encabezados)
		# else if empresa=Movistar:
			# parserMovistar(self, archivo, encabezados)
		# else if empresa=Claro:
			# parserClaro(self, archivo, encabezados)
		# else if empresa=Nextel:
			# parserNextel(self, archivo, encabezados)
		# else
			# print ("No existe la empresa %s", empresa)
	def chequearEmpresa(self, archivo, empresa):
		return True