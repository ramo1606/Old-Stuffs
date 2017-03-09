#!/usr/bin/env python
# *-* coding: utf-8 *-*

from PyQt4 import QtCore, QtGui, QtWebKit
from xlwt import *
from datetime import *

from Fuentes.Parsers.Parser import Parser
from Fuentes.Parsers.Diccionario import Diccionario
from Fuentes.Hilo.Hilo import Hilo
from Fuentes.Parsers.Sabana import Sabana
from Fuentes.Parsers.CjtoSabana import ConjuntoSabanas
from Fuentes.Funcionalidad.Pagina1 import *
from Fuentes.Funcionalidad.Pagina2 import *
from Fuentes.Funcionalidad.Pagina3 import *
from Fuentes.Parsers.DBmanager import *

from Fuentes.Funcionalidad.dialogos import *

import sys
from threading import Condition	

		
class VentanaPpal(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(VentanaPpal, self).__init__(parent)
		
		self.setGeometry(100, 100, 1024, 600)
		self.setWindowTitle("Astrea 1.0")	
		
		

		# Crear los menues
		self.statusBar()
		self.crearAcciones()
		self.crearMenues()
				
		#Atributos de la Ventana Principal
		self.closeButton = QtGui.QPushButton("Cerrar")
		self.closeButton.setFixedSize(120, 23)
		
		self.volverInicioBoton = QtGui.QPushButton("Volver al Inicio")
		self.volverInicioBoton.setFixedSize(120, 23)
				
		# Atributos para el manejo del Hilo
		self.hilo = []
		self.condicion = Condition()
		self.listaHilo = []
		
		# Atributos manejo de sabanas
		self.cjtoSabanas = []
		self.nuevoSinonimo = False
		
		# Atributos Comunicacion Pantallas
		self.nuevaBusquedaFlag = True
		self.ampliarBusquedaFlag = False
		
		# Elementos para la base de datos
		self.db = dbManager("sabanas")
		
		# Conexiones Main Windows
		self.closeButton.clicked.connect(self.close_)
		self.volverInicioBoton.clicked.connect(self.accionVolverInicioBoton)
		
		
		self.crearPagina1()


	
	def crearPagina1(self):
		# INICIO PRIMERA PANTALLA	
		# Acciones Disponibles
		self.accionAbrir.setEnabled(True)
		self.accionGuardar.setEnabled(False)
		self.accionImprimir.setEnabled(False)
		
		
		# Contenedor donde van las cosas
		self.contenedorPagina1 = QtGui.QWidget()
		self.setCentralWidget(self.contenedorPagina1)
	
		
		# Atributos para la carga de archivos
		self.grupoArchivo = QtGui.QGroupBox("Carga de Archivos")
		
		self.cargarArchivoBoton = QtGui.QPushButton("Cargar Archivo...")
		self.cargarArchivoBoton.setFixedSize(120, 30)
		self.cargarArchivoBoton.setToolTip("Agregar un nuevo archivo")
		self.eliminarArchivoBoton = QtGui.QPushButton("Eliminar")
		self.eliminarArchivoBoton.setFixedSize(120, 30)
		self.eliminarArchivoBoton.setToolTip("Eliminar archivo de la lista")
		self.finalizarBoton = QtGui.QPushButton("Finalizar Carga")
		self.finalizarBoton.setFixedSize(120, 30)
		self.verificarBoton = QtGui.QPushButton("Verificar Archivos")
		self.verificarBoton.setFixedSize(120, 30)
		self.verificarBoton.setToolTip("Verifica que no exista ambiguedad de datos en las sabanas cargadas")
		
		self.finalizarBoton.setToolTip("Finaliza la carga de archivos")
		self.eliminarArchivoBoton.setEnabled(False)
		self.finalizarBoton.setEnabled(False)
		self.verificarBoton.setEnabled(False)
		
		
		
		self.grillaArchivos = QtGui.QTableWidget(0,5)
		self.grillaArchivos.setToolTip("Lista de archivos cargados")
		self.grillaArchivos.setHorizontalHeaderLabels(["Archivo", "Ubicación", "Empresa", "Control", "Error"])
		self.grillaArchivos.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.grillaArchivos.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.grillaArchivos.setSortingEnabled(True)
		
		# Sector de unificacion de columnas
		self.grupoColumnas = QtGui.QGroupBox("Unificación de Columnas")
		self.grupoColumnas.setEnabled(False)
		self.grupoColumnas.setVisible(False)
				
		self.archivoLabel = QtGui.QLabel()
		self.sinonimoLinea = QtGui.QLineEdit()
		self.sinonimoLinea.setReadOnly(True)
		self.sinonimoLinea.setToolTip("Nombre de la columna del archivo")
		self.sinonimoLabel = QtGui.QLabel("es lo mismo que:")
		self.conceptosLista = QtGui.QComboBox()
		self.conceptosLista.setToolTip("Significado del sinonimo")
		self.conceptosLista.setSizeAdjustPolicy(self.conceptosLista.AdjustToContents)
		self.okBoton = QtGui.QPushButton("Ok")
						
		# Layouts
		botonLayout = QtGui.QHBoxLayout()
		botonLayout.addWidget(self.eliminarArchivoBoton)
		botonLayout.addWidget(self.finalizarBoton)
		botonLayout.setAlignment(QtCore.Qt.AlignRight)
		
		botonVerificarLayout = QtGui.QHBoxLayout()
		botonVerificarLayout.addWidget(self.verificarBoton)
		botonVerificarLayout.setAlignment(QtCore.Qt.AlignLeft)
		
		botonesLayout = QtGui.QHBoxLayout()
		botonesLayout.addLayout(botonVerificarLayout)
		botonesLayout.addLayout(botonLayout)
		
		archivoLayout = QtGui.QVBoxLayout()
		archivoLayout.addWidget(self.cargarArchivoBoton)
		archivoLayout.addWidget(self.grillaArchivos)
		archivoLayout.addLayout(botonesLayout)

		columnasLayout = QtGui.QGridLayout()
		columnasLayout.addWidget(self.archivoLabel, 0, 0)
		columnasLayout.addWidget(self.sinonimoLinea, 1, 0)
		columnasLayout.addWidget(self.sinonimoLabel, 1, 1)
		columnasLayout.addWidget(self.conceptosLista, 1, 2)
		columnasLayout.addWidget(self.okBoton, 2, 1)
		
		
		paginaLayout = QtGui.QVBoxLayout()
		paginaLayout.addLayout(archivoLayout)
		
		pagLayout = QtGui.QVBoxLayout()
		pagLayout.addLayout(columnasLayout)
		
		self.grupoArchivo.setLayout(paginaLayout)
		
		self.grupoColumnas.setLayout(pagLayout)
		
		
		botonCerrarLayout = QtGui.QHBoxLayout()
		botonCerrarLayout.addWidget(self.volverInicioBoton)
		botonCerrarLayout.addWidget(self.closeButton)
		botonCerrarLayout.setAlignment(QtCore.Qt.AlignRight)
		self.volverInicioBoton.setVisible(False)
	
		mainLayout = QtGui.QVBoxLayout(self.contenedorPagina1)
		mainLayout.addWidget(self.grupoArchivo)
		mainLayout.addWidget(self.grupoColumnas)
		mainLayout.addLayout(botonCerrarLayout)
		mainLayout.addStretch(1)
		self.contenedorPagina1.setLayout(mainLayout)
			
		
		# Conexiones pagina 1
		self.cargarArchivoBoton.clicked.connect(self.abrirArchivo)
		self.eliminarArchivoBoton.clicked.connect(self.eliminarArchivo)
		self.finalizarBoton.clicked.connect(self.accionBotonFinalizar)
		self.verificarBoton.clicked.connect(self.accionVerificarBoton)
		self.okBoton.clicked.connect(self.accionOkBoton)
	
	
			
	def crearPagina2(self):
		# Acciones Disponibles
		self.accionAbrir.setEnabled(False)
		self.accionGuardar.setEnabled(False)
		self.accionImprimir.setEnabled(False)
		self.volverInicioBoton.setVisible(True)
		
		if self.nuevaBusquedaFlag:
			self.contenedorPagina2 = QtGui.QWidget()
			self.setCentralWidget(self.contenedorPagina2)
				
		# Atributos de la Busqueda
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
		
		
		#Atributos de Opciones de Salida
		self.grupoSalida = QtGui.QGroupBox("Opciones De Salida")
		self.todoCheck = QtGui.QCheckBox("Seleccionar Todo")
		
		
		self.nroOrigenCheck = QtGui.QCheckBox("Nro. de Origen")
		self.nroOrigenCheck.setChecked(True)
		self.nroDestinoCheck = QtGui.QCheckBox("Nro. de Destino")
		self.nroDestinoCheck.setChecked(True)
		self.fechaInicioCheck = QtGui.QCheckBox("Fecha")
		self.fechaInicioCheck.setChecked(True)
		self.horaInicioCheck = QtGui.QCheckBox("Hora")
		self.horaInicioCheck.setChecked(True)
		self.duracionCheck = QtGui.QCheckBox("Duración de LLamada")
		self.nroImeiCheck = QtGui.QCheckBox("Nro. de Imei")
		self.nroSimCheck = QtGui.QCheckBox("Nro. de Sim")
		self.celdaIdCheck = QtGui.QCheckBox("Id. de Celda")
		self.dirOrigenCheck = QtGui.QCheckBox("Dirección Nro. de Origen")
		self.dirDestinoCheck = QtGui.QCheckBox("Dirección Nro. Destino")
		self.locOrigenCheck = QtGui.QCheckBox("Localidad Nro. Origen")
		self.locDestinoCheck = QtGui.QCheckBox("Localidad Nro. Destino")
		self.msjCheck = QtGui.QCheckBox("Tipo de Comunicación")
		self.estadoCheck = QtGui.QCheckBox("Estado")
		self.dirAntenaCheck = QtGui.QCheckBox("Dirección de Antena")
		self.dirAntenaCheck.setChecked(True)
		self.locAntenaCheck = QtGui.QCheckBox("Localidad de Antena")
		self.provAntenaCheck = QtGui.QCheckBox("Provincia de Antena")
		self.titOrigenCheck = QtGui.QCheckBox("Titular Nro. Origen")
		self.titDestinoCheck = QtGui.QCheckBox("Titular Nro. Destino")
		self.empOrigenCheck = QtGui.QCheckBox("Empresa Nro. Origen")
		self.empDestinoCheck = QtGui.QCheckBox("Empresa Nro. Destino")
		self.provOrigenCheck = QtGui.QCheckBox("Provincia Nro. Origen")
		self.provDestinoCheck = QtGui.QCheckBox("Provincia Nro. Destino")
		self.contMensajeCheck = QtGui.QCheckBox("Contenido de Mensaje")
		
		
		
		
		self.opcionesSalidaLayOut = QtGui.QGridLayout()
		self.opcionesSalidaLayOut.addWidget(self.todoCheck, 0, 0)
		self.opcionesSalidaLayOut.addWidget(self.nroOrigenCheck, 1, 0)
		self.opcionesSalidaLayOut.addWidget(self.nroDestinoCheck, 1, 1)
		self.opcionesSalidaLayOut.addWidget(self.fechaInicioCheck, 1, 2)
		self.opcionesSalidaLayOut.addWidget(self.horaInicioCheck, 1, 3)
		self.opcionesSalidaLayOut.addWidget(self.dirAntenaCheck, 1, 4)
		self.opcionesSalidaLayOut.addWidget(self.locAntenaCheck, 2, 0)
		self.opcionesSalidaLayOut.addWidget(self.provAntenaCheck, 2, 1)
		self.opcionesSalidaLayOut.addWidget(self.celdaIdCheck, 2, 2)
		self.opcionesSalidaLayOut.addWidget(self.dirOrigenCheck, 2, 3)
		self.opcionesSalidaLayOut.addWidget(self.dirDestinoCheck, 2, 4)
		self.opcionesSalidaLayOut.addWidget(self.locOrigenCheck, 3, 0)
		self.opcionesSalidaLayOut.addWidget(self.locDestinoCheck, 3, 1)
		self.opcionesSalidaLayOut.addWidget(self.provOrigenCheck, 3, 2)
		self.opcionesSalidaLayOut.addWidget(self.empOrigenCheck, 3, 3)
		self.opcionesSalidaLayOut.addWidget(self.empDestinoCheck, 3, 4)
		self.opcionesSalidaLayOut.addWidget(self.contMensajeCheck, 5, 1)
		self.opcionesSalidaLayOut.addWidget(self.msjCheck, 5, 2)
		
		
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
		self.grupoSalida.setLayout(self.opcionesSalidaLayOut)
		self.grupoAvanzada.setLayout(self.grupoAvanzadaLayouts)
		self.grupoCodArea.setLayout(self.grupoCodAreaLayout)

		botonCerrarLayout = QtGui.QHBoxLayout()
		botonCerrarLayout.addWidget(self.volverInicioBoton)
		botonCerrarLayout.addWidget(self.closeButton)
		botonCerrarLayout.setAlignment(QtCore.Qt.AlignRight)
		
		if self.nuevaBusquedaFlag:
			mainLayout = QtGui.QVBoxLayout()
			mainLayout.addWidget(self.grupoBusqueda)
			mainLayout.addWidget(self.grupoCodArea)
			mainLayout.addWidget(self.grupoAvanzada)
			mainLayout.addWidget(self.grupoSalida)
			mainLayout.addLayout(avanzadaLayout)
			mainLayout.addLayout(botonCerrarLayout)
			mainLayout.addStretch(1)
			self.contenedorPagina2.setLayout(mainLayout)
		else:
			self.grupoAmpliarBusqueda = QtGui.QGroupBox("Ampliar Búsqueda")
			ampliarBusquedaLayout = QtGui.QVBoxLayout()
			ampliarBusquedaLayout.addWidget(self.grupoBusqueda)
			ampliarBusquedaLayout.addWidget(self.grupoCodArea)
			ampliarBusquedaLayout.addWidget(self.grupoAvanzada)
			ampliarBusquedaLayout.addLayout(avanzadaLayout)
			self.grupoAmpliarBusqueda.setLayout(ampliarBusquedaLayout)
			self.grupoAmpliarBusqueda.setWindowTitle("Ampliar Búsqueda")
			self.grupoAmpliarBusqueda.setVisible(False)
			
			
		
		# Conexiones
		self.todoCheck.stateChanged.connect(self.accionTodoCheck)
		self.buscarBoton.clicked.connect(self.accionBuscarBoton)
		self.avanzadaBoton.clicked.connect(self.accionAvanzadaBoton)
		self.limpiarBoton.clicked.connect(self.accionLimpiarBoton)
	
		
		self.opcionesSalidaLayOut.addWidget(self.provDestinoCheck, 4, 0)
		self.opcionesSalidaLayOut.addWidget(self.duracionCheck, 4, 1)
		self.opcionesSalidaLayOut.addWidget(self.nroImeiCheck, 4, 2)
		self.opcionesSalidaLayOut.addWidget(self.nroSimCheck, 4, 3)
		self.opcionesSalidaLayOut.addWidget(self.titOrigenCheck, 4, 4)
		self.opcionesSalidaLayOut.addWidget(self.titDestinoCheck, 5, 0)
	
	
	def crearPagina3(self, listaSalida, listaBusqueda):
		
		# Acciones Disponibles
		self.accionAbrir.setEnabled(False)
		self.accionGuardar.setEnabled(True)
		self.accionImprimir.setEnabled(True)
		
		self.contenedorPagina3 = QtGui.QWidget()
		self.setCentralWidget(self.contenedorPagina3)
		
		self.listaAlias = []
		self.cantidadRefinamientos = 0
		
		
		# Opciones de resultados:
		self.grupoResultados = QtGui.QGroupBox("Opciones de Búsqueda")
		self.infoLabel = QtGui.QLabel("Haciendo click en la celda deseada, de despliega el menú de opciones")
		self.grillaResultados = QtGui.QTableWidget()
		self.grillaResultados.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.grillaResultados.setSortingEnabled(True)
		
		self.refinarBoton = QtGui.QPushButton("Refinar Búsqueda")
		self.refinarBoton.setFixedSize(120, 23)
		
		
		
		self.imprimirBoton = QtGui.QPushButton("Imprimir...")
		self.imprimirBoton.setFixedSize(120, 23)
		self.guardarBoton = QtGui.QPushButton("Guardar...")
		self.nuevaBusquedaBoton = QtGui.QPushButton("Nueva Búsqueda")
		self.ampliarBusquedaBoton = QtGui.QPushButton("Ampliar Búsqueda...")
		
		
		
		#Grupos de Opciones Segun Elemento
		
		self.grupoNumeroTelefono = QtGui.QGroupBox("Opciones Disponibles")
		self.grupoUbicacionMapa = QtGui.QGroupBox("Opciones Disponibles")
		self.grupoTitular = QtGui.QGroupBox("Opciones Disponibles")
		self.grupoImei = QtGui.QGroupBox("Opciones Disponibles")
		
		
		
		self.aliasBoton = QtGui.QPushButton("Alias")
		self.aliasBoton.setFixedSize(120, 23)
		self.intervencionBoton = QtGui.QPushButton("Pedir Intervención")
		self.intervencionBoton.setFixedSize(120, 23)
		self.arrestoBoton = QtGui.QPushButton("Pedir Arresto")
		self.arrestoBoton.setFixedSize(120, 23)
		self.codAreaBoton = QtGui.QPushButton("Código de Área")
		self.codAreaBoton.setFixedSize(120, 23)
		self.imeiBoton = QtGui.QPushButton("Fabricante Imei")
		self.imeiBoton.setFixedSize(120, 23)
		self.ubicacionBoton = QtGui.QPushButton("Ver en Mapa")
		self.ubicacionBoton.setFixedSize(120, 23)
		
		
		numerosTelefonos = QtGui.QHBoxLayout()
		numerosTelefonos.addWidget(self.aliasBoton)
		numerosTelefonos.addWidget(self.intervencionBoton)
		numerosTelefonos.addWidget(self.codAreaBoton)
		
		ubicacionLayout = QtGui.QHBoxLayout()
		ubicacionLayout.addWidget(self.ubicacionBoton)
		
		imeiLayout = QtGui.QHBoxLayout()
		imeiLayout.addWidget(self.imeiBoton)
		
		titularLayout = QtGui.QHBoxLayout()
		titularLayout.addWidget(self.arrestoBoton)
		
		
		self.grupoImei.setLayout(imeiLayout)
		self.grupoNumeroTelefono.setLayout(numerosTelefonos)
		self.grupoTitular.setLayout(titularLayout)
		self.grupoUbicacionMapa.setLayout(ubicacionLayout)
		
		
		self.grupoImei.setVisible(False)
		self.grupoNumeroTelefono.setVisible(False)
		self.grupoTitular.setVisible(False)
		self.grupoUbicacionMapa.setVisible(False)
		
		# Layouts
		self.resultadosLayouts = QtGui.QVBoxLayout()
		self.grupoResultados.setLayout(self.resultadosLayouts)
		botonesDerechaLayout = QtGui.QHBoxLayout()
		botonesDerechaLayout.addWidget(self.guardarBoton)
		botonesDerechaLayout.addWidget(self.ampliarBusquedaBoton)
		botonesDerechaLayout.addWidget(self.nuevaBusquedaBoton)
		botonesDerechaLayout.setAlignment(QtCore.Qt.AlignRight)
		
		botonesResultadoLayout = QtGui.QHBoxLayout()
		botonesResultadoLayout.addWidget(self.imprimirBoton)
		botonesResultadoLayout.addLayout(botonesDerechaLayout)
		
		botonRefinarLayout = QtGui.QHBoxLayout()
		botonRefinarLayout.addWidget(self.refinarBoton)
		botonRefinarLayout.setAlignment(QtCore.Qt.AlignRight)
		
		labelLayout = QtGui.QHBoxLayout()
		labelLayout.addWidget(self.infoLabel)
		labelLayout.setAlignment(QtCore.Qt.AlignCenter)
		
		self.resultadosLayouts.addLayout(labelLayout)
		self.resultadosLayouts.addWidget(self.grillaResultados)
		self.resultadosLayouts.addLayout(botonRefinarLayout)
		self.resultadosLayouts.addLayout(botonesResultadoLayout)
		
		botonCerrarLayout = QtGui.QHBoxLayout()
		botonCerrarLayout.addWidget(self.volverInicioBoton)
		botonCerrarLayout.addWidget(self.closeButton)
		botonCerrarLayout.setAlignment(QtCore.Qt.AlignRight)
		
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(self.grupoResultados)
		mainLayout.addWidget(self.grupoImei)
		mainLayout.addWidget(self.grupoNumeroTelefono)
		mainLayout.addWidget(self.grupoTitular)
		mainLayout.addWidget(self.grupoUbicacionMapa)
		mainLayout.addLayout(botonCerrarLayout)
		mainLayout.addStretch(1)
		
		
		self.contenedorPagina3.setLayout(mainLayout)
		
		query = self.db.busqueda(listaBusqueda, listaSalida)
		self.llenarGrillaResultados(listaSalida, query)
		
		
		
		#Conexiones
		
		self.imprimirBoton.clicked.connect(self.vistaPreviaBoton)
		self.guardarBoton.clicked.connect(self.guardarResultadosBoton)
		self.ampliarBusquedaBoton.clicked.connect(self.accionAmpliarBusqueda)
		self.nuevaBusquedaBoton.clicked.connect(self.accionNuevaBusquedaBoton)
		self.connect(self.grillaResultados, QtCore.SIGNAL("cellActivated(int, int)"), self.celdaClick)
		self.grillaResultados.cellPressed.connect(self.celdaClick)	
		self.aliasBoton.clicked.connect(self.accionAliasBoton)
		self.codAreaBoton.clicked.connect(self.accionCodigosDeAreaBoton)
		self.refinarBoton.clicked.connect(self.accionRefinarBoton)
		self.ubicacionBoton.clicked.connect(self.accionUbicacionBoton)
		
	
	def accionVolverInicioBoton(self):
		self.db.eliminarDB()
		self.hilo = []
		self.condicion = Condition()
		self.listaHilo = []
		
		# Atributos manejo de sabanas
		self.cjtoSabanas = []
		self.nuevoSinonimo = False
		
		# Atributos Comunicacion Pantallas
		self.nuevaBusquedaFlag = True
		
		# Elementos para la base de datos
		self.db = dbManager("sabanas")
		
		self.crearPagina1()
	
	def closeEvent(self, event):
		self.db.eliminarDB()
		event.accept()
	
	def close_(self):
		# cerrar conexion con la base de datos
		# eliminar todo tipo de archivo temporal que se haya creado
		self.db.eliminarDB()
		self.close()
	
	def crearAcciones(self):
		self.accionAbrir = QtGui.QAction("&Abrir...", self,
				shortcut=QtGui.QKeySequence.New,
				statusTip="Agregar archivo a la lista", triggered=self.abrirArchivo)
		self.accionAbrir.setEnabled(False)

		self.accionImprimir = QtGui.QAction("&Imprimir", self,
				shortcut=QtGui.QKeySequence.Print,
				statusTip="Imprimir los resultados", triggered=self.vistaPreviaBoton)
		self.accionImprimir.setEnabled(False)
		

		self.accionGuardar = QtGui.QAction("&Guardar...", self,
				shortcut=QtGui.QKeySequence.Save,
				statusTip="Guardar resultados", triggered=self.guardarResultadosBoton)
		self.accionGuardar.setEnabled(False)		
		
		# TODO
		self.accionCodigosDeArea = QtGui.QAction("&Códigos de Área", self,
				statusTip="Información de los códigos de áreas", triggered=self.accionCodigosDeAreaBoton)		
		self.accionCodigosDeArea.setEnabled(True)
		
		self.accionAsignarAlias = QtGui.QAction("&Asignar Alias", self,
				statusTip="Asignar Alias a un número de teléfono", triggered=self.accionAliasBoton)		
		self.accionAsignarAlias.setEnabled(False)
		
		self.accionPedirIntervencion = QtGui.QAction("&Pedir Intervención", self,
				statusTip="Pedir Intervención del número de teléfono", triggered=self.accionPedirIntervencionBoton)		
		self.accionPedirIntervencion.setEnabled(False)
		
		self.accionPedirArresto = QtGui.QAction("&Pedir Arresto", self,
				statusTip="Pedir Arresto para el titular", triggered=self.accionPedirArrestoBoton)		
		self.accionPedirArresto.setEnabled(False)
		
		self.accionVerMapa = QtGui.QAction("&Ver en Mapa", self,
				statusTip="Ver en Mapa la ubicación requerida", triggered=self.accionUbicacionBoton)		
		self.accionVerMapa.setEnabled(False)
		
		

		self.accionAbrirManualDeUsuario = QtGui.QAction("&Manual de Usuario...", self,
				statusTip="Visualizar el manual de usuario", triggered=self.accionAbrirManualDeUsuario)		
		
		self.accionAcercaDe = QtGui.QAction("&Acerca De Astrea", self,
				statusTip="Información de Astrea", triggered=self.accionAcercaDe)		
		
		
		
	def crearMenues(self):
		# Menu Archivo
		self.menuArchivo = self.menuBar().addMenu("&Archivo")
		self.menuArchivo.addAction(self.accionAbrir)
		self.menuArchivo.addAction(self.accionGuardar)
		self.menuArchivo.addAction(self.accionImprimir)
		
				
		# Menu Opciones
		self.opcionesMenu = self.menuBar().addMenu("&Opciones")
		self.opcionesMenu.addAction(self.accionAsignarAlias)
		self.opcionesMenu.addAction(self.accionPedirIntervencion)
		self.opcionesMenu.addAction(self.accionPedirArresto)
		self.opcionesMenu.addAction(self.accionVerMapa)
		
		
		# Menu Herramientas
		self.herramientasMenu = self.menuBar().addMenu("&Herramientas")
		self.herramientasMenu.addAction(self.accionCodigosDeArea)
		
		
		# Menu Herramientas
		self.ayudaMenu = self.menuBar().addMenu("&Ayuda")
		self.ayudaMenu.addAction(self.accionAbrirManualDeUsuario)
		self.ayudaMenu.addAction(self.accionAcercaDe)
		
	
	
	def accionAbrirManualDeUsuario(self):
		os.system("Fuentes\Manuales\manual.pdf")
	
	def	accionAcercaDe(self):
		# QMessageBox.about (QWidget parent, QString caption, QString text)
		QtGui.QMessageBox.about(self, 'Acerca De...',
			'''<html>
				<head>
					<title>HTML Online Editor Sample</title>
				</head>
				<body>
					<h1>
						Informaci&oacute;n</h1>
					<p>
						Astrea fu&eacute; desarrollado como tesis de grado en la carrera de Lic. en Cs. de la Computaci&oacute;n - FaMAF - Universidad Nacional de C&oacute;rdoba - Argentina.</p>
					<p>
						Version 1.0</p>
					<p>
						Software de distribuci&oacute;n gratutita.</p>
					<p>
						Desarrollado por:</p>
					<ul>
						<li>
							Alurralde, Ramiro (<a href="mailto:ramo160689@gmail.com">ramo160689@gmail.com</a>)</li>
						<li>
							Bigatti, Juli&aacute;n (<a href="mailto:jbigatti@gmail.com">jbigatti@gmail.com</a>)</li>
					</ul>
					<p>
						Agradecimientos:</p>
					<ul>
						<li>
							Docente a cargo: Alonso Alemany, Laura (<a href="mailto:ramo160689@gmail.com">mail?</a>)</li>
						<li>
							Detective: Ledesma, Daniel (<a href="mailto:jbigatti@gmail.com">mails?</a>)</li>
						<li>
							Detective: Santiago, blabla (mail??)</li>
					</ul>
				</body>
				</html>''')
	
	#INICIO PRIMERA PANTALLA
	def abrirArchivo(self):
		archivo = QtGui.QFileDialog.getOpenFileName(self,
			"Buscar Archivo...",
			"",
			"All Files (*);;Excel Files (*.xls);;Coma Separated Value (*.csv);;Text Files (*.txt)")
		if archivo:
			lista = archivo.split("/")
			item = lista.last()
			if not self.archivoDuplicado(archivo, item):
				self.eliminarArchivoBoton.setEnabled(True)
				self.finalizarBoton.setEnabled(True)
				archivoNombre = QtGui.QLabel(QtCore.QString(item))
				archivoUbicacion = QtGui.QLabel(archivo)
				listadoEmpresas = QtGui.QComboBox()
				listadoEmpresas.addItems(["Claro", "Personal", "Movistar", "Nextel", "Resultado Anterior"]) 
				check = QtGui.QCheckBox()
				check.setEnabled(False)
				# Primer Archivo Ingresado
				if self.grillaArchivos.rowCount() == 0:
					self.grillaArchivos.insertRow(0)
				else:
					self.grillaArchivos.insertRow(self.grillaArchivos.rowCount())
				
				col = self.grillaArchivos.rowCount()-1
				self.grillaArchivos.setCellWidget(col,0, archivoNombre)
				self.grillaArchivos.setCellWidget(col,1, archivoUbicacion)
				self.grillaArchivos.setCellWidget(col,2, listadoEmpresas)
				self.grillaArchivos.setCellWidget(col,3, check)
				self.grillaArchivos.setCellWidget(col,4, QtGui.QLabel(QtCore.QString()))
				self.grillaArchivos.cellWidget(col,4).setEnabled(False)
				
				self.grillaArchivos.resizeColumnsToContents()	
			else:
				aviso = QtGui.QMessageBox.information(self,
				"Cuidado", "No es posible ingresar más de una vez el mismo archivo.")
				#Cuidado al agregar codigo proque cuando sale de la info termina la funcion
				
				
				
	def archivoDuplicado(self, ubic, nom):
	# Verificamos por ubicacion y nombre de archivo
		i = 0
		resultado = False
		
		if self.grillaArchivos.rowCount() != 0:
			while i < self.grillaArchivos.rowCount() and not resultado:
				ubicacion = self.grillaArchivos.cellWidget(i, 1)
				nombre = self.grillaArchivos.cellWidget(i, 0)
				if nombre.text() == nom:
					if ubicacion.text() == ubic:
						resultado = True
				i = i + 1
		return resultado
		
	def eliminarArchivo(self):
		fila = self.grillaArchivos.currentRow()
		if fila == -1:
			aviso = QtGui.QMessageBox.information(self,
			"Cuidado", "Antes debe seleccionar una fila.")
		else:
			indice = 0
			flag = False
			if self.cjtoSabanas:
				nombre = self.grillaArchivos.cellWidget(fila,1).text()
				self.cjtoSabanas.sacarSabanaN(self.cjtoSabanas.buscarSabana(nombre))

			self.grillaArchivos.removeRow(fila)
			if self.grillaArchivos.rowCount() == 0:
				self.eliminarArchivoBoton.setEnabled(False)
				self.finalizarBoton.setEnabled(False)
				self.verificarBoton.setEnabled(False)
				self.grupoColumnas.setEnabled(False)
		
	
	
	def crearCjtoSabanas(self):
		cjtoSabanas = ConjuntoSabanas()
		indice = 0
		while indice < self.grillaArchivos.rowCount():
			sabana = Sabana(self.grillaArchivos.cellWidget(indice,1).text(),
			self.grillaArchivos.cellWidget(indice,2).currentText(),
			self.grillaArchivos.cellWidget(indice,3).isChecked())
			indice = indice + 1
			cjtoSabanas.insertarSabana(sabana)
		return cjtoSabanas	
	
	def indiceGrilla(self, nombreArchivo):
		indice = 0
		while indice < self.grillaArchivos.rowCount():
			if self.grillaArchivos.cellWidget(indice,1).text() == nombreArchivo:
				return indice
			indice += 1
		
		print "la cagamos no encuentra el archivo en la lista"
		return -1

		
	def accionVerificarBoton(self):
		# Solo puede apretar una vez el boton
		
		# Preparo interfaz de Usuario
		self.grupoArchivo.setEnabled(False)
		self.grupoColumnas.setVisible(True)
		self.grupoColumnas.setEnabled(True)
		
		indice = 0
		self.sabanaActual = []
		while indice < len(self.cjtoSabanas.listaSabanas):
			if (not self.cjtoSabanas.listaSabanas[indice].checked and
				self.cjtoSabanas.listaSabanas[indice].control == 2):
				self.sabanaActual = self.cjtoSabanas.listaSabanas[indice]
				break
			indice += 1
		
		if self.sabanaActual != []:
			self.listarDatosConflictivos()
		else:
			print "nunca deberiamos entrar aca"
			#TODO
			# aca terminamos de verificar, ver a quien llamar
		
		
	def listarDatosConflictivos(self):
			
		self.archivoLabel.setText(self.sabanaActual.nombreArchivo)
		self.listaAux = []
		indice = 0
		while indice < len(self.sabanaActual.listaTuplas):
			if (not self.sabanaActual.listaTuplas[indice][1] or 
				len(self.sabanaActual.listaTuplas[indice][1]) > 1):
				
				self.listaAux.append(self.sabanaActual.listaTuplas.pop(indice))
				indice = 0
			else:
				indice += 1		

		
		if self.listaAux:
			elemento = self.listaAux.pop()
			if len(elemento[1]) == 0:
				self.nuevoSinonimo = True
			elemento = (elemento[0], self.sabanaActual.conceptosDisponibles(elemento[1]))
			if self.hilo == []:
				self.listaHilo.append(elemento)
				self.hilo = Hilo(self.listaHilo, self.condicion, self.sinonimoLinea, self.conceptosLista)
				self.hilo.start()
				print "Inicio el Hilo"
			else:
				self.condicion.acquire()
				self.listaHilo.append(elemento)
				self.condicion.notify()
				self.condicion.release()
				
		
	def actualizarGrillaArchivos(self, sabana):
		
		indice = self.indiceGrilla(sabana.nombreArchivo)
		
		if not sabana.checked:
			if sabana.control == 1:
				self.grillaArchivos.cellWidget(indice, 4).setText("El archivo no corresponde con la empresa seleccionada")
				self.finalizarBoton.setEnabled(True)
			elif sabana.control == 2:
				self.verificarBoton.setEnabled(True)
				self.finalizarBoton.setEnabled(False)
				self.grillaArchivos.cellWidget(indice, 2).setEnabled(False)
				self.grillaArchivos.cellWidget(indice, 4).setText("Existen conflictos con las columnas de la sabana")
				self.verificarBoton.setEnabled(True)
			else:
				print "algo esta mal.......... muy mal, puto"
			
		else:
			self.grillaArchivos.cellWidget(indice, 2).setEnabled(False)
			self.grillaArchivos.cellWidget(indice, 3).setChecked(True)
			self.grillaArchivos.cellWidget(indice, 4).setVisible(False)
		self.grillaArchivos.resizeColumnsToContents()
		
	def actualizarCjtoSabanas(self):
		flag = False
		indice = 0
		while indice < len(self.cjtoSabanas.listaSabanas):
			if self.cjtoSabanas.listaSabanas[indice].control == 1:
				ubicacion = self.indiceGrilla(self.cjtoSabanas.listaSabanas[indice].nombreArchivo)
				self.cjtoSabanas.sacarSabanaN(indice)
				sabana = Sabana(self.grillaArchivos.cellWidget(ubicacion,1).text(),
				self.grillaArchivos.cellWidget(ubicacion,2).currentText(),
				self.grillaArchivos.cellWidget(ubicacion,3).isChecked())
				self.cjtoSabanas.insertarSabana(sabana)
			indice += 1
		
		if len(self.cjtoSabanas.listaSabanas) < self.grillaArchivos.rowCount():
			indice = 0
			while indice < self.grillaArchivos.rowCount():
				nombre = self.grillaArchivos.cellWidget(indice, 1).text()
				if self.cjtoSabanas.buscarSabana(nombre) == -1:
					sabana = Sabana(self.grillaArchivos.cellWidget(indice,1).text(),
					self.grillaArchivos.cellWidget(indice,2).currentText(),
					self.grillaArchivos.cellWidget(indice,3).isChecked())
					self.cjtoSabanas.insertarSabana(sabana)
				indice += 1
	
	def accionBotonFinalizar(self):
		self.eliminarArchivoBoton.setEnabled(False)
		if not self.cjtoSabanas:
			self.finalizarBoton.setEnabled(False)
			self.cjtoSabanas = self.crearCjtoSabanas()
		else:
			self.actualizarCjtoSabanas()
		
		
		#Funcion en Pagina1
		verificarColumnas(self.cjtoSabanas)

		
		
		self.flag = self.cjtoSabanas.todoVerificado()
		for item in self.cjtoSabanas.listaSabanas:
			self.actualizarGrillaArchivos(item)
		
		
		if	self.flag:
			parser = Parser()
			flag = parser.parsear(self.cjtoSabanas)
			if flag == -1:
				aviso = QtGui.QMessageBox.about(self,
				"Aviso", "Existen entradas en la sabana Movistar que no fueron ingresadas")
			#Hacer una espera
			
			self.crearPagina2()
			
			
	def archivoListo(self, archivo):
		flag = True
		indice = 0
		while flag and indice < self.grillaArchivos.rowCount():
			if self.grillaArchivos.cellWidget(indice,1).text() == archivo:
				self.grillaArchivos.cellWidget(indice,3).setCheckState(QtCore.Qt.Checked)
			indice = indice + 1
			
	def sinAmbiguedades(self):
		for item in self.cjtoSabanas.listaSabanas:
			if item.control == 2 and not item.checked:
				return False
		return True
	
	
	def accionOkBoton(self):
		dic = Diccionario()
		# obtener datos de la interfaz y trabajarlos
		sinonimo = unicode(self.sinonimoLinea.text(), "latin")
		aux = dic.traduccionConceptos([str(self.conceptosLista.currentText())])
		concepto = aux[0]
		
		if self.nuevoSinonimo:
			dic.agregarSinonimo(concepto, sinonimo)
			self.nuevoSinonimo = False
		self.sabanaActual.listaTuplas.append((sinonimo, [concepto]))
		

		self.condicion.acquire()
		if len(self.listaAux) > 0:
			elemento = self.listaAux.pop()
			if len(elemento[1]) == 0:
				self.nuevoSinonimo = True
			elemento = (elemento[0], self.sabanaActual.conceptosDisponibles(elemento[1]))
			self.listaHilo.append(elemento)
			self.condicion.notify()
			self.condicion.release()
		else:
			self.sabanaActual.checked = True
			indice = self.indiceGrilla(self.sabanaActual.nombreArchivo)
			self.grillaArchivos.cellWidget(indice, 3).setChecked(True)
			self.grillaArchivos.cellWidget(indice, 4).setText("")
			self.condicion.notify()
			self.condicion.release()
			if not self.sinAmbiguedades():
				self.accionVerificarBoton()
			else:
				self.hilo.fin = True
				print "termino el hilo"
				# Es por si el hilo necesita volver a iniciarse
				self.hilo = []
				self.grupoArchivo.setEnabled(True)
				self.grupoColumnas.setVisible(False)
				self.grupoColumnas.setEnabled(False)
				self.finalizarBoton.setEnabled(True)
				self.finalizarBoton.setText("Finalizar")
				self.verificarBoton.setEnabled(False)
		
	#FIN PRIMERA PANTALLA
	
	# INICIO SEGUNDA PANTALLA
	def accionTodoCheck(self):
	
		if self.todoCheck.isChecked():
			self.nroOrigenCheck.setChecked(True)
			self.nroDestinoCheck.setChecked(True)
			self.fechaInicioCheck.setChecked(True)
			self.horaInicioCheck.setChecked(True)
			self.duracionCheck.setChecked(True)
			self.nroImeiCheck.setChecked(True)
			self.nroSimCheck.setChecked(True)
			self.celdaIdCheck.setChecked(True)
			self.dirOrigenCheck.setChecked(True)
			self.dirDestinoCheck.setChecked(True)
			self.locOrigenCheck.setChecked(True)
			self.locDestinoCheck.setChecked(True)
			self.msjCheck.setChecked(True)
			self.estadoCheck.setChecked(True)
			self.dirAntenaCheck.setChecked(True)
			self.locAntenaCheck.setChecked(True)
			self.provAntenaCheck.setChecked(True)
			self.titOrigenCheck.setChecked(True)
			self.titDestinoCheck.setChecked(True)
			self.empOrigenCheck.setChecked(True)
			self.empDestinoCheck.setChecked(True)
			self.provOrigenCheck.setChecked(True)
			self.provDestinoCheck.setChecked(True)
			self.contMensajeCheck.setChecked(True)	
		else:
			self.nroOrigenCheck.setChecked(False)
			self.nroDestinoCheck.setChecked(False)
			self.fechaInicioCheck.setChecked(False)
			self.horaInicioCheck.setChecked(False)
			self.duracionCheck.setChecked(False)
			self.nroImeiCheck.setChecked(False)
			self.nroSimCheck.setChecked(False)
			self.celdaIdCheck.setChecked(False)
			self.dirOrigenCheck.setChecked(False)
			self.dirDestinoCheck.setChecked(False)
			self.locOrigenCheck.setChecked(False)
			self.locDestinoCheck.setChecked(False)
			self.msjCheck.setChecked(False)
			self.estadoCheck.setChecked(False)
			self.dirAntenaCheck.setChecked(False)
			self.locAntenaCheck.setChecked(False)
			self.provAntenaCheck.setChecked(False)
			self.titOrigenCheck.setChecked(False)
			self.titDestinoCheck.setChecked(False)
			self.empOrigenCheck.setChecked(False)
			self.empDestinoCheck.setChecked(False)
			self.provOrigenCheck.setChecked(False)
			self.provDestinoCheck.setChecked(False)
			self.contMensajeCheck.setChecked(False)
			
	def limpiarPantallaBusqueda(self):
		self.nroOrigen.clear()
		self.nroDestino.clear()
		self.codLinea.clear()
		self.codAreaOpc.setCurrentIndex(0)
		self.codAreaOpcDistinto.setChecked(True)
		self.fechaDesde.setDate(QtCore.QDate(1800, 01, 01))
		self.fechaHasta.setDate(QtCore.QDate.currentDate())
		self.horaDesde.setTime(QtCore.QTime(00,00,00))
		self.horaHasta.setTime(QtCore.QTime(23,59,59))
		if self.antena.count > 0:
			self.antena.setCurrentIndex(0)
		self.duracionDesde.setCurrentIndex(0)
		self.duracionHasta.setCurrentIndex(self.duracionHasta.count() - 1)
		#Grupo Avanzada
		self.nroImei.clear()
		self.nroSim.clear()
		if self.idCelda.count > 0:
			self.idCelda.setCurrentIndex(0)
		self.tipoMsj.setCurrentIndex(0)
		if self.provAntena.count > 0:
			self.provAntena.setCurrentIndex(0)
		if self.locAntena.count > 0:
			self.locAntena.setCurrentIndex(0)
		self.dirOrigen.clear()
		self.dirDestino.clear()
		self.locOrigen.clear()
		self.locDestino.clear()
		self.provOrigen.clear()
		self.provDestino.clear()
		self.titularOrigen.clear()
		self.titularDestino.clear()
		self.empOrigen.clear()
		self.empDestino.clear()
		self.contMsj.clear()
		if self.estadoMsj.count > 0:
			self.estadoMsj.setCurrentIndex(0)
		
	
	def accionLimpiarBoton(self):
		msgBox = QtGui.QMessageBox()
		msgBox.setText("¿Está seguro que desea limpiar la búsqueda?")
		msgBox.setInformativeText("Todos los datos de búsqueda volveran al estado inicial")
		siBoton = QtGui.QPushButton("Sí")
		noBoton = QtGui.QPushButton("No")
		msgBox.addButton(siBoton, QtGui.QMessageBox.YesRole)
		msgBox.addButton(noBoton, QtGui.QMessageBox.NoRole)
		msgBox.setIcon(QtGui.QMessageBox.Question)
		msgBox.exec_()
		if msgBox.clickedButton() == siBoton:
			self.limpiarPantallaBusqueda()
		else:
			print "no"
	
	def obtenerOpcionesSalida(self):
		lista = []
		
		if self.nroOrigenCheck.isChecked():
			lista.append("numeroOrigen")
		if self.nroDestinoCheck.isChecked():
			lista.append("numeroDestino")
		if self.fechaInicioCheck.isChecked():
			lista.append("fecha")
		if self.horaInicioCheck.isChecked():
			lista.append("hora")
		if self.duracionCheck.isChecked():
			lista.append("duracion")
		if self.nroImeiCheck.isChecked():
			lista.append("numeroImei")
		if self.nroSimCheck.isChecked():
			lista.append("numeroSim")
		if self.celdaIdCheck.isChecked():
			lista.append("celda")
		if self.dirOrigenCheck.isChecked():
			lista.append("direccionOrigen")
		if self.dirDestinoCheck.isChecked():
			lista.append("direccionDestino")
		if self.locOrigenCheck.isChecked():
			lista.append("localidadOrigen")
		if self.locDestinoCheck.isChecked():
			lista.append("localidadDestino")
		if self.msjCheck.isChecked():
			lista.append("tipoComunicacion")
		if self.estadoCheck.isChecked():
			lista.append("estado")
		if self.dirAntenaCheck.isChecked():
			lista.append("antenaDireccion")
		if self.locAntenaCheck.isChecked():
			lista.append("antenaLocalidad")
		if self.provAntenaCheck.isChecked():
			lista.append("antenaProvincia")
		if self.titOrigenCheck.isChecked():
			lista.append("titularOrigen")
		if self.titDestinoCheck.isChecked():
			lista.append("titularDestino")
		if self.empOrigenCheck.isChecked():
			lista.append("empresaOrigen")
		if self.empDestinoCheck.isChecked():
			lista.append("empresaDestino")
		if self.provOrigenCheck.isChecked():
			lista.append("provinciaOrigen")
		if self.provDestinoCheck.isChecked():
			lista.append("provinciaDestino")
		if self.contMensajeCheck.isChecked():
			lista.append("contenidoMensaje")
		lista.append("nombreArchivo")
		return lista
	
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
		
	
	def obtenerEncabezadosResultados(self):
		dic = Diccionario()
		listaColumnas = []
		for i in range(self.grillaResultados.columnCount()):
			listaColumnas.append(str(self.grillaResultados.horizontalHeaderItem(i).text()))
		listaColumnas = dic.traduccionConceptos(listaColumnas)
		return listaColumnas
	
	def accionBuscarBoton(self):
		if not self.ampliarBusquedaFlag:
			listaSalida = self.obtenerOpcionesSalida()
		else:
			self.ampliarBusquedaFlag = False
			listaSalida = self.obtenerEncabezadosResultados()
		listaBusqueda = self.obtenerOpcionesBusqueda()
		
		if self.nuevaBusquedaFlag:
			self.crearPagina3(listaSalida, listaBusqueda)
		else:
			query = self.db.busqueda(listaBusqueda, listaSalida)
			self.llenarGrillaResultados(listaSalida, query)
			self.grupoAmpliarBusqueda.close()
			

	def accionAvanzadaBoton(self):
		if self.grupoAvanzada.isVisible():
			self.grupoAvanzada.setVisible(False)
		else:
			self.grupoAvanzada.setVisible(True)
		self.grupoAmpliarBusqueda.adjustSize()
	# FIN SEGUNDA PANTALLA
	
	
	
	# INICIO TERCERA PANTALLA
	def accionNuevaBusquedaBoton(self):
		self.db.eliminarHistorialConsultas()
		self.nuevaBusquedaFlag = True
		self.crearPagina2()
		
	def accionAmpliarBusqueda(self):
		self.nuevaBusquedaFlag = False
		self.ampliarBusquedaFlag = True
		
		self.crearPagina2()
		self.grupoAmpliarBusqueda.setVisible(True)
	
	def llenarGrillaResultados(self, listaSalida, query):
		if query != -1:
			while query.next():
				indice = 0
				fila = self.grillaResultados.rowCount()
				dic = Diccionario()
				traducciones = dic.traduccionConceptos(listaSalida)		
				if fila == 0:
					self.grillaResultados.setColumnCount(len(listaSalida))
					self.grillaResultados.setHorizontalHeaderLabels(traducciones)
					self.grillaResultados.insertRow(fila)
				else:
					self.grillaResultados.insertRow(fila)
						
						
				for indice in range(len(listaSalida)):
					valor = query.value(indice)
					resultado = QtGui.QLabel(query.value(indice).toString())
					self.grillaResultados.setCellWidget(fila, indice, resultado)
		self.grillaResultados.resizeColumnsToContents()

	def celdaClick(self, fila, col):
		columna = self.grillaResultados.horizontalHeaderItem(col).text()
		dic = Diccionario()
		concepto = dic.traduccionConceptos([columna])
		if concepto[0] in {"numeroDestino", "numeroOrigen"}:
			self.grupoNumeroTelefono.setVisible(True)
			self.grupoUbicacionMapa.setVisible(False)
			self.grupoImei.setVisible(False)
			self.grupoTitular.setVisible(False)
			
			self.accionAsignarAlias.setEnabled(True)
			self.accionPedirIntervencion.setEnabled(True)
			self.accionCodigosDeArea.setEnabled(True)
			self.accionPedirArresto.setEnabled(False)
			self.accionVerMapa.setEnabled(False)				
		elif concepto[0] in {"antenaDireccion", "localidadOrigen", 
							"localidadDestino", "provinciaDestino",
							"provinciaOrigen", "direccionOrigen",
							"direccionDestino", "antenaProvincia",
							"antenaLocalidad"}:
			self.grupoNumeroTelefono.setVisible(False)
			self.grupoUbicacionMapa.setVisible(True)
			self.grupoImei.setVisible(False)
			self.grupoTitular.setVisible(False)
			
			self.accionAsignarAlias.setEnabled(False)
			self.accionPedirIntervencion.setEnabled(False)
			self.accionCodigosDeArea.setEnabled(True)
			self.accionPedirArresto.setEnabled(False)
			self.accionPedirIntervencion.setEnabled(False)
			self.accionVerMapa.setEnabled(True)
		elif concepto[0] in {"numeroImei"}:
			self.grupoNumeroTelefono.setVisible(False)
			self.grupoUbicacionMapa.setVisible(False)
			self.grupoImei.setVisible(True)
			self.grupoTitular.setVisible(False)
		
			self.accionAsignarAlias.setEnabled(False)
			self.accionPedirIntervencion.setEnabled(False)
			self.accionCodigosDeArea.setEnabled(True)
			self.accionPedirArresto.setEnabled(False)
			self.accionPedirIntervencion.setEnabled(False)
			self.accionVerMapa.setEnabled(False)
		elif concepto[0] in {"titularOrigen", "titularDestino"}:
			self.grupoNumeroTelefono.setVisible(False)
			self.grupoUbicacionMapa.setVisible(False)
			self.grupoImei.setVisible(False)
			self.grupoTitular.setVisible(True)
		
			self.accionAsignarAlias.setEnabled(False)
			self.accionPedirIntervencion.setEnabled(False)
			self.accionCodigosDeArea.setEnabled(True)
			self.accionPedirArresto.setEnabled(True)
			self.accionPedirIntervencion.setEnabled(False)
			self.accionVerMapa.setEnabled(False)

		
		
		else:
			self.grupoNumeroTelefono.setVisible(False)
			self.grupoUbicacionMapa.setVisible(False)
			self.grupoImei.setVisible(False)
			self.grupoTitular.setVisible(False)
			
			self.accionAsignarAlias.setEnabled(False)
			self.accionPedirIntervencion.setEnabled(False)
			self.accionCodigosDeArea.setEnabled(True)
			self.accionPedirArresto.setEnabled(False)
			self.accionPedirIntervencion.setEnabled(False)
			self.accionVerMapa.setEnabled(False)
			print concepto

	def actualizarGrillaResultados(self, datoViejo, datoNuevo, rango):
		for i in range(self.grillaResultados.rowCount()):
			if self.grillaResultados.cellWidget(i, rango[0]).text() == datoViejo:
				label = QtGui.QLabel(datoNuevo)
				label.setToolTip(datoViejo)
				self.grillaResultados.setCellWidget(i, rango[0], label)
			elif self.grillaResultados.cellWidget(i, rango[1]).text() == datoViejo:
				label = QtGui.QLabel(datoNuevo)
				label.setToolTip(datoViejo)
				self.grillaResultados.setCellWidget(i, rango[1], label)
			else:
				pass
			
	
	def accionAliasBoton(self):
		dialogo = AliasDialog(listarAlias(self.listaAlias))
		dialogo = dialogo.texto
		if dialogo[0] != "":
			rango = []
			dic = Diccionario()
			traducciones = dic.traduccionConceptos(["numeroOrigen", "numeroDestino"])
			fila = self.grillaResultados.currentRow()
			col = self.grillaResultados.currentColumn()
			for item in range(self.grillaResultados.columnCount()):
				columna = self.grillaResultados.horizontalHeaderItem(item).text()
				if columna in traducciones:
					if item != col:
						rango = [col, item]
			if dialogo[1]:
				if aliasDuplicado(dialogo[0], self.listaAlias):
					numero = self.grillaResultados.cellWidget(fila, col).text()
					alias = dialogo[0]
					self.listaAlias.append((alias, numero))
					self.actualizarGrillaResultados(numero, alias, rango)
					
				else:
					aviso = QtGui.QMessageBox.information(self,
				"Cuidado", "No es posible ingresar el alias deseado.")
			else:
				alias = dialogo[0]
				if alias == "Todos":
					indice = 0
					while len(self.listaAlias) > 0:
						if indice < len(self.listaAlias):
							self.actualizarGrillaResultados(self.listaAlias[indice][0], self.listaAlias[indice][1], rango)
							eliminarAlias(self.listaAlias, self.listaAlias[indice][1])
							indice += 1
						else:
							indice = 0
				else:
					numero = obtenerNumero(self.listaAlias, alias)
					eliminarAlias(self.listaAlias, numero)
					self.actualizarGrillaResultados(alias, numero, rango)
				
				
	def accionCodigosDeAreaBoton(self):
		dialogo = CodigoAreaDialog()
	
	def accionAsignarAliasBoton(self):
		pass
		
	def	accionPedirIntervencionBoton(self):
		pass
		
	def accionPedirArrestoBoton(Self):
		pass
		
	def accionUbicacionBoton(self):
		url = "http://maps.google.com/maps?q="
		aux = ""
		col = self.grillaResultados.currentColumn()
		fil = self.grillaResultados.currentRow()
		columna = self.grillaResultados.horizontalHeaderItem(col).text()
		dic = Diccionario()
		concepto = dic.traduccionConceptos([columna])[0]
		listaColumnas = self.obtenerEncabezadosResultados()
	
		if concepto in {"antenaDireccion", "antenaProvincia", "antenaLocalidad"}:
			for item in listaColumnas:
				if item == "antenaDireccion":
					aux = aux + self.grillaResultados.cellWidget(fil, listaColumnas.index(item)).text() + " "
				elif item == "antenaProvincia":
					aux = aux + self.grillaResultados.cellWidget(fil, listaColumnas.index(item)).text() + " "
				elif item == "antenaLocalidad":
					aux = aux + self.grillaResultados.cellWidget(fil, listaColumnas.index(item)).text() + " "
				else:
					pass
		elif concepto in {"localidadOrigen", "provinciaOrigen", "direccionOrigen"}:
			for item in listaColumnas:
				if item == "localidadOrigen":
					aux = aux + self.grillaResultados.cellWidget(fil, listaColumnas.index(item)).text() + " "
				elif item == "provinciaOrigen":
					aux = aux + self.grillaResultados.cellWidget(fil, listaColumnas.index(item)).text() + " "
				elif item == "direccionOrigen":
					aux = aux + self.grillaResultados.cellWidget(fil, listaColumnas.index(item)).text() + " "
				else:
					pass
		elif concepto in {"direccionDestino", "provinciaDestino", "localidadDestino"}:
			for item in listaColumnas:
				if item == "direccionDestino":
					aux = aux + self.grillaResultados.cellWidget(fil, listaColumnas.index(item)).text() + " "
				elif item == "provinciaDestino":
					aux = aux + self.grillaResultados.cellWidget(fil, listaColumnas.index(item)).text() + " "
				elif item == "localidadDestino":
					aux = aux + self.grillaResultados.cellWidget(fil, listaColumnas.index(item)).text() + " "
				else:
					pass
		else:
			print "Algo raro che"
		
		aux = unicode(aux, "latin")
		aux = aux.strip()
		aux = aux.replace(" ", "+")
		if aux == "":
			aux = "argentina"
		url = url + aux
		dialogo = UbicacionMapa(url)
		
	def accionImeiBoton(self):
		pass	
		
	def crearArchivo(self, fileName):
		lista = fileName.split(".")
		print lista.last()
		if lista.last() == "xls":
			workbook = Workbook() 
			sheet = workbook.add_sheet("Busqueda")
			
			for col in range(self.grillaResultados.columnCount()-1):
				style = easyxf('font: bold 1')
				sheet.write(0, col, unicode(self.grillaResultados.horizontalHeaderItem(col).text(), "latin"), style)
			
			for col in range(self.grillaResultados.columnCount()-1):
				for row in range(self.grillaResultados.rowCount()):
					value = unicode(self.grillaResultados.cellWidget(row, col).text(), "latin")
					sheet.write(row + 1, col, value)
			print "------------------"
			print fileName
			workbook.save(fileName)
		else:
			with open(unicode(fileName), 'wb') as stream:
				writer = csv.writer(stream)
				rowData = []
				for col in range(self.grillaResultados.columnCount()-1):
					rowData.append(unicode(self.grillaResultados.horizontalHeaderItem(col).text()).encode('utf8'))
				writer.writerow(rowData)

				for row in range(self.grillaResultados.rowCount()):
					rowData = []
					for col in range(self.grillaResultados.columnCount()-1):
						rowData.append(unicode(self.grillaResultados.cellWidget(row, col).text()).encode('utf8'))
					writer.writerow(rowData)
		
		
	def guardarResultadosBoton(self):
		archivo = QtGui.QFileDialog.getSaveFileName(self,
		"Guardar Archivo...",
		"",
		"Excel Files (*.xls);;Coma Separated Value (*.csv)")
		
		if archivo:
			# lista = archivo.split("/")
			# item = lista.last()
			self.crearArchivo(archivo)
		
	def handlePaintRequest(self, printer):
		document = QtGui.QTextDocument()
		cursor = QtGui.QTextCursor(document)
		table = cursor.insertTable(
			self.grillaResultados.rowCount(), self.grillaResultados.columnCount())
		for col in range(table.columns()):
			cursor.insertText(self.grillaResultados.horizontalHeaderItem(col).text())
			cursor.movePosition(QtGui.QTextCursor.NextCell)
		for row in range(table.rows()):
			for col in range(table.columns()):
				cursor.insertText(self.grillaResultados.cellWidget(row, col).text())
				cursor.movePosition(QtGui.QTextCursor.NextCell)
		document.print_(printer)
	
	def vistaPreviaBoton(self):
		dialog = QtGui.QPrintPreviewDialog()
		dialog.setWindowTitle("Vista Previa Impresión")
		dialog.paintRequested.connect(self.handlePaintRequest)
		dialog.exec_()
	
	def limpiarGrilla(self):
		while self.grillaResultados.rowCount() != 0:
			self.grillaResultados.removeRow(0)
	
	def accionRefinarBoton(self):
		self.cantidadRefinamientos += 1
		if self.cantidadRefinamientos <= 14:
			self.ampliarBusquedaBoton.setEnabled(False)
			dialog = RefinarBusquedaDialog()
			listaBusqueda = dialog.listaBusqueda
			dic = Diccionario()
			columnas = []
			for indice in range(self.grillaResultados.columnCount()):
				columnas.append(unicode(self.grillaResultados.horizontalHeaderItem(indice).text(), "latin"))
			#Saco nombreArchivo	
			print "Las Columnas"
			print columnas
			encabezados = dic.traduccionConceptos(columnas)
			print "Encabezados"
			print encabezados
			refinamiento = self.db.refinarBusqueda(listaBusqueda, encabezados, self.cantidadRefinamientos)
			print refinamiento
			self.limpiarGrilla()
			self.llenarGrillaResultados(encabezados, refinamiento)
		else:
			aviso = QtGui.QMessageBox.information(self,
			"Cuidado", "No puede refinar búsqueda mas de 14 veces")
			
	# FIN TERCERA PANTALLA
	
	
	
	
	
	
if __name__ == '__main__':
	import sys, time
	
	app = QtGui.QApplication(sys.argv)
	splash_pix = QtGui.QPixmap('splash_loading.png')
	splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	splash.setMask(splash_pix.mask())
	splash.show()
	programa = VentanaPpal()
	programa.show()
	splash.finish(programa)
	sys.exit(app.exec_())	
