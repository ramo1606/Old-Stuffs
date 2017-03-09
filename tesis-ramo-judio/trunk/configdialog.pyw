#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##	 * Redistributions of source code must retain the above copyright
##	   notice, this list of conditions and the following disclaimer.
##	 * Redistributions in binary form must reproduce the above copyright
##	   notice, this list of conditions and the following disclaimer in
##	   the documentation and/or other materials provided with the
##	   distribution.
##	 * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##	   the names of its contributors may be used to endorse or promote
##	   products derived from this software without specific prior written
##	   permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt4 import QtCore, QtGui


from Fuentes.Parsers.Parser import Parser
from Fuentes.Diccionario.Diccionario import Diccionario
from Hilo import Hilo

import sys
from threading import Condition

import configdialog_rc


class Sabana():
	def __init__(self, nombreArchivo, nombreEmpresa):
		self.nombreArchivo = nombreArchivo
		self.nombreEmpresa = nombreEmpresa
		self.control = false
		# self.listaEncabezados = Parser().listaEncabezados((nombreArchivo, nombreEmpresa))
		# self.cantidad = len(self.listaEncabezados)
		# self.listaEncabezadosVacia = False
		# self.listaTuplas = []
		
		
	def insertarTupla(self, tupla):
		self.listaTuplas.append(tupla)
		self.cantidad -= 1
		if self.cantidad == 0:
			self.listaEncabezadosVacia = True
	
	def sacarEncabezado(self):
		if self.listaEncabezados:
			return self.listaEncabezados.pop()
		else:
			print "Error al sacar encabezado"

	def sabanaVacia(self):
		return self.listaEncabezadosVacia
		
	def aliasArchivo(self):
		alias = self.nombreArchivo
		return alias.split("/")[len(alias.split("/")) - 1]
		
		
class ConjuntoSabanas():
	def __init__(self):
		self.listaSabanas = []
		self.inidice = 0
		self.cantidadSabanas = 0
		self.completo = False
		self.listaResultado = []
	
	def insertarSabana(self, sabana):
		if not sabana.sabanaVacia():
			self.listaSabanas.append(sabana)
			self.cantidadSabanas += 1
		else:
			self.listaResultado.append(sabana)
			
		if not self.listaSabanas:
			self.completo = True
		
	def sacarSabana(self):
		if self.listaSabanas:
			self.cantidadSabanas -= 1
			return self.listaSabanas.pop()
	
	def listadoResultado(self):
		return self.listaResultado
	
		


