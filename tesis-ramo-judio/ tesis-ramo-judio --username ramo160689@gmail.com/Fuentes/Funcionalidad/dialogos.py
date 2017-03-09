#!/usr/bin/env python
# *-* coding: utf-8 *-*
from PyQt4 import QtCore, QtGui, QtWebKit
from Fuentes.Parsers.DBmanager import *
from Fuentes.Funcionalidad.Pagina2 import *

from Fuentes.Funcionalidad.Pagina3 import *

class UbicacionMapa(QtGui.QDialog):

	def __init__(self, url, parent=None):
		super(UbicacionMapa, self).__init__(parent)
		self.resize(640,480)
		self.setWindowTitle("Mapa de la Ubicacion")
		mainLayout = QtGui.QVBoxLayout()

		self.html = QtWebKit.QWebView()

		mainLayout.addWidget(self.html)
		self.setLayout(mainLayout)
		self.html.load(QtCore.QUrl(url))
		self.html.show()
		self.exec_()

		

class RefinarBusquedaDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		super(RefinarBusquedaDialog, self).__init__(parent)
		
		self.setWindowTitle("Refinar Búsqueda")
		
		self.listaBusqueda = []
		self.db = dbManager()
		#-------------
		self.grupoBusqueda = QtGui.QGroupBox("Opciones de Búsqueda")

		self.nroOrigenLabel = QtGui.QLabel("Nro. de Origen:")
		self.nroOrigen = QtGui.QLineEdit()
		self.nroOrigen.setCompleter(self.db.obtenerAutocompletar("numeroOrigen"))

		self.nroDestinoLabel = QtGui.QLabel("Nro. de Destino:")
		self.nroDestino = QtGui.QLineEdit()
		self.nroDestino.setCompleter(self.db.obtenerAutocompletar("numeroDestino"))
		
		self.fecha1Label = QtGui.QLabel("Fecha: Desde:")
		self.fecha2Label = QtGui.QLabel("Hasta:")
		self.fechaDesde = QtGui.QDateTimeEdit(QtCore.QDate(1800, 01, 01))
		self.fechaHasta = QtGui.QDateTimeEdit(QtCore.QDate.currentDate())

		
		self.antenaLabel = QtGui.QLabel("Antena:")
		self.antena = QtGui.QComboBox()
		self.antena.addItems(["Todos"] + self.db.obtenerAutocompletar("antenaDireccion", 1))
		
		self.duracionLabel = QtGui.QLabel("Duración: ")
		self.duracionDesde = QtGui.QComboBox()
		self.duracionDesde.addItems(["0 seg.", "30 seg.", "1 min.", "2 min.", "3 min.", "4 min."])
		
		self.duracionHastaLabel = QtGui.QLabel("Hasta: ")
		self.duracionHasta = QtGui.QComboBox()
		self.duracionHasta.addItems(["30 seg.", "1 min.", "2 min.", "3 min.", "4 min.", "5 min.", "más de 5 min."])
		self.duracionHasta.setCurrentIndex(self.duracionHasta.count() - 1)
		
		
		self.horaDesdeLabel = QtGui.QLabel("Hora: Desde")
		self.horaDesde = QtGui.QDateTimeEdit(QtCore.QTime(00,00,00))
		self.horaHastalabel = QtGui.QLabel("Hasta: ")
		self.horaHasta = QtGui.QDateTimeEdit(QtCore.QTime(23,59,59))
		
		self.busquedaLayOut = QtGui.QGridLayout()
		self.busquedaLayOut.addWidget(self.nroOrigenLabel, 0, 0)
		self.busquedaLayOut.addWidget(self.nroOrigen, 0, 1)
		self.busquedaLayOut.addWidget(self.nroDestinoLabel, 0, 2)
		self.busquedaLayOut.addWidget(self.nroDestino, 0, 3)
		self.busquedaLayOut.addWidget(self.fecha1Label, 1, 0)
		self.busquedaLayOut.addWidget(self.fechaDesde, 1, 1)
		self.busquedaLayOut.addWidget(self.fecha2Label, 1, 2)
		self.busquedaLayOut.addWidget(self.fechaHasta, 1, 3)
		self.busquedaLayOut.addWidget(self.horaDesdeLabel, 2, 0)
		self.busquedaLayOut.addWidget(self.horaDesde, 2, 1)
		self.busquedaLayOut.addWidget(self.horaHastalabel, 2, 2)
		self.busquedaLayOut.addWidget(self.horaHasta, 2, 3)
		self.busquedaLayOut.addWidget(self.duracionLabel, 3, 0)
		self.busquedaLayOut.addWidget(self.duracionDesde, 3, 1)
		self.busquedaLayOut.addWidget(self.duracionHastaLabel, 3, 2)
		self.busquedaLayOut.addWidget(self.duracionHasta, 3, 3)
		self.busquedaLayOut.addWidget(self.antenaLabel, 4, 0)
		self.busquedaLayOut.addWidget(self.antena, 4, 1)
		
		#Atributos por codigo de area
		
		self.grupoCodArea = QtGui.QGroupBox("Código de Área")
		self.codAreaOpcIgual = QtGui.QRadioButton("Igual a")
		self.codAreaOpcDistinto = QtGui.QRadioButton("Distinto de")
		self.codAreaOpcDistinto.setChecked(True)
		ceroLabel = QtGui.QLabel("0")
		buscarEnLabel = QtGui.QLabel("buscar en: ")
		self.codLinea = QtGui.QLineEdit()
		self.codLinea.setToolTip("Ingrese el código de área sin 0")
		self.codAreaOpc = QtGui.QComboBox()
		self.codAreaOpc.addItems(["Ambos", "Nro. Origen", "Nro. Destino"])
		self.codAreaOpc.setToolTip("Elija en que números buscar")
		
		
		
		
		#Atributos de Busqueda Avanzada
		self.grupoAvanzada = QtGui.QGroupBox("Búsqueda Avanzada")
		self.imeiLabel = QtGui.QLabel("Nro. Imei:")
		self.nroImei = QtGui.QLineEdit()
		self.nroImei.setCompleter(self.db.obtenerAutocompletar("numeroImei"))
		
		self.simLabel = QtGui.QLabel("Nro. de Sim:")
		self.nroSim = QtGui.QLineEdit()
		self.nroSim.setCompleter(self.db.obtenerAutocompletar("numeroSim"))
		
		self.idCeldaLabel = QtGui.QLabel("Id. de Celda:")
		self.idCelda = QtGui.QComboBox()
		self.idCelda.addItems(["Todos"] + self.db.obtenerAutocompletar("celda", 1))
		
		self.tipoMsjLabel = QtGui.QLabel("Tipo de Comunicacion(Msj/Llamada):")
		self.tipoMsj = QtGui.QComboBox()
		self.tipoMsj.addItems(["Ambos", "Mensaje", "Llamada"])
		self.provAntenaLabel = QtGui.QLabel("Prov. de Antena:")
		self.provAntena = QtGui.QComboBox()
		self.provAntena.addItems(["Todos"] + self.db.obtenerAutocompletar("antenaProvincia", 1))
		
		self.locAntenaLabel = QtGui.QLabel("Loc. de Antena:")
		self.locAntena = QtGui.QComboBox()
		self.locAntena.addItems(["Todos"] + self.db.obtenerAutocompletar("antenaLocalidad", 1))
		
		self.dirOrigenLabel = QtGui.QLabel("Dirección de Nro. Origen:")
		self.dirOrigen = QtGui.QLineEdit()
		self.dirOrigen.setCompleter(self.db.obtenerAutocompletar("direccionOrigen"))
		
		self.dirDestinoLabel = QtGui.QLabel("Dirección de Nro. Destino:")
		self.dirDestino = QtGui.QLineEdit()
		self.dirDestino.setCompleter(self.db.obtenerAutocompletar("direccionDestino"))
		
		self.locOrigenLabel = QtGui.QLabel("Localidad de Nro. Origen:")
		self.locOrigen = QtGui.QLineEdit()
		self.locOrigen.setCompleter(self.db.obtenerAutocompletar("localidadOrigen"))
		
		self.locDestinoLabel = QtGui.QLabel("Localidad de Nro. Destino:")
		self.locDestino = QtGui.QLineEdit()
		self.locDestino.setCompleter(self.db.obtenerAutocompletar("localidadDestino"))
		
		self.provOrigenLabel = QtGui.QLabel("Provincia de Nro. Origen:")
		self.provOrigen = QtGui.QLineEdit()
		self.provOrigen.setCompleter(self.db.obtenerAutocompletar("provinciaOrigen"))
		
		self.provDestinoLabel = QtGui.QLabel("Provincia de Nro. Destino:")
		self.provDestino = QtGui.QLineEdit()
		self.provDestino.setCompleter(self.db.obtenerAutocompletar("provDestino"))
		
		
		self.titularOrigenLabel = QtGui.QLabel("Titular de Nro. Origen:")
		self.titularOrigen = QtGui.QLineEdit()
		self.titularOrigen.setCompleter(self.db.obtenerAutocompletar("titularOrigen"))
		
		self.titularDestinoLabel = QtGui.QLabel("Titular de Nro. Destino:")
		self.titularDestino = QtGui.QLineEdit()
		self.titularDestino.setCompleter(self.db.obtenerAutocompletar("titularDestino"))
		
		self.empOrigenLabel = QtGui.QLabel("Empresa de Nro. Origen:")
		self.empOrigen = QtGui.QLineEdit()
		self.empOrigen.setCompleter(self.db.obtenerAutocompletar("empresaOrigen"))
		
		
		self.empDestinoLabel = QtGui.QLabel("Empresa de Nro. Destino:")
		self.empDestino = QtGui.QLineEdit()
		self.empDestino.setCompleter(self.db.obtenerAutocompletar("empresaDestino"))
		
		self.contMsjLabel = QtGui.QLabel("Contenido de Msj:")
		self.contMsj = QtGui.QLineEdit()
		
		self.estadoMsjLabel = QtGui.QLabel("Estado de Msj:")
		self.estadoMsj = QtGui.QComboBox()
		self.estadoMsj.addItems(["Todos"] + self.db.obtenerAutocompletar("estado", 1))
		
		self.grupoAvanzada.setVisible(False)
		
		self.grupoAvanzadaLayouts = QtGui.QGridLayout()
		self.grupoAvanzadaLayouts.addWidget(self.imeiLabel, 0, 0)
		self.grupoAvanzadaLayouts.addWidget(self.nroImei, 0, 1)
		self.grupoAvanzadaLayouts.addWidget(self.simLabel, 0, 2)
		self.grupoAvanzadaLayouts.addWidget(self.nroSim, 0, 3)
		self.grupoAvanzadaLayouts.addWidget(self.idCeldaLabel, 0, 4)
		self.grupoAvanzadaLayouts.addWidget(self.idCelda, 0, 5)
		self.grupoAvanzadaLayouts.addWidget(self.tipoMsjLabel, 0, 6)
		self.grupoAvanzadaLayouts.addWidget(self.tipoMsj, 0, 7)
		self.grupoAvanzadaLayouts.addWidget(self.provAntenaLabel, 1, 0)
		self.grupoAvanzadaLayouts.addWidget(self.provAntena, 1, 1)
		self.grupoAvanzadaLayouts.addWidget(self.locAntenaLabel, 1, 2)
		self.grupoAvanzadaLayouts.addWidget(self.locAntena, 1, 3)
		self.grupoAvanzadaLayouts.addWidget(self.dirOrigenLabel, 1, 4)
		self.grupoAvanzadaLayouts.addWidget(self.dirOrigen, 1, 5)
		self.grupoAvanzadaLayouts.addWidget(self.dirDestinoLabel, 1, 6)
		self.grupoAvanzadaLayouts.addWidget(self.dirDestino, 1, 7)
		self.grupoAvanzadaLayouts.addWidget(self.locOrigenLabel, 2, 0)
		self.grupoAvanzadaLayouts.addWidget(self.locOrigen, 2, 1)
		self.grupoAvanzadaLayouts.addWidget(self.locDestinoLabel, 2, 2)
		self.grupoAvanzadaLayouts.addWidget(self.locDestino, 2, 3)
		self.grupoAvanzadaLayouts.addWidget(self.provOrigenLabel, 2, 4)
		self.grupoAvanzadaLayouts.addWidget(self.provOrigen, 2, 5)
		self.grupoAvanzadaLayouts.addWidget(self.provDestinoLabel, 2, 6)
		self.grupoAvanzadaLayouts.addWidget(self.provDestino, 2, 7)
		self.grupoAvanzadaLayouts.addWidget(self.titularOrigenLabel, 3, 0)
		self.grupoAvanzadaLayouts.addWidget(self.titularOrigen, 3, 1)
		self.grupoAvanzadaLayouts.addWidget(self.titularDestinoLabel, 3, 2)
		self.grupoAvanzadaLayouts.addWidget(self.titularDestino, 3, 3)
		self.grupoAvanzadaLayouts.addWidget(self.empOrigenLabel, 3, 4)
		self.grupoAvanzadaLayouts.addWidget(self.empOrigen, 3, 5)
		self.grupoAvanzadaLayouts.addWidget(self.empDestinoLabel, 3, 6)
		self.grupoAvanzadaLayouts.addWidget(self.empDestino, 3, 7)
		self.grupoAvanzadaLayouts.addWidget(self.contMsjLabel, 4, 2)
		self.grupoAvanzadaLayouts.addWidget(self.contMsj, 4, 3)
		self.grupoAvanzadaLayouts.addWidget(self.estadoMsjLabel, 4, 4)
		self.grupoAvanzadaLayouts.addWidget(self.estadoMsj, 4, 5)
		
		
		
		
		
		self.avanzadaBoton = QtGui.QPushButton("Búsqueda Avanzada")
		self.avanzadaBoton.setFixedSize(120, 23)
		self.buscarBoton = QtGui.QPushButton("Buscar")
		self.buscarBoton.setFixedSize(120, 23)
		self.limpiarBoton = QtGui.QPushButton("Limpiar Búsqueda")
		self.limpiarBoton.setFixedSize(120, 23)
		avanzadaLayout = QtGui.QHBoxLayout()
		avanzadaLayout.addWidget(self.limpiarBoton)
		avanzadaLayout.addWidget(self.avanzadaBoton)
		avanzadaLayout.addWidget(self.buscarBoton)
		avanzadaLayout.setAlignment(QtCore.Qt.AlignRight)
		
		#Atributos de la Pagina Completa
		self.avanzadaBoton = QtGui.QPushButton("Búsqueda Avanzada")
		self.avanzadaBoton.setFixedSize(120, 23)
		self.buscarBoton = QtGui.QPushButton("Buscar")
		self.buscarBoton.setFixedSize(120, 23)
		self.limpiarBoton = QtGui.QPushButton("Limpiar Búsqueda")
		self.limpiarBoton.setFixedSize(120, 23)
		avanzadaLayout = QtGui.QHBoxLayout()
		avanzadaLayout.addWidget(self.limpiarBoton)
		avanzadaLayout.addWidget(self.avanzadaBoton)
		avanzadaLayout.addWidget(self.buscarBoton)
		avanzadaLayout.setAlignment(QtCore.Qt.AlignRight)
		
		self.grupoCodAreaLayout = QtGui.QHBoxLayout()
		self.grupoCodAreaLayout.addWidget(self.codAreaOpcIgual)
		self.grupoCodAreaLayout.addWidget(self.codAreaOpcDistinto)
		self.grupoCodAreaLayout.addSpacing(20)
		self.grupoCodAreaLayout.addWidget(ceroLabel)		
		self.grupoCodAreaLayout.addWidget(self.codLinea)
		self.grupoCodAreaLayout.addWidget(buscarEnLabel)
		self.grupoCodAreaLayout.addWidget(self.codAreaOpc)
		self.grupoCodAreaLayout.addSpacing(600)
		
		#Layouts
		self.grupoBusqueda.setLayout(self.busquedaLayOut)
		self.grupoAvanzada.setLayout(self.grupoAvanzadaLayouts)
		self.grupoCodArea.setLayout(self.grupoCodAreaLayout)
		
		
		self.cerrarBoton = QtGui.QPushButton("Cerrar")
		cerrarLayout = QtGui.QHBoxLayout()
		cerrarLayout.addWidget(self.cerrarBoton)
		cerrarLayout.setAlignment(QtCore.Qt.AlignRight)
		
		
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(self.grupoBusqueda)
		mainLayout.addWidget(self.grupoCodArea)
		mainLayout.addWidget(self.grupoAvanzada)
		mainLayout.addLayout(avanzadaLayout)
		mainLayout.addLayout(cerrarLayout)
		self.setLayout(mainLayout)
		
		
		#Conexiones
		self.cerrarBoton.clicked.connect(self.accionCerrarBoton)
		self.avanzadaBoton.clicked.connect(self.accionAvanzadaBoton)
		self.buscarBoton.clicked.connect(self.accionBuscarBoton)

		self.exec_()
		
		
	def accionCerrarBoton(self):
		self.close()
		
	def accionAvanzadaBoton(self):
		if self.grupoAvanzada.isVisible():
			self.grupoAvanzada.setVisible(False)
		else:
			self.grupoAvanzada.setVisible(True)
		self.adjustSize()
		
	def obtenerOpcionesBusqueda(self):
		lista = []
				
		#Opciones basicas
		aux =str(self.nroOrigen.text())
		if aux != "":
			lista.append(("numeroOrigen", aux))
		aux = str(self.nroDestino.text())
		if aux != "":
			lista.append(("numeroDestino", aux))
		aux = str(self.fechaDesde.date().toString("dd.MM.yyyy"))
		aux = aux.split(".")
		aux.reverse()
		aux = aux[0] + aux[1] + aux[2]
		aux1 = str(self.fechaHasta.date().toString("dd.MM.yyyy"))
		aux1 = aux1.split(".")
		aux1.reverse()
		aux1 = aux1[0] + aux1[1] + aux1[2]
		lista.append(("fecha", aux, aux1))
		aux = str(self.horaDesde.time().toString())
		aux2 = str(self.horaHasta.time().toString())
		#Por la forma que se cargo en la base de datos
		if aux2 == "23:59:59":
			aux2 = "25:00:00"
		
		lista.append(("hora", aux, aux2))
	
		aux = unicode(self.antena.currentText(), "latin")
		if aux != "Todos":
			lista.append(("antenaDireccion", aux))
		
		aux = traducirDuracion(unicode(self.duracionDesde.currentText(), "latin"))
		aux1 = traducirDuracion(unicode(self.duracionHasta.currentText(), "latin"))
		
		lista.append(("duracion", aux, aux1))
		
		#Opciones de código de área
		aux = str(self.codLinea.text())
		if aux != "":
			if self.codAreaOpcDistinto.isChecked():
				lista.append(("codigoArea","distinto",self.codAreaOpc.currentIndex(), aux))
			else:
				lista.append(("codigoArea","igual",self.codAreaOpc.currentIndex(), aux))
		
		#Opciones Avanzadas
		aux = str(self.nroImei.text())
		if aux != "":
			lista.append(("numeroImei", aux))
		aux = str(self.nroSim.text())
		if aux != "":
			lista.append(("numeroSim", aux))
		aux = unicode(self.idCelda.currentText(), "utf-8")
		if aux != "Todos":
			lista.append(("celda", aux))
		aux = str(self.tipoMsj.currentText())
		# Aqui solo tenemos la opcion sms/mms y ninguno
		if aux != "Ambos":
			lista.append(("tipoComunicacion", aux))
		aux = str(self.provAntena.currentText())
		if aux != "Todos":
			lista.append(("antenaProvincia", aux))
		aux = str(self.locAntena.currentText())
		if aux != "Todos":
			lista.append(("antenaLocalidad", aux))
		aux = str(self.dirOrigen.text())
		if aux != "":
			lista.append(("direccionOrigen", aux))
		aux = str(self.dirDestino.text())
		if aux != "":
			lista.append(("direccionDestino", aux))
		aux = str(self.locOrigen.text())
		if aux != "":
			lista.append(("localidadOrigen", aux))
		aux = str(self.locDestino.text())
		if aux != "":
			lista.append(("localidadDestino", aux))
		aux = str(self.provOrigen.text())
		if aux != "":
			lista.append(("provinciaOrigen", aux))
		aux = str(self.provDestino.text())
		if aux != "":
			lista.append(("provinciaDestino", aux))
		aux = str(self.titularOrigen.text())
		if aux != "":
			lista.append(("tirularOrigen", aux))
		aux = str(self.titularDestino.text())
		if aux != "":
			lista.append(("titularDestino", aux))
		aux = str(self.empOrigen.text())
		if aux != "":
			lista.append(("empresaOrigen", aux))
		aux = str(self.empDestino.text())
		if aux != "":
			lista.append(("empresaDestino", aux))
		aux = str(self.contMsj.text())
		if aux != "":
			lista.append(("contenidoMensaje", aux))
		aux = str(self.estadoMsj.currentText())
		if aux != "Todos":
			lista.append(("estado", aux))
				
		return lista
		
	def accionBuscarBoton(self):
		self.listaBusqueda = self.obtenerOpcionesBusqueda()
		self.close()

		
class CodigoAreaDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		super(CodigoAreaDialog, self).__init__(parent)
		
		self.setWindowTitle("Códigos de Área")
		
		self.buscarBoton = QtGui.QPushButton("Buscar")
		self.cancelarBoton = QtGui.QPushButton("Cancelar")
		label1 = QtGui.QLabel("Ingrese el código de área a buscar:")
		self.codLine = QtGui.QLineEdit()
		self.codLine.setFixedSize(170, 25)
		self.lista = QtGui.QTextEdit()
		self.lista.setFixedSize(170, 100)
		self.lista.setVisible(False)
		
		buscarLayout = QtGui.QHBoxLayout()
		buscarLayout.addWidget(self.buscarBoton)
		buscarLayout.addWidget(self.cancelarBoton)
		buscarLayout.setAlignment(QtCore.Qt.AlignRight)
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(label1)
		mainLayout.addWidget(self.codLine)
		mainLayout.addWidget(self.lista)
		mainLayout.addLayout(buscarLayout)
		
		self.setLayout(mainLayout)
		
		self.buscarBoton.clicked.connect(self.buscarAccion)
		self.cancelarBoton.clicked.connect(self.cancelarAccion)
		self.exec_()
		
	def buscarAccion(self):
		codigo = str(self.codLine.text())
		listado = dicCodigosArea(codigo)
		texto = ""
		if listado:
			for item in listado:
				texto = texto + item + "\n"
		else:
			texto = "Característica inexistente"
		self.lista.setText(texto)
		self.lista.setVisible(True)
		self.lista.setReadOnly(True)
		
	def cancelarAccion(self):
		self.close()

