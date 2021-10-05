from mainWindow import Ui_MainWindow #основное GUI-окно
import reestr_pb #реестр PB второе окно
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox #интерфейс
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtSql import  QSqlDatabase, QSqlTableModel

#import configparser #библиотека для чтения настроек из файла settings.ini
import sys
class MainApp(QMainWindow, UiMainWindow): #основной класс главного окна
  def __init__(self, parent=None):
    super(MainApp,self).__init__(parent)
    self.setupUi(self) #иницилизация главного окна
    self.init_Ui() #инициализация привязок к кнопкам главного окна
  
  def Init_Ui(self): #привязка функций к кнопкам
    self.reestr.clicked.connect(self.openReestr) #Кнопка открытия реестра
  def openReestr(self):
    self.operR = reestrWidget()
    self.operR.show()

class reestrWidget(QWidget, reestr_pb.Ui_Form):
  def __init__(self, parent=None):
    super(reestrWidget,self).__init__(parent)
    self.setupUi(self)
    self.Init_Ui() #подключение к БД и пр.
  def init_Ui(self):
    self.CreateConnection() #подключение к БД
    self.CreateModel() #Создание модели таблицы
    #строка поиска
    filter_proxy_model = QSortFilterProxyModel()
    filter_proxy_model.setSourceModel(self.model)
    filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
    filter_proxy_model.setFilterKeyColumn(2)
    search_field=self.search
    search_field.textChanged.connect(filter_proxy_model.setFilterRegExp)
    self.ReestrView.setModel(filter_proxy_model) #привязка отфильтрованной модели к таблице
    
    self.ReestrView.resizeColumnsToContents() #ресайз размера колонок по содержимому
    self.ReestrView.hideColumn(0) #Скрываем столбец с ID
    self.pushAdd.clicked.connect(self.addReestr)
    self.pushDel.clicked.connect(self.delReestr)
  def CreateConnection(self):
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("clients.db")
    if not con.open():
      QMessageBox.critical(None,"QTableView Example - Error!", "Database Error: %s" % con.lastError().databasetext(),)
      return False
    return True
  
  def CreateModel(self):
    
    
  
  
  
