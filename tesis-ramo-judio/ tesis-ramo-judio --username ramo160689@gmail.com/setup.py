from cx_Freeze import setup,Executable
import sys

includefiles = ['Fuentes\Manuales\manual.pdf', 'Fuentes\Funcionalidad\codigosArea.txt', 'splash_loading.png', "Fuentes\Parsers\Diccionario", ("C:\Python27\Lib\site-packages\PyQt4\plugins\sqldrivers","sqldrivers")]
includes = ['sip', 'PyQt4.QtCore', 'PyQt4.QtGui', 'PyQt4.QtWebKit', 'PyQt4.QtSql', 'PyQt4.QtNetwork', 'PyQt4.QtSql']
excludes = []
packages = ['sip', 're', 'os', 'sys', 'xlwt', 'xlrd', 'datetime', 'PyQt4.QtSql','Fuentes.Funcionalidad', 'Fuentes.Parsers', 'Fuentes.Parsers.Diccionario', 'Fuentes.Hilo']


setup(
	name = 'Astrea',
	version = '1.0',
	description = 'Buscador en sabanas telefonicas',
	author = 'Alurralde/Bigatti',
	author_email = 'ramo160689@gmail.com',
	options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles, 'includes':includes}}, 
	executables = [Executable(script='configdialog.pyw', base="Win32GUI")]
)