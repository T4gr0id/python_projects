import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, \
    QTableView, QGridLayout, QListWidget, QLabel, QListView, QTabWidget, QFrame, \
    QHeaderView, QFormLayout                                                        # +++
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QTableView(self)
        self.model = QStandardItemModel()
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Имя", "Пол", "Возраст", "Отделение", "Диагноз"])

        self.table.setAlternatingRowColors(True)                                    # +
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)  # +

        self.btn = QPushButton("Отправить")
        self.btn.clicked.connect(self.add)

        self.years = QLabel('Возраст', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.years.setMaximumWidth(60)
        self.years_line = QLineEdit(placeholderText='Введите возраст...')
        self.diagnose_line = QLineEdit(placeholderText='Введите диагноз...')
        self.diagnose = QLabel('Диагноз', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.otd_line = QLineEdit(placeholderText='Введите отделение...')
        self.otd = QLabel('Отделение', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.gender_line = QLineEdit(placeholderText='Введите пол...')
        self.gender = QLabel('Пол', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.name_line = QLineEdit(placeholderText='Введите имя...')
        self.name = QLabel('Имя', alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.init()

    def init(self):
        grid = QGridLayout(self)
        grid.addWidget(self.name, 1, 0)
        grid.addWidget(self.name_line, 1, 1, 1, 3)
        grid.addWidget(self.gender, 2, 0)
        grid.addWidget(self.gender_line, 2, 1, 1, 3)
        grid.addWidget(self.years, 3, 0)
        grid.addWidget(self.years_line, 3, 1, 1, 3)
        grid.addWidget(self.otd, 4, 0)
        grid.addWidget(self.otd_line, 4, 1, 1, 3)
        grid.addWidget(self.diagnose, 5, 0)
        grid.addWidget(self.diagnose_line, 5, 1, 1, 3)
        grid.addWidget(self.btn, 6, 1, 1, 3) #, 1, -10)
        grid.addWidget(self.table, 7, 0, 5, 4)

    def add(self):
        rows = self.model.rowCount()
        columns = self.model.columnCount()
        for column in range(columns):
            if column == 0:
                self.model.setItem(rows, column, QStandardItem(self.name_line.text()))
            if column == 1:
                self.model.setItem(rows, column, QStandardItem(self.gender_line.text()))
            if column == 2:
                self.model.setItem(rows, column, QStandardItem(self.years_line.text()))
            if column == 3:
                self.model.setItem(rows, column, QStandardItem(self.otd_line.text()))
            if column == 4:
                self.model.setItem(rows, column, QStandardItem(self.diagnose_line.text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = Example()
    ex.resize(700, 500)
    ex.setWindowTitle('Как передать введенные данные из LineEdit в таблицу?')
    ex.setWindowIcon(QIcon('key.png'))
    ex.show()
    sys.exit(app.exec_())
