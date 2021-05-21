import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from mplwidget import MplWidget
import random
from pyqtGUI_nagrev import *
from nagrev import *


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tablewidget_headers = ['Координата']
        self.coords_data = []
        self.T = []
        # Добавь валидатор на инпут
        # self.lineEdit_3.setValidator(QtGui.QIntValidator(1, 99))
        # Замени, чтобы не было масштабирования
        # setPointSize -> setPixelSize
        self.ui.pushButton.clicked.connect(self.get_result)
        self.ui.pushButton_2.clicked.connect(self.export_data)

    def get_result(self):
        if self.ui.lineEdit.text() == '' or self.ui.lineEdit_2.text() == '' \
                or self.ui.lineEdit_4.text() == '' or self.ui.lineEdit_5.text() == '':
            pass
        else:
            table_header = f'Температура'
            self.ui.tableWidget.setColumnCount(2)
            self.tablewidget_headers.append(table_header)
            self.ui.tableWidget.setHorizontalHeaderLabels(self.tablewidget_headers)
            self.ui.tableWidget.setRowCount(int(self.ui.lineEdit_4.text()))
            start_variables(B=(int(self.ui.lineEdit.text()))/1000,
                TN=int(self.ui.lineEdit_2.text()),
                K=int(self.ui.lineEdit_4.text()),
                XK=int(self.ui.lineEdit_5.text()),
                a1=int(self.ui.lineEdit_6.text()))
            self.T = calculate_T(K=int(self.ui.lineEdit_4.text()),
                XK=int(self.ui.lineEdit_5.text()),
                a1=int(self.ui.lineEdit_6.text()))
            for coords in range(int(self.ui.lineEdit_4.text())):
                delta_coords = int(self.ui.lineEdit.text()) / (int(self.ui.lineEdit_4.text())-1)
                current_coords = f'{delta_coords * coords:.1f}'
                self.coords_data.append(current_coords)
                current_temp = f'{self.T[coords]:.1f}'
                self.ui.tableWidget.setItem(coords, 0, QtWidgets.QTableWidgetItem(current_coords))
                self.ui.tableWidget.setItem(coords, 1, QtWidgets.QTableWidgetItem(current_temp))
            self.add_mpl()
            self.coords_data = []
            self.ui.tabWidget.setCurrentIndex(1)    #Переключение на вторую вкладку

    def export_data(self):
        with open("nagrev_export_data.txt", "w", encoding='windows-1251') as file:
            file.write(f'Координата,мм;Температура, град\n')
            for x in range(int(self.ui.lineEdit_4.text())):
                file.write(f'{self.ui.tableWidget.item(x, 0).text()};{self.ui.tableWidget.item(x, 1).text()}\n')


    def add_mpl(self):
        self.ui.widget.canvas.axes.clear()
        self.ui.widget.canvas.axes.set_xlabel("Температура, С")  # ось абсцисс
        self.ui.widget.canvas.axes.set_ylabel("Толщина, мм")
        self.ui.widget.canvas.axes.grid(1, ls='--', color='#777777', alpha=0.5, lw=1)
        # self.ui.widget.canvas.axes.set_xlim(min(self.T), max(self.T))
        self.ui.widget.canvas.axes.plot(self.T, self.coords_data)
        self.ui.widget.canvas.axes.set_title('График температуры')
        self.ui.widget.canvas.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
