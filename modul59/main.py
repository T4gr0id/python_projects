import PyQt5.QtSql
import time
from mainWindow import Ui_MainWindow  # основное GUI-окно

# import reestr_pb #реестр PB второе окно
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox  # интерфейс
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel

# import configparser #библиотека для чтения настроек из файла settings.ini
import sys

class MainApp(QMainWindow, Ui_MainWindow):  # основной класс главного окна
    customFormat = 'dd.MM.yyyy'
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)  # иницилизация главного окна
        self.Init_Ui()  # инициализация привязок к кнопкам главного окна

    def load_data(self, sp):  # заставка
        for i in range(1, 11):  # Имитируем процесс
            time.sleep(0.05)  # Что-то загружаем
            sp.showMessage("Загрузка данных... {0}%".format(i * 10),
                           QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
            QtWidgets.qApp.processEvents()  # Запускаем оборот цикла

    def Init_Ui(self):  # привязка функций к кнопкам
        self.CreateConnection()
        self.CreateModel()
        self.MyDateCalendar()

        # self.reestr.clicked.connect(self.openReestr)  # Кнопка открытия реестра
        self.StatusPB.clicked.connect(self.addRecord)
        self.DelPB.clicked.connect(self.delRecord)
        self.RefreshPB.clicked.connect(self.refReestr)
        self.refreshButton.clicked.connect(self.refreshRecord)

        # строка поиска
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(2)
        search_field = self.search
        search_field.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.MainReestr.setModel(self.filter_proxy_model)  # привязка отфильтрованной модели к таблице
        self.MainReestr.resizeColumnsToContents()  # ресайз размера колонок по содержимому
        self.MainReestr.hideColumn(0)  # Скрываем столбец с ID

        # центрирование содержимого столбцов в таблице
        delegate = AlignDelegate(self.MainReestr)
        for x in range(12):
            self.MainReestr.setItemDelegateForColumn(x, delegate)
        # заполнение комбобоксов
        spk_1 = ['Private Banking', 'Сбербанк 1']
        spk_2 = ['Нет', 'Да']
        self.statusPB.addItems(spk_1)
        self.statusPB.setCurrentIndex(-1)
        self.newStatusPB.addItems(spk_2)
        self.newStatusPB.setCurrentIndex(-1)
        self.inoBank.addItems(spk_2)
        self.inoBank.setCurrentIndex(-1)
        self.oes.addItems(spk_2)
        self.oes.setCurrentIndex(-1)
        self.control.addItems(spk_2)
        self.control.setCurrentIndex(-1)
        self.sanction.addItems(spk_2)
        self.sanction.setCurrentIndex(-1)

        self.refresh_row = -1   # Будет содержать индекс обновляемой строки(-1 запрет обновления)

        # событие выбора строки
        self.selection_model = self.MainReestr.selectionModel()
        self.selection_model.selectionChanged.connect(self.selection_changed)

    def selection_changed(self):
        #Формирование списка из данных выделенной строки
        rows = {index.row() for index in self.selection_model.selectedIndexes()}
        output = []
        if len(self.selection_model.selectedIndexes()) == 12:
            for row in rows:
                self.refresh_row = row  # Сохраняем индекс выбранной строки для обновления
                row_data = []
                for column in range(self.MainReestr.model().columnCount()):
                    index = self.MainReestr.model().index(row, column)
                    row_data.append(index.data())
                output.append(row_data)
            #print(output)
            #передача данных из списка в QlineEdit
            if row_data[1] != '':
                self.untb.setText(row_data[1])  # унтб
            else:
                self.untb.setText('')
            if row_data[2] != '':
                self.fio.setText(row_data[2])  # фио
            else:
                self.fio.setText('')
            if row_data[3] != '':
                self.birthdate.setText(row_data[3])  # дата рождения
            else:
                self.birthdate.clear()
            if row_data[4] != '':
                self.dul.setText(row_data[4])  # дул
            else:
                self.dul.setText('')
            #Статус PB
            if row_data[5] != '':
                if row_data[5] == 'Private Banking':
                    self.statusPB.setCurrentIndex(0)
                elif row_data[5] == 'Сбербанк 1':
                    self.statusPB.setCurrentIndex(1)
            else:
                self.statusPB.setCurrentIndex(-1)
            if row_data[6] != '':
                if row_data[6] == 'Нет':
                    self.newStatusPB.setCurrentIndex(0)
                elif row_data[6] == 'Да':
                    self.newStatusPB.setCurrentIndex(1)
            else:
                self.newStatusPB.setCurrentIndex(-1)
            if row_data[7] != '':
                if row_data[7] == 'Нет':
                    self.inoBank.setCurrentIndex(0)
                elif row_data[7] == 'Да':
                    self.inoBank.setCurrentIndex(1)
            else:
                self.inoBank.setCurrentIndex(-1)
            if row_data[8] != '':
                if row_data[8] == 'Нет':
                    self.oes.setCurrentIndex(0)
                elif row_data[8] == 'Да':
                    self.oes.setCurrentIndex(1)
            else:
                self.oes.setCurrentIndex(-1)
            if row_data[9] != '':
                if row_data[9] == 'Нет':
                    self.control.setCurrentIndex(0)
                elif row_data[9] == 'Да':
                    self.control.setCurrentIndex(1)
            else:
                self.control.setCurrentIndex(-1)
            if row_data[10] != '':
                if row_data[10] == 'Нет':
                    self.sanction.setCurrentIndex(0)
                elif row_data[10] == 'Да':
                    self.sanction.setCurrentIndex(1)
            else:
                self.sanction.setCurrentIndex(-1)
            if row_data[11] != '':
                self.comment.setText(row_data[11])
            else:
                self.comment.setText('')
        else:
            self.refresh_row = -1   # Если не была выбрана строка целиком, сбрасываем индекс

    #обновление модели
    def refReestr(self):
        self.model.select()

    def addRecord(self):  # добавление в неотфильтрованную модель
        record = self.model.record()
        record.setValue(1, self.untb.text())
        record.setValue(2, self.fio.text())
        record.setValue(3, self.birthdate.text())
        record.setValue(4, self.dul.text())
        record.setValue(5, self.statusPB.currentText())
        record.setValue(6, int(self.newStatusPB.currentIndex()))
        record.setValue(7, int(self.inoBank.currentIndex()))
        record.setValue(8, int(self.oes.currentIndex()))
        record.setValue(9, int(self.control.currentIndex()))
        record.setValue(10, int(self.sanction.currentIndex()))
        record.setValue(11, self.comment.text())
        self.model.insertRecord(-1, record)
        self.model.select()

    def delRecord(self, MainReestr):  # удаление из неотфильтрованной модели
        index = self.MainReestr.currentIndex()
        if not index.isValid():
            return
        record = self.model.record(index.row())
        self.model.removeRow(index.row())
        self.model.submitAll()
        self.model.select()

    def refreshRecord(self, MainReestr):  # Обновление строки в таблице (и базе данных)
        if (self.refresh_row == -1):
            return
        record = self.model.record(self.refresh_row)
        record.setValue(1, self.untb.text())
        record.setValue(2, self.fio.text())
        record.setValue(3, self.birthdate.text())
        record.setValue(4, self.dul.text())
        record.setValue(5, self.statusPB.currentText())
        record.setValue(6, int(self.newStatusPB.currentIndex()))
        record.setValue(7, int(self.inoBank.currentIndex()))
        record.setValue(8, int(self.oes.currentIndex()))
        record.setValue(9, int(self.control.currentIndex()))
        record.setValue(10, int(self.sanction.currentIndex()))
        record.setValue(11, self.comment.text())
        self.model.setRecord(self.refresh_row, record)
        self.model.select()
        self.refresh_row = -1   # Запрет на последующие обновления до следующего выделения строки

    def CreateConnection(self):
        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("clients.db")
        if not con.open():
            QMessageBox.critical(None, "QTableView Example - Error!",
                                 "Database Error: %s" % con.lastError().databasetext(), )
            return False
        return True

    def CreateModel(self):
        self.model = QSqlTableModel()
        self.model.setTable('mainReestr')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, 'УНТБ')
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, 'ФИО')
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, 'Дата рождения')
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, 'ДУЛ')
        self.model.setHeaderData(5, QtCore.Qt.Horizontal, 'Статус')
        self.model.setHeaderData(6, QtCore.Qt.Horizontal, 'Присвоение статуса')
        self.model.setHeaderData(7, QtCore.Qt.Horizontal, 'Запрос инобанка')
        self.model.setHeaderData(8, QtCore.Qt.Horizontal, 'Отказ')
        self.model.setHeaderData(9, QtCore.Qt.Horizontal, 'На контроле')
        self.model.setHeaderData(10, QtCore.Qt.Horizontal, 'Санкции')
        self.model.setHeaderData(11, QtCore.Qt.Horizontal, 'Комментарий')
        self.model.select()


    def MyDateCalendar(self):
        customFormat = 'dd.MM.yyyy'
        #self.birthdate = QtWidgets.QLineEdit()
        self.birthdate.setMaxLength(len(self.format()))
        self.validator = SimpleDateValidator(self)
        self.birthdate.setValidator(self.validator)
        #self.dropDownButton = QtWidgets.QToolButton()
        self.QCalendar.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_ArrowDown))
        self.QCalendar.setMaximumHeight(self.birthdate.sizeHint().height())
        self.QCalendar.setCheckable(True)
        self.QCalendar.setFocusPolicy(QtCore.Qt.NoFocus)

        self.calendar = QtWidgets.QCalendarWidget()
        self.calendar.setWindowFlags(QtCore.Qt.Popup)
        self.calendar.installEventFilter(self)
        self.QCalendar.pressed.connect(self.showPopup)
        self.QCalendar.released.connect(self.calendar.hide)
        self.birthdate.editingFinished.connect(self.editingFinished)
        self.calendar.clicked.connect(self.setDate)
        self.calendar.activated.connect(self.setDate)
        self.setDate(QtCore.QDate.currentDate())

    def editingFinished(self):
        if self.calendar.isVisible():
            return
        if not self.isValid():
            self.birthdate.setText('')

    def format(self):
        return self.customFormat or QtCore.QLocale().dateFormat(QtCore.QLocale.ShortFormat)

    def setFormat(self, format):
        # принимать только числовые форматы даты
        if format and 'MMM' in format or 'ddd' in format:
            return
        self.customFormat = format
        self.setDate(self.calendar.selectedDate())
        self.calendar.hide()
        self.birthdate.setMaxLength(self.format())
        self.validator.setFormat(self.format())

    def text(self):
        return self.birthdate.text()

    def date(self):
        if not self.isValid():
            return None
        date = QtCore.QDate.fromString(self.text(), self.format())
        if date.isValid():
            return date
        return int(self.text())

    def setDate(self, date):
        self.birthdate.setText(date.toString(self.format()))
        self.calendar.setSelectedDate(date)
        self.calendar.hide()

    def setDateRange(self, minimum, maximum):
        self.calendar.setDateRange(minimum, maximum)

    def isValid(self):
        text = self.text()
        if not text:
            return False
        date = QtCore.QDate.fromString(text, self.format())
        if date.isValid():
            self.setDate(date)
            return True
        try:
            year = int(text)
            start = self.calendar.minimumDate().year()
            end = self.calendar.maximumDate().year()
            if start <= year <= end:
                return True
        except:
            pass
        return False

    def hidePopup(self):
        self.calendar.hide()

    def showPopup(self):
        pos = self.birthdate.mapToGlobal(self.birthdate.rect().bottomLeft())
        pos += QtCore.QPoint(0, 1)
        rect = QtCore.QRect(pos, self.calendar.sizeHint())
        self.calendar.setGeometry(rect)
        self.calendar.show()
        self.calendar.setFocus()

    def eventFilter(self, source, event):
        # нажмите или отпустите кнопку, когда календарь отображается / скрывается
        if event.type() == QtCore.QEvent.Hide:
            self.QCalendar.setDown(False)
        elif event.type() == QtCore.QEvent.Show:
            self.QCalendar.setDown(True)
        return super().eventFilter(source, event)

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Down, QtCore.Qt.Key_F4):
            if not self.calendar.isVisible():
                self.showPopup()
        super().keyPressEvent(event)

class SimpleDateValidator(QtGui.QValidator):
    def validate(self, text, pos):
        if not text:
            return self.Acceptable, text, pos
        fmt = self.parent().format()
        _sep = set(fmt.replace('d', '').replace('M', '').replace('y', ''))

        for l in text:
            # убедитесь, что набранный текст представляет собой цифру или разделитель
            if not l.isdigit() and l not in _sep:
                return self.Invalid, text, pos
        years = fmt.count('y')
        if len(text) <= years and text.isdigit():
            return self.Acceptable, text, pos
        if QtCore.QDate.fromString(text, fmt).isValid():
            return self.Acceptable, text, pos
        return self.Intermediate, text, pos

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__()

    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter
        col, _data = index.column(), index.data()
        if col == 9 and _data == 1:
            painter.fillRect(option.rect, QtCore.Qt.red)
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("img1.jpg"))
    splash.showMessage("Загрузка данных... 0%",
                       QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    splash.show()  # Отображаем заставку
    QtWidgets.qApp.processEvents()  # Запускаем оборот цикла
    window = MainApp()
    window.load_data(splash)  # Загружаем данные
    window.show()
    splash.finish(window)  # Скрываем заставку
    sys.exit(app.exec_())