class ConfigurationPage(QtGui.QWidget):
	def __init__(self, parent=None):
		super(ConfigurationPage, self).__init__(parent)

		self.grupoArchivo = QtGui.QGroupBox("Carga de Archivos")
		
		self.condicion = Condition()
		self.listaHilo = []
		self.listaConfirmacionColumnas = []
		
		
		#Sector de Carga de Archivos
		self.cargarArchivoBoton = QtGui.QPushButton("Cargar Archivo...")
		self.cargarArchivoBoton.setToolTip("Agregar un nuevo archivo")
		self.eliminarArchivoBoton = QtGui.QPushButton("Eliminar")
		self.eliminarArchivoBoton.setToolTip("Eliminar archivo de la lista")
		self.finalizarBoton = QtGui.QPushButton("Finalizar Carga")
		self.finalizarBoton.setToolTip("Finaliza la carga de archivos")
		self.eliminarArchivoBoton.setEnabled(False)
		self.finalizarBoton.setEnabled(False)
			
		self.grillaArchivos = QtGui.QTableWidget(0,4)
		self.grillaArchivos.setToolTip("Lista de archivos cargados")
		self.grillaArchivos.setHorizontalHeaderLabels(["Archivo", "Ubicacion", "Empresa", "Control"])
		self.grillaArchivos.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.grillaArchivos.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.grillaArchivos.setSortingEnabled(True)
		
		

		botonLayout = QtGui.QHBoxLayout()
		botonLayout.addWidget(self.eliminarArchivoBoton)
		botonLayout.addWidget(self.finalizarBoton)
		
		
		archivoLayout = QtGui.QVBoxLayout()
		archivoLayout.addWidget(self.cargarArchivoBoton)
		archivoLayout.addWidget(self.grillaArchivos)
		archivoLayout.addLayout(botonLayout)
		
		
		self.grupoColumnas = QtGui.QGroupBox("Unificacion de Columnas")
		self.grupoColumnas.setEnabled(False)
		#Sector de unificacion de columnas
		self.archivoLabel = QtGui.QLabel()
		self.sinonimoLinea = QtGui.QLineEdit()
		self.sinonimoLinea.setReadOnly(True)
		self.sinonimoLinea.setToolTip("Nombre de la columna del archivo")
		self.sinonimoLabel = QtGui.QLabel("es lo mismo que:")
		self.conceptosLista = QtGui.QComboBox()
		self.conceptosLista.setToolTip("Significado del sinonimo")
		self.conceptosLista.setSizeAdjustPolicy(self.conceptosLista.AdjustToContents)
		
		
		self.siBoton = QtGui.QPushButton("Si")
		self.noBoton = QtGui.QPushButton("No")
		
		
		
		columnasLayout = QtGui.QGridLayout()
		columnasLayout.addWidget(self.archivoLabel, 0, 0)
		columnasLayout.addWidget(self.sinonimoLinea, 1, 0)
		columnasLayout.addWidget(self.sinonimoLabel, 1, 1)
		columnasLayout.addWidget(self.conceptosLista, 1, 2)
		columnasLayout.addWidget(self.siBoton, 2, 1)
		columnasLayout.addWidget(self.noBoton, 2, 2)	
		
		
		paginaLayout = QtGui.QVBoxLayout()
		paginaLayout.addLayout(archivoLayout)
		
		pagLayout = QtGui.QVBoxLayout()
		pagLayout.addLayout(columnasLayout)
		
		self.grupoArchivo.setLayout(paginaLayout)
		self.grupoColumnas.setLayout(pagLayout)
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(self.grupoArchivo)
		mainLayout.addWidget(self.grupoColumnas)
		mainLayout.addStretch(1)
		
		self.setLayout(mainLayout)
		
		#Conexiones
		self.cargarArchivoBoton.clicked.connect(self.abrirArchivo)
		self.eliminarArchivoBoton.clicked.connect(self.eliminarArchivo)
		self.finalizarBoton.clicked.connect(self.accionBotonFinalizar)
		self.siBoton.clicked.connect(self.accionSiBoton)
		self.noBoton.clicked.connect(self.accionNoBoton)
		
		
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
				listadoEmpresas.addItems(["Claro", "Personal", "Movistar", "Nextel"]) 
				check = QtGui.QCheckBox()
				check.setEnabled(False)
				#Primer Archivo Ingresado
				if self.grillaArchivos.rowCount() == 0:
					self.grillaArchivos.insertRow(0)
				else:
					self.grillaArchivos.insertRow(self.grillaArchivos.rowCount())
				
				self.grillaArchivos.setCellWidget(self.grillaArchivos.rowCount()-1,0, archivoNombre)
				self.grillaArchivos.setCellWidget(self.grillaArchivos.rowCount()-1,1, archivoUbicacion)
				self.grillaArchivos.setCellWidget(self.grillaArchivos.rowCount()-1,2, listadoEmpresas)
				self.grillaArchivos.setCellWidget(self.grillaArchivos.rowCount()-1,3, check)
				
				#--------------
				self.grillaArchivo.setRowHidden(self.grillaArchivos.rowCount()-1, True)
				#--------------
				
				self.grillaArchivos.resizeColumnsToContents()				
			else:
				aviso = QtGui.QMessageBox.information(self,
				"Cuidado", "No es posible ingresar mas de una vez el mismo archivo.")
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
			"Cuidado", "Antes debe selccionar una fila.")
		else:
			self.grillaArchivos.removeRow(fila)
			if self.grillaArchivos.rowCount() == 0:
				self.eliminarArchivoBoton.setEnabled(False)
				self.finalizarBoton.setEnabled(False)
				self.grupoColumnas.setEnabled(False)
	
	# listado = [(nombreArchivo, empresa)]
	def listadoArchivos(self):
		indice = 0
		self.conjuntoSabanas = ConjuntoSabanas()
		for i in range(self.grillaArchivos.rowCount()):
			print self.grillaArchivos.cellWidget(indice,1).text(), self.grillaArchivos.cellWidget(indice,2).currentText()
			sabana = Sabana(self.grillaArchivos.cellWidget(indice,1).text(),
			self.grillaArchivos.cellWidget(indice,2).currentText())
			self.conjuntoSabanas.insertarSabana(sabana)
	
		
	#self.tresupla = [(arch, empre, [encab])]
	def accionBotonFinalizar(self):
		self.grupoArchivo.setEnabled(False)
		self.grupoColumnas.setEnabled(True)
		self.listadoArchivos()
		
		sabana = self.conjuntoSabanas.sacarSabana()

		
		nombreArchivo = sabana.aliasArchivo()
		self.listaHilo.append(sabana.sacarEncabezado())
		self.conjuntoSabanas.insertarSabana(sabana)
		self.hilo = Hilo(self.listaHilo, self.conceptosLista, self.condicion, self.archivoLabel, nombreArchivo, self.sinonimoLinea)
		self.hilo.start()
		
	
	def archivoListo(self, archivo):
		flag = True
		indice = 0
		while flag and indice < self.grillaArchivos.rowCount():
			if self.grillaArchivos.cellWidget(indice,1).text() == archivo:
				if Parser().chequearEmpresa(archivo, self.grillaArchivos.cellWidget(indice,2).currentText()):
					self.grillaArchivos.cellWidget(indice,3).setCheckState(QtCore.Qt.Checked)
					tresupla = (archivo,
								self.grillaArchivos.cellWidget(indice,2).currentText(),
								self.listaConfirmacionColumnas)
					return tresupla
				else:
					aviso = QtGui.QMessageBox.warning(self,
					"Cuidado", "Es posible que el archivo " + archivo + " no sea de la empresa que dice ser")
					self.grupoColumnas.setEnabled(False)
					self.grupoArchivo.setEnabled(True)
					
			indice = indice + 1
			
	
	def accionSiBoton(self):
		
		sabana = self.conjuntoSabanas.sacarSabana()
		
		tupla = (self.conceptosLista.currentText(), self.sinonimoLinea.text())
		sabana.insertarTupla(tupla)
		
		self.condicion.acquire()
				
		self.hilo.nombreArchivo = sabana.aliasArchivo()
		self.listaHilo.append(sabana.sacarEncabezado())
		self.conjuntoSabanas.insertarSabana(sabana)
		if self.conjuntoSabanas.completo:
			self.hilo.fin = True
			print "terminamos"
			self.siBoton.setEnabled(False)
		self.condicion.notify()
		self.condicion.release()
		print "apreto si"
		
	
	def accionNoBoton(self):
		# todo 
		# armar lista para parsers definitivos
		self.condicion.acquire()
		if len(self.tuplasEncabezados) > 0:#Tengo tuplas
			tupla = self.tuplasEncabezados.pop()
			if len(tupla[1]) > 0: #tengo encabezado	
				sinonimo = tupla[1].pop()
				self.hilo.nombreArchivo = tupla[0].split("/")[len(tupla[0].split("/")) - 1]
				self.listaHilo.append(sinonimo)
				if len(tupla[1]) > 0:
					self.tuplasEncabezados.append(tupla)
				else:
					self.archivoListo(tupla[0])
		else:
			self.hilo.fin = True
		self.condicion.notify()
		self.condicion.release()
		print "apreto no"
	
	def tuplaConfirmacionColumnas(self):
		if self.sinonimoLinea.text() != "" and self.conceptosLista.currentText() != "":
			tupla = (self.conceptosLista.currentText(), self.sinonimoLinea.text())
			return tupla
		else:
			print "Error al armar la tupla"
		
	
	
