# import os

def crearTabla():
	archivo = open("temp.csv", "r")
	linea = archivo.readline()
	linea = linea.split("\n")[0]
	linea = linea.split(";")
	print linea
	metodoejemplo(linea)
	

def metodoejemplo(lista):
		create = "CREATE TABLE `sabanas`.`ejemplo` ("
		for item in lista:
			if item.find("fecha") != -1:
				create = create + item + " DATE,"
			elif item.find("hora") != -1:
				create = create + item + " TIME,"
			else:
				create = create + item + " TEXT,"
				
		create = create + ");"
		open("crear.txt", "w").write(create)
		
		
		
	# INSERT INTO `esquema`.`tabla` (`col1`,`col2`) VALUES ('val1','val2');	
	# INSERT INTO table_name
	# VALUES (value1, value2, value3,...)	
	# [(concepto, ubicacion)] tupla de trabajo		
def insertarDatos():
	archivo = open("temp.csv", "r")
	linea = archivo.readline()
	linea = linea.split("\n")[0].split(";")
	listaConceptos = linea
	
	salida = open("insertar.txt", "w")
	
	for item in archivo:
		item = item.split("\n")[0].split(";")
		insert = "INSERT INTO ejemplo ("
		indice = 0
		
	
		while indice < len(listaConceptos):
			if indice == len(listaConceptos)-1:
				insert = insert + listaConceptos[indice] + ") VALUES ("
			else:
				insert = insert + listaConceptos[indice] + ", "
			indice += 1
		
		indice = 0
		while indice < len(item) - 1:
			if indice == len(item) - 2:
				insert = insert + "'" + item[indice] + "'" + ");\n"
			elif indice == 2:
				if item[indice] == "":
					insert = insert + "'18000101'" + ","
				else:
					insert = insert + "'" + item[indice] + "'" + ","
			elif indice == 3:
				if item[indice] == "":
					insert = insert + "'18000101'" + ","
				else:
					insert = insert + "'" + item[indice] + "'" + ","
			elif indice == 4:
				if item[indice] == "":
					insert = insert + "'25:00:00'" + ","
				else:
					insert = insert + "'" + item[indice] + "'" + ","
			elif indice == 5:
				if item[indice] == "":
					insert = insert + "'25:00:00'" + ","
				else:
					insert = insert + "'" + item[indice] + "'" + ","
			else:
				insert = insert + "'" + item[indice] + "'" + ","
			indice += 1
		salida.write(insert)
		
		
# from PyQt4 import QtGui, QtCore

# STARTTEXT = ('This TextEdit provides autocompletions for words that have ' +
# 'more than 3 characters.\nYou can trigger autocompletion using %s\n\n'''% (
# QtGui.QKeySequence("Ctrl+E").toString(QtGui.QKeySequence.NativeText)))

# class DictionaryCompleter(QtGui.QCompleter):
	# def __init__(self, parent=None):
		# words = []
		# try:
			# f = open("words.txt","r")
			# for word in f:
				# words.append(word.strip())
			# f.close()
		# except IOError:
			# print "dictionary not in anticipated location"
		# QtGui.QCompleter.__init__(self, words, parent)

# class CompletionTextEdit(QtGui.QTextEdit):
	# def __init__(self, parent=None):
		# super(CompletionTextEdit, self).__init__(parent)
		# self.setMinimumWidth(400)
		# self.setPlainText(STARTTEXT)
		# self.completer = None
		# self.moveCursor(QtGui.QTextCursor.End)

	# def setCompleter(self, completer):
		# if self.completer:
			# self.disconnect(self.completer, 0, self, 0)
		# if not completer:
			# return

		# completer.setWidget(self)
		# completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
		# completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		# self.completer = completer
		# self.connect(self.completer,
			# QtCore.SIGNAL("activated(const QString&)"), self.insertCompletion)

	# def insertCompletion(self, completion):
		# tc = self.textCursor()
		# extra = (completion.length() -
			# self.completer.completionPrefix().length())
		# tc.movePosition(QtGui.QTextCursor.Left)
		# tc.movePosition(QtGui.QTextCursor.EndOfWord)
		# tc.insertText(completion.right(extra))
		# self.setTextCursor(tc)

	# def textUnderCursor(self):
		# tc = self.textCursor()
		# tc.select(QtGui.QTextCursor.WordUnderCursor)
		# return tc.selectedText()

	# def focusInEvent(self, event):
		# if self.completer:
			# self.completer.setWidget(self);
		# QtGui.QTextEdit.focusInEvent(self, event)

	# def keyPressEvent(self, event):
		# if self.completer and self.completer.popup().isVisible():
			# if event.key() in (
			# QtCore.Qt.Key_Enter,
			# QtCore.Qt.Key_Return,
			# QtCore.Qt.Key_Escape,
			# QtCore.Qt.Key_Tab,
			# QtCore.Qt.Key_Backtab):
				# event.ignore()
				# return

		# has ctrl-E been pressed??
		# isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and
					  # event.key() == QtCore.Qt.Key_E)
		# if (not self.completer or not isShortcut):
			# QtGui.QTextEdit.keyPressEvent(self, event)

		# ctrl or shift key on it's own??
		# ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier ,
				# QtCore.Qt.ShiftModifier)
		# if ctrlOrShift and event.text().isEmpty():
			# ctrl or shift key on it's own
			# return

		# eow = QtCore.QString("~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=") #end of word

		# hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
						# not ctrlOrShift)

		# completionPrefix = self.textUnderCursor()

		# if (not isShortcut and (hasModifier or event.text().isEmpty() or
		# completionPrefix.length() < 3 or
		# eow.contains(event.text().right(1)))):
			# self.completer.popup().hide()
			# return

		# if (completionPrefix != self.completer.completionPrefix()):
			# self.completer.setCompletionPrefix(completionPrefix)
			# popup = self.completer.popup()
			# popup.setCurrentIndex(
				# self.completer.completionModel().index(0,0))

		# cr = self.cursorRect()
		# cr.setWidth(self.completer.popup().sizeHintForColumn(0)
			# + self.completer.popup().verticalScrollBar().sizeHint().width())
		# self.completer.complete(cr) ## popup it up!

# if __name__ == "__main__":

	# app = QtGui.QApplication([])
	# completer = DictionaryCompleter()
	# te = CompletionTextEdit()
	# te.setCompleter(completer)
	# te.show()
	# app.exec_()

	