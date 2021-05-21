import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from mplwidget import MplWidget
import random
from pyqtGUI import *
from raschet import *


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tablewidget1_headers = ['Координата']
        self.coords_data = []
        self.T = []
        self.T_top, self.T_bot = [], []
        self.zone_time = []
        # Валидаторы
        self.ui.lineEdit.setValidator(QtGui.QIntValidator(1, 999))
        self.ui.lineEdit_2.setValidator(QtGui.QIntValidator(1, 9999))
        self.ui.lineEdit_3.setValidator(QtGui.QIntValidator(1, 99))
        self.ui.lineEdit_4.setValidator(QtGui.QIntValidator(1, 99))
        self.ui.lineEdit_5.setValidator(
            QtGui.QDoubleValidator(0, 99, 2, notation=QtGui.QDoubleValidator.StandardNotation))
        self.ui.lineEdit_6.setValidator(QtGui.QIntValidator(1, 999))
        self.ui.lineEdit_11.setValidator(QtGui.QIntValidator(1, 9999))
        self.ui.lineEdit_12.setValidator(QtGui.QIntValidator(1, 99999))
        self.ui.lineEdit_13.setValidator(QtGui.QIntValidator(1, 9999))
        self.ui.lineEdit_14.setValidator(QtGui.QIntValidator(1, 99999))
        self.ui.lineEdit_15.setValidator(QtGui.QIntValidator(1, 99))
        self.ui.lineEdit_16.setValidator(QtGui.QIntValidator(1, 9999))
        self.ui.lineEdit_17.setValidator(
            QtGui.QDoubleValidator(0, 99, 2, notation=QtGui.QDoubleValidator.StandardNotation))
        self.ui.lineEdit_18.setValidator(QtGui.QIntValidator(1, 999999))
        # Замени, чтобы не было масштабирования
        # setPointSize -> setPixelSize

        # Кнопки
        self.ui.pushButton.clicked.connect(self.get_result)
        self.ui.pushButton_3.clicked.connect(self.get_result_tab2)
        self.ui.pushButton_2.clicked.connect(self.zone_table_append)
        self.ui.pushButton_4.clicked.connect(self.export_data)

        # Картинки
        logo_1 = resource_path("POWERPNT_CXLFW6i2uP.png")
        logo_2 = resource_path("POWERPNT_nmj5jX9473.png")
        self.ui.label.setPixmap(QtGui.QPixmap(logo_1))
        self.ui.label_10.setPixmap(QtGui.QPixmap(logo_2))

    def get_result(self):
        self.T = []
        self.T_top, self.T_bot = [], []
        self.zone_time = []
        self.coords_data = []

        try:
            rows_count = int(self.ui.lineEdit_3.text())
        except ValueError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', f'Поле количество зон в печи не заполнено')
            return
        for row in range(self.ui.tableWidget.rowCount()):
            self.zone_time.append(0)
            for column in range(self.ui.tableWidget.columnCount()):
                current_cell = self.ui.tableWidget.item(row, column).text()
                if column == 0:
                    if current_cell.isdigit():
                        self.T_bot.append(int(current_cell))
                        self.T_top.append(int(current_cell))
                    else:
                        QtWidgets.QMessageBox.about(self, 'Ошибка',
                                                        f'Температура в зоне №{row+1} задана не верно')
                        return
                elif column == 1:
                    if current_cell.isdigit():
                        self.zone_time[row] += int(current_cell) * 60 * 60
                    elif current_cell == '':
                        pass
                    else:
                        QtWidgets.QMessageBox.about(self, 'Ошибка',
                                                    f'Время в зоне №{row + 1}, ячейке {column+1}, задано не верно')
                        return
                elif column == 2:
                    if current_cell.isdigit():
                        self.zone_time[row] += int(current_cell) * 60
                    elif current_cell == '':
                        pass
                    else:
                        QtWidgets.QMessageBox.about(self, 'Ошибка',
                                                    f'Время в зоне №{row + 1}, ячейке {column+1}, задано не верно')
                        return
                elif column == 3:
                    if current_cell.isdigit():
                        self.zone_time[row] += int(current_cell)
                    elif current_cell == '':
                        pass
                    else:
                        QtWidgets.QMessageBox.about(self, 'Ошибка',
                                                    f'Время в зоне №{row + 1}, ячейке {column + 1}, задано не верно')
                        return
            if self.zone_time[row] == 0:
                QtWidgets.QMessageBox.about(self, 'Ошибка',
                                            f'Время в зоне №{row + 1} задано нулевым значением')
                return
        if self.ui.lineEdit.text() == '' or self.ui.lineEdit_2.text() == '' \
                or self.ui.lineEdit_4.text() == '' or self.ui.lineEdit_5.text() == '' \
                or len(self.zone_time) != rows_count \
                or len(self.T_bot) != rows_count:
            QtWidgets.QMessageBox.about(self, 'Ошибка', f'Исходные данные не заполнены до конца')
        else:
            self.ui.tableWidget1.setColumnCount(int(self.ui.lineEdit_3.text()) + 1)
            self.ui.tableWidget1.setRowCount(int(self.ui.lineEdit_4.text()))
            for i in range(1, int(self.ui.lineEdit_3.text()) + 1):
                table_header = f'Зона {i}'
                self.tablewidget1_headers.append(table_header)
            self.ui.tableWidget1.setHorizontalHeaderLabels(self.tablewidget1_headers)
            current_material = materials_dict[self.ui.comboBox.currentText()]
            self.T = calc_plast4r(b=(int(self.ui.lineEdit.text())) / 1000,
                                  T_ini=(int(self.ui.lineEdit_2.text())),
                                  T_up=self.T_top,
                                  T_down=self.T_bot,
                                  t_comm=self.zone_time,
                                  substance=current_material,
                                  k=(int(self.ui.lineEdit_4.text())),
                                  dt=(float(self.ui.lineEdit_5.text())))
            for coords in range(int(self.ui.lineEdit_4.text())):
                delta_coords = int(self.ui.lineEdit.text()) / (int(self.ui.lineEdit_4.text()) - 1)
                current_coords = f'{int(self.ui.lineEdit.text()) - (delta_coords * coords):.1f}'
                self.coords_data.append(current_coords)
                for zone in range(1, int(self.ui.lineEdit_3.text()) + 1):
                    current_temp = f'{self.T[zone - 1][coords]:.1f}'
                    self.ui.tableWidget1.setItem(coords, 0, QtWidgets.QTableWidgetItem(current_coords))
                    self.ui.tableWidget1.setItem(coords, zone, QtWidgets.QTableWidgetItem(current_temp))
            self.add_mpl_zones()
            self.ui.tabWidget.setCurrentIndex(2)  # Переключение на вторую вкладку

    def get_result_tab2(self):
        if self.ui.lineEdit_6.text() == '' or self.ui.lineEdit_11.text() == '' \
                or self.ui.lineEdit_18.text() == '' or self.ui.lineEdit_15.text() == '' \
                or self.ui.lineEdit_17.text() == '' or self.ui.lineEdit_16.text() == '' \
                or self.ui.lineEdit_12.text() == '' or self.ui.lineEdit_15.text() == '' \
                or self.ui.lineEdit_13.text() == '' or self.ui.lineEdit_14.text() == '':
                QtWidgets.QMessageBox.about(self, 'Ошибка', f'Исходные данные не заполнены до конца')
        else:
            self.coords_data = []
            self.T = []
            self.ui.tableWidget1.setColumnCount(2)
            table_header = f'Температура'
            self.tablewidget1_headers.append(table_header)
            self.ui.tableWidget1.setHorizontalHeaderLabels(self.tablewidget1_headers)
            if (int(self.ui.lineEdit_11.text()) > int(self.ui.lineEdit_13.text())) and \
                    (int(self.ui.lineEdit_11.text()) > int(self.ui.lineEdit_16.text())):
                current_material = materials_cooling_dict[self.ui.comboBox_2.currentText()]
            else:
                current_material = materials_dict[self.ui.comboBox_2.currentText()]
            self.ui.tableWidget1.setRowCount(int(self.ui.lineEdit_15.text()))
            self.T = calc_plast3r(b=(int(self.ui.lineEdit_6.text())) / 1000,
                                  T_ini=(int(self.ui.lineEdit_11.text())),
                                  T_up=(int(self.ui.lineEdit_16.text())),
                                  alpha_up=(int(self.ui.lineEdit_12.text())),
                                  T_down=(int(self.ui.lineEdit_13.text())),
                                  alpha_down=(int(self.ui.lineEdit_14.text())),
                                  t_comm=(int(self.ui.lineEdit_18.text())),
                                  substance=current_material,
                                  k=(int(self.ui.lineEdit_15.text())),
                                  dt=(float(self.ui.lineEdit_17.text())))
            for coords in range(int(self.ui.lineEdit_15.text())):
                delta_coords = int(self.ui.lineEdit_6.text()) / (int(self.ui.lineEdit_15.text()) - 1)
                current_coords = f'{int(self.ui.lineEdit_6.text()) - (delta_coords * coords):.1f}'
                self.coords_data.append(current_coords)
                current_temp = f'{self.T[coords]:.1f}'
                self.ui.tableWidget1.setItem(coords, 0, QtWidgets.QTableWidgetItem(current_coords))
                self.ui.tableWidget1.setItem(coords, 1, QtWidgets.QTableWidgetItem(current_temp))
            self.add_mpl()
            self.coords_data = []
            self.ui.tabWidget.setCurrentIndex(2)  # Переключение на вторую вкладку

    def add_mpl(self):
        self.ui.widget.canvas.axes.clear()
        self.ui.widget.canvas.axes.set_xlabel("Температура, С")
        self.ui.widget.canvas.axes.set_ylabel("Толщина, мм")
        self.ui.widget.canvas.axes.grid(1, ls='--', color='#777777', alpha=0.5, lw=1)
        # self.ui.widget.canvas.axes.set_xlim(min(self.T), max(self.T))
        self.ui.widget.canvas.axes.plot(self.T[::-1], self.coords_data[::-1])
        self.ui.widget.canvas.axes.set_title('График температуры')
        self.ui.widget.canvas.draw()

    def add_mpl_zones(self):
        self.ui.widget.canvas.axes.clear()
        self.ui.widget.canvas.axes.set_xlabel("Температура, С")
        self.ui.widget.canvas.axes.set_ylabel("Толщина, мм")
        self.ui.widget.canvas.axes.grid(1, ls='--', color='#777777', alpha=0.5, lw=1)
        # self.ui.widget.canvas.axes.set_xlim(min(self.T), max(self.T))
        current_zone = 0
        for zone in self.T:
            current_zone += 1
            self.ui.widget.canvas.axes.plot(zone[::-1], self.coords_data[::-1], label=f'Зона {current_zone}')

        self.ui.widget.canvas.axes.legend(loc='best', shadow=True, fontsize='medium')
        self.ui.widget.canvas.axes.set_title('График температуры')
        self.ui.widget.canvas.draw()

    def zone_table_append(self):
        try:
            rows_count = int(self.ui.lineEdit_3.text())
        except ValueError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', f'Поле количество зон в печи не заполнено')
            return
        self.ui.tableWidget.setRowCount(int(self.ui.lineEdit_3.text()))
        for i in range(self.ui.tableWidget.rowCount()):
            for j in range(self.ui.tableWidget.columnCount()):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                font = QtGui.QFont()
                font.setFamily("Calibri")
                font.setPointSize(8)
                item.setFont(font)
                self.ui.tableWidget.setItem(i, j, item)

    def export_data(self):
        if self.ui.tableWidget1.item(0, 0) is None:
            QtWidgets.QMessageBox.about(self, 'Экспорт не удался', f'Таблица для экспорта пуста')
        else:
            with open("export_data.txt", "w", encoding='windows-1251') as file:
                headers = ''
                for column in range(self.ui.tableWidget1.columnCount()):
                    headers += f'{self.ui.tableWidget1.horizontalHeaderItem(column).text()};'
                file.write(f'{headers[:-1]}\n')
                for row in range(self.ui.tableWidget1.rowCount()):
                    item = ''
                    for column in range(self.ui.tableWidget1.columnCount()):
                        item += f'{self.ui.tableWidget1.item(row, column).text()};'
                    file.write(f'{item[:-1]}\n')
            QtWidgets.QMessageBox.about(self, 'Экспорт данных', f' Данные успешно экспортированы в txt файл\n '
                                                                f'{os.getcwd()}')


materials_dict = {
    '09Г2С': '09G2S',
    'Ст3сп': 'st3sp',
    'Сталь20': 'st20',
    'K60': 'K60',
    'SH400': 'sh400',
    'SH450': 'sh450',
    'SH500': 'sh500',
    'X70': 'X70',
}

materials_cooling_dict = {
    '09Г2С': '09G2S',
    'Ст3сп': 'st3sp',
    'Сталь20': 'st20',
    'K60': 'K60',
    'SH400': 'sh400_cooling',
    'SH450': 'sh450',
    'SH500': 'sh500_cooling',
    'X70': 'X70_cooling',
}

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