class UpdatePage(QtGui.QWidget):
	def __init__(self, parent=None):
		super(UpdatePage, self).__init__(parent)

		updateGroup = QtGui.QGroupBox("Package selection")
		systemCheckBox = QtGui.QCheckBox("Update system")
		appsCheckBox = QtGui.QCheckBox("Update applications")
		docsCheckBox = QtGui.QCheckBox("Update documentation")

		packageGroup = QtGui.QGroupBox("Existing packages")

		packageList = QtGui.QListWidget()
		qtItem = QtGui.QListWidgetItem(packageList)
		qtItem.setText("Qt")
		qsaItem = QtGui.QListWidgetItem(packageList)
		qsaItem.setText("QSA")
		teamBuilderItem = QtGui.QListWidgetItem(packageList)
		teamBuilderItem.setText("Teambuilder")

		startUpdateButton = QtGui.QPushButton("Start update")

		updateLayout = QtGui.QVBoxLayout()
		updateLayout.addWidget(systemCheckBox)
		updateLayout.addWidget(appsCheckBox)
		updateLayout.addWidget(docsCheckBox)
		updateGroup.setLayout(updateLayout)

		packageLayout = QtGui.QVBoxLayout()
		packageLayout.addWidget(packageList)
		packageGroup.setLayout(packageLayout)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(updateGroup)
		mainLayout.addWidget(packageGroup)
		mainLayout.addSpacing(12)
		mainLayout.addWidget(startUpdateButton)
		mainLayout.addStretch(1)

		self.setLayout(mainLayout)


