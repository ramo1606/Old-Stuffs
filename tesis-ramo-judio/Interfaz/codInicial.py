import os,sys

from Parser import Sabana

from PyQt4 import QtCore, QtGui

from Inicial import Ui_MainWindow

class Main(QtGui.QMainWindow):
        def __init__(self):
                QtGui.QMainWindow.__init__(self)
                self.ui=Ui_MainWindow()
                self.ui.setupUi(self)
                QtCore.QObject.connect(self.ui.pushButton_5, QtCore.SIGNAL("clicked()"), self.close)
                

                
        def cargaArchivos(self):

            file_ = QtGui.QFileDialog.getOpenFileName(self,
                "Buscar Archivo...",
                "*.xls",
                "All Files (*);;Text Files (*.txt)")
            if file_:
                self.ui.pushButton_2.setEnabled(True)
                lista = file_.split("/")
                item = lista.last()
                fileName = QtGui.QLabel(QtCore.QString(item))
                direction = QtGui.QLabel(file_)
                self.ui.tableWidget.setCellWidget(0,0, fileName)
                self.ui.tableWidget.setCellWidget(0,1, direction)
                self.sabana = Sabana(file_)
                self.sabana.tabla()
                encabezados = self.sabana.nombres()
                self.ui.lineEdit.clear()
                self.ui.lineEdit.setText(QtCore.QString(encabezados[0]))
                self.ui.comboBox.addItems(encabezados)

        def clearSelection(self):
                

        def close(self):
            sys.exit()


def main():
        # Again, this is boilerplate, it's going to be the same on
        # almost every app you write
        app = QtGui.QApplication(sys.argv)
        window=Main()
        window.show()
        
        # It's exec_ because exec is a reserved word in Python
        sys.exit(app.exec_())


if __name__ == "__main__":
          main()
