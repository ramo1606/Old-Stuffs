import xlrd

class Sabana:
    def __init__(self, nomSabana):
        self.book = xlrd.open_workbook(nomSabana)
        self.sheet = self.book.sheet_by_index(0)
        self.filas = self.sheet.nrows
        self.columnas = self.sheet.ncols
        self.index = 0


    def tabla(self):
        flag = True
        while flag:
            if self.sheet.cell_type(self.index, 0) != xlrd.XL_CELL_EMPTY:
                flag = False
            else:
                self.index = self.index + 1
        return self.index


    def nombres(self):
        for colums in range(self.columnas):
            tipos = self.sheet.row_values(self.index,0,self.columnas)
        return tipos

    def lineasTotales(self,col):
        index1 = self.index + 1
        lista = []
        for rows in range(index1, self.filas - 1):
            linea = self.sheet.cell_value(rows,col)
            if not(linea in lista):
                lista.append(self.linea)
        return lista

