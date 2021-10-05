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
  
  
  
