from MainWindow import Ui_MainWindow  # основное GUI-окно
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QDateTime, QSortFilterProxyModel
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QStyledItemDelegate, QItemDelegate, QDateTimeEdit  # интерфейс
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel
from PyQt5.QtGui     import QBrush
from datetime import datetime
import sys#, pandas as pd

class MySortFilterProxyModel(QSortFilterProxyModel):
  def lessThan(self, left, right):
    if left.column() == 7:
      l = float(self.sourceModel().data(left))
      r = float(self.sourceModel().data(right))
      return l<r
    return super().lessThan(left, right)

class MainApp(QMainWindow, Ui_MainWindow):  # основной класс главного окна
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)  # иницилизация главного окна
        self.Init_Ui()  # инициализация привязок к кнопкам главного окна

    def load_data(self, sp):  # заставка
        for i in range(1, 11):  # Имитируем процесс
#            time.sleep(0.5)  # Что-то загружаем
            sp.showMessage("Загрузка данных... {0}%".format(i * 10),
                           QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
            QtWidgets.qApp.processEvents()  # Запускаем оборот цикла

    def Init_Ui(self):  # привязка функций к кнопкам
        self.CreateConnection()
        #self.CreateModel()
        self.model = CreateModel()
        # self.reestr.clicked.connect(self.openReestr)  # Кнопка открытия реестра
        self.refreshButton.clicked.connect(self.refreshRecord)

        # строка поиска
        self.filter_proxy_model = MySortFilterProxyModel()
        #self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setSourceModel(self.model)
        #self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(9)
        search_field = self.search
        search_field.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.MainReestr.setModel(self.filter_proxy_model)  # привязка отфильтрованной модели к таблице
        self.MainReestr.resizeColumnsToContents()  # ресайз размера колонок по содержимому
        #self.MainReestr.hideColumn(0)  # Скрываем столбец с ID
        self.MainReestr.setSortingEnabled(True)

        self.refresh_row = -1   # Будет содержать индекс обновляемой строки(-1 запрет обновления)
        # событие выбора строки
        self.selection_model = self.MainReestr.selectionModel()
        self.selection_model.selectionChanged.connect(self.selection_changed)
        # делегат 
        
        delegate = DateDelegate(self)
        self.MainReestr.setItemDelegateForColumn(8, delegate)
        self.MainReestr.setItemDelegateForColumn(9, delegate)
        
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
            #передача данных из списка в QlineEdit
            
            if row_data[1] != '':
                self.use_chip.setText(row_data[1])
            else:
                self.use_chip.setText('')
            if row_data[2] != '':
                self.merchant_name.setText(str(row_data[2]))
            else:
                self.merchant_name.setText('')
            if row_data[3] != '':
                self.merchant_city.setText(row_data[3])
            else:
                self.merchant_city.setText('')
            if row_data[4] != '':
                self.merchant_state.setText(row_data[4])
            else:
                self.merchant_state.setText('')
            if row_data[5] != '':
                self.zip.setText(str(row_data[5]))
            else:
                self.zip.setText('')
            if row_data[6] != '':
                self.mcc.setText(str(row_data[6]))
            else:
                self.mcc.setText('')
            if row_data[7] != '':
                self.amount.setText(str(row_data[7]))
            else:
                self.amount.setText('')
            if row_data[8] != '':                
                self.tmp_datetime.setDateTime(datetime.fromtimestamp(int(row_data[8])))
            else:
                self.tmp_date.setDate(QtCore.QDate.fromString('2022-01-01','yyyy-MM-dd'))
            if row_data[9] != '':
                self.tmp_date.setDateTime(datetime.fromtimestamp(int(row_data[9])))
            else:
                self.tmp_date.setDate(QtCore.QDate.fromString('2022-01-01','yyyy-MM-dd'))
            if row_data[10] != '':
                self.control.setText(str(row_data[10]))
            else:
                self.control.setText('')
            
            if row_data[11] != '':
                self.comment.setText(str(row_data[11]))
            else:
                self.comment.setText('')
            
        else:
            self.refresh_row = -1   # Если не была выбрана строка целиком, сбрасываем индекс
    #не работает!!
    def refreshRecord(self, MainReestr):  # Обновление строки в таблице (и базе данных)
        if (self.refresh_row == -1):
            return
        record = self.model.record(self.refresh_row)
        record.setValue(1, self.use_chip.text())
        record.setValue(2, self.merchant_name.text())
        record.setValue(3, self.merchant_city.text())
        record.setValue(4, self.merchant_state.text())
        record.setValue(5, self.zip.text())
        record.setValue(6, self.mcc.text())
        #record.setValue(7, float(self.amount.text()))
        #record.setValue(8, self.datetime.text())
        #ecord.setValue(9, self.date.text())
        record.setValue(10,self.control.text())
        record.setValue(11,self.comment.text())
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

class CreateModel(QSqlTableModel):
    def __init__(self, *args,**kwargs):
        super(CreateModel,self).__init__(*args,**kwargs)
        self.setTable('mainReestr')
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.setHeaderData(0, QtCore.Qt.Horizontal, 'id')
        self.setHeaderData(1, QtCore.Qt.Horizontal, 'Use Chip')
        self.setHeaderData(2, QtCore.Qt.Horizontal, 'Merchant Name')
        self.setHeaderData(3, QtCore.Qt.Horizontal, 'Merchant City')
        self.setHeaderData(4, QtCore.Qt.Horizontal, 'Merchant State')
        self.setHeaderData(5, QtCore.Qt.Horizontal, 'Zip')
        self.setHeaderData(6, QtCore.Qt.Horizontal, 'MCC')
        self.setHeaderData(7, QtCore.Qt.Horizontal, 'Amount')
        self.setHeaderData(8, QtCore.Qt.Horizontal, 'datetime')
        self.setHeaderData(9, QtCore.Qt.Horizontal, 'date')
        self.setHeaderData(10, QtCore.Qt.Horizontal, 'На контроле')
        self.setHeaderData(11, QtCore.Qt.Horizontal, 'Комментарий')
        self.select()
        while self.canFetchMore():
            self.fetchMore()
            
    def data(self, item, role = Qt.DisplayRole):
    #окраска, если если надо
        if role==Qt.BackgroundRole:
            control = super().index(item.row(), 10).data()
            if control == 'Да':
                return QtGui.QBrush(Qt.red)
    #изменяем формат вывода
        if role==Qt.DisplayRole:
            if item.column() == 7:
                result = super().data(item, role)
                return "{num:.2f}".format(num=result)
      #это теперь в делегате будет
      #if item.column() == 2:
      #  result = super().data(item, role)
      #  return QDateTime.fromString(result, "yyyy-MM-dd hh:mm:ss 000000")
        return super().data(item, role)

class DateDelegate(QItemDelegate):
    def __init__(self, parent = None):
        super().__init__(parent)
        
    def createEditor(self, parent, option, index):
        return QDateTimeEdit(parent)
    def setEditorData(self, editor, index):
        result = index.data()
        editor.setDateTime(QDateTime.fromSecsSinceEpoch(result).toPyDateTime())
    def setModelData(self, editor, model, index):
        result = editor.dateTime()
        result = result.toSecsSinceEpoch()
        model.setData(index, result)
    def paint(self, painter, option, index):
        self.drawBackground(painter, option, index)
        result = index.data()
        result = QDateTime.fromSecsSinceEpoch(result).toString("dd.MM.yyyy hh:mm:ss")
        #result = result.toString("yyyy-MM-dd hh:mm:ss")
        self.drawDisplay(painter, option, option.rect, result)
        self.drawFocus(painter, option, option.rect)

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