class AliasDialog(QtGui.QDialog):
	def __init__(self, listaAlias, parent=None):
		super(AliasDialog, self).__init__(parent)
		
		self.setWindowTitle("Asignar/Eliminar Alias")
		self.asignarOpcion = QtGui.QRadioButton("Asignar Alias")
		self.asignarOpcion.setChecked(True)
		self.eliminarOpcion = QtGui.QRadioButton("Eliminar Alias")
		grupoOpciones = QtGui.QGroupBox("Opciones")
		
		self.texto = ("","")
		label = QtGui.QLabel("Ingrese el Alias: ")
		label2 = QtGui.QLabel("Elija cual Eliminar: ")
		self.alias = QtGui.QLineEdit()
		self.okBoton = QtGui.QPushButton("Ok")
		self.cancelarBoton = QtGui.QPushButton("Cancelar")
		self.asignados = QtGui.QComboBox()
		if listaAlias:
			self.asignados.addItems(["Todos"] + listaAlias)
			self.asignados.setEnabled(False)
		else:
			self.eliminarOpcion.setEnabled(False)
			self.asignados.setEnabled(False)
		grupoOpcionesLayot = QtGui.QGridLayout()
		grupoOpcionesLayot.addWidget(self.asignarOpcion, 0, 0)
		grupoOpcionesLayot.addWidget(self.eliminarOpcion, 0, 1)
		grupoOpcionesLayot.addWidget(label, 1, 0)
		grupoOpcionesLayot.addWidget(self.alias, 1, 1)
		grupoOpcionesLayot.addWidget(label2, 2, 0)
		grupoOpcionesLayot.addWidget(self.asignados, 2, 1)
		grupoOpcionesLayot.addWidget(self.okBoton, 3, 0)
		grupoOpcionesLayot.addWidget(self.cancelarBoton, 3, 1)
		
		
		grupoOpciones.setLayout(grupoOpcionesLayot)
		self.setLayout(grupoOpcionesLayot)
		
		self.asignarOpcion.clicked.connect(self.asignarAccion)
		self.eliminarOpcion.clicked.connect(self.eliminarAccion)
		self.okBoton.clicked.connect(self.okAccion)
		self.cancelarBoton.clicked.connect(self.cancelarAccion)
		self.exec_()
		
	def asignarAccion(self):
		self.asignados.setEnabled(False)
		self.alias.setEnabled(True)
		
	def eliminarAccion(self):
		self.asignados.setEnabled(True)
		self.alias.setEnabled(False)
		
	def okAccion(self):
		if self.asignarOpcion.isChecked():
			self.texto = (str(self.alias.text()), True)
		else:
			self.texto = (str(self.asignados.currentText()), False)
		self.close()
	
	def cancelarAccion(self):
		self.texto = ("", "")
		self.close()		