class QueryPage(QtGui.QWidget):
	def __init__(self, parent=None):
		super(QueryPage, self).__init__(parent)

		packagesGroup = QtGui.QGroupBox("Look for packages")

		nameLabel = QtGui.QLabel("Name:")
		nameEdit = QtGui.QLineEdit()

		dateLabel = QtGui.QLabel("Released after:")
		dateEdit = QtGui.QDateTimeEdit(QtCore.QDate.currentDate())

		releasesCheckBox = QtGui.QCheckBox("Releases")
		upgradesCheckBox = QtGui.QCheckBox("Upgrades")

		hitsSpinBox = QtGui.QSpinBox()
		hitsSpinBox.setPrefix("Return up to ")
		hitsSpinBox.setSuffix(" results")
		hitsSpinBox.setSpecialValueText("Return only the first result")
		hitsSpinBox.setMinimum(1)
		hitsSpinBox.setMaximum(100)
		hitsSpinBox.setSingleStep(10)

		startQueryButton = QtGui.QPushButton("Start query")

		packagesLayout = QtGui.QGridLayout()
		packagesLayout.addWidget(nameLabel, 0, 0)
		packagesLayout.addWidget(nameEdit, 0, 1)
		packagesLayout.addWidget(dateLabel, 1, 0)
		packagesLayout.addWidget(dateEdit, 1, 1)
		packagesLayout.addWidget(releasesCheckBox, 2, 0)
		packagesLayout.addWidget(upgradesCheckBox, 3, 0)
		packagesLayout.addWidget(hitsSpinBox, 4, 0, 1, 2)
		packagesGroup.setLayout(packagesLayout)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(packagesGroup)
		mainLayout.addSpacing(12)
		mainLayout.addWidget(startQueryButton)
		mainLayout.addStretch(1)

		self.setLayout(mainLayout)


class ConfigDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		super(ConfigDialog, self).__init__(parent)

		self.contentsWidget = QtGui.QListWidget()
		self.contentsWidget.setViewMode(QtGui.QListView.IconMode)
		self.contentsWidget.setIconSize(QtCore.QSize(96, 84))
		self.contentsWidget.setMovement(QtGui.QListView.Static)
		self.contentsWidget.setMaximumWidth(128)
		self.contentsWidget.setSpacing(12)

		self.pagesWidget = QtGui.QStackedWidget()
		self.paginaConfig = ConfigurationPage()
		self.paginaActual = UpdatePage()
		self.paginaConsulta = QueryPage()
		self.pagesWidget.addWidget(self.paginaConfig)
		self.pagesWidget.addWidget(self.paginaActual)
		self.pagesWidget.addWidget(self.paginaConsulta)

		self.closeButton = QtGui.QPushButton("Close")
		
		self.createIcons()
		self.contentsWidget.setCurrentRow(0)

		
		horizontalLayout = QtGui.QHBoxLayout()
		horizontalLayout.addWidget(self.contentsWidget)
		horizontalLayout.addWidget(self.pagesWidget, 1)

		buttonsLayout = QtGui.QHBoxLayout()
		buttonsLayout.addStretch(1)
		buttonsLayout.addWidget(self.closeButton)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addLayout(horizontalLayout)
		mainLayout.addStretch(1)
		mainLayout.addSpacing(12)
		mainLayout.addLayout(buttonsLayout)

		self.setLayout(mainLayout)

		self.setWindowTitle("Config Dialog")

	def changePage(self, current, previous):
		if not current:
			current = previous

		self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))

	def createIcons(self):
		configButton = QtGui.QListWidgetItem(self.contentsWidget)
		configButton.setIcon(QtGui.QIcon(':/images/config.png'))
		configButton.setText("Configuration")
		configButton.setTextAlignment(QtCore.Qt.AlignHCenter)
		configButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

		updateButton = QtGui.QListWidgetItem(self.contentsWidget)
		updateButton.setIcon(QtGui.QIcon(':/images/update.png'))
		updateButton.setText("Update")
		updateButton.setTextAlignment(QtCore.Qt.AlignHCenter)
		updateButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

		queryButton = QtGui.QListWidgetItem(self.contentsWidget)
		queryButton.setIcon(QtGui.QIcon(':/images/query.png'))
		queryButton.setText("Query")
		queryButton.setTextAlignment(QtCore.Qt.AlignHCenter)
		queryButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

		self.contentsWidget.currentItemChanged.connect(self.changePage)

		
		
		
class VentanaPpal(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(VentanaPpal, self).__init__(parent)

		self.ui = ConfigDialog()
		self.setCentralWidget(self.ui)
		self.setGeometry(100, 100, 800, 600)
		
		self.statusBar()
		
		self.crearAcciones()
		self.crearMenues()
		
		
		# Conexiones
		self.ui.closeButton.clicked.connect(self.close)

		
	def crearAcciones(self):
		self.accionAbrir = QtGui.QAction("&Abrir...", self,
				shortcut=QtGui.QKeySequence.New,
				statusTip="Agregar archivo a la lista", triggered=self.ui.paginaConfig.abrirArchivo)
		
		# TODO
		self.accionImprimir = QtGui.QAction("&Imprimir", self,
				shortcut=QtGui.QKeySequence.New,
				statusTip="Imprimir los resultados", triggered=self.imprimirResultados)
		
		
		# TODO
		self.accionGuardar = QtGui.QAction("&Guardar...", self,
				shortcut=QtGui.QKeySequence.Save,
				statusTip="Guardar resultados", triggered=self.guardarReusltados)
				
		# TODO
		self.accionCopiar = QtGui.QAction("&Copiar", self,
				shortcut=QtGui.QKeySequence.Copy,
				statusTip="Copiar", triggered=self.copiar)		
		
		# TODO
		self.accionPegar = QtGui.QAction("&Pegar", self,
				shortcut=QtGui.QKeySequence.Paste,
				statusTip="Pegar", triggered=self.pegar)
	
	def crearMenues(self):
		# Menu Archivo
		self.menuArchivo = self.menuBar().addMenu("&Archivo")
		self.menuArchivo.addAction(self.accionAbrir)
		self.menuArchivo.addAction(self.accionGuardar)
		
		# Menu Editar
		self.editarMenu = self.menuBar().addMenu("&Editar")
		self.editarMenu.addAction(self.accionCopiar)
		self.editarMenu.addAction(self.accionPegar)
		
		# Menu Opciones
		self.opcionesMenu = self.menuBar().addMenu("&Opciones")


	def guardarReusltados(self):
		pass
		
	def imprimirResultados(self):
		pass
		
	def copiar(self):
		pass
		
	def pegar(self):
		pass		
		
if __name__ == '__main__':

	import sys

	app = QtGui.QApplication(sys.argv)
	programa = VentanaPpal()
	programa.show()
	sys.exit(app.exec_())	
