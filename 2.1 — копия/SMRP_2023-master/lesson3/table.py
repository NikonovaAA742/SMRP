import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QTableWidgetItem, QFileDialog, \
    QInputDialog, QColorDialog, QDialog

from database import global_init, create_session, Patient
from database import Insurance
from ui_update_patient import Ui_Dialog
from ui_table import Ui_MainWindow


from PyQt5.QtCore import Qt, QModelIndex


class TableViewer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.table_is_changeable = True

    def initUI(self):
        global_init("database/db.db")
        self.session = create_session()
        self.pushButton.clicked.connect(self.load_table)

        self.pushButton1.clicked.connect(self.create_patient)

        self.tableWidget.doubleClicked.connect(self.update_patient)
        #self.tableWidget.cellChanged.connect(self.cell_changed)
        #self.pushButton_open_file.clicked.connect(self.color_dialog)

    def create_patient(self):
        self.patient_creator = PatientCreator()
        self.patient_creator.exec_()
        self.load_table()


    def update_patient(self, index: QModelIndex):
        current_row = index.row()
        id_ = int(self.tableWidget.item(current_row, 0).text())
        self.patient_updater = PatientUpdater(id_)
        self.patient_updater.exec_()
        self.load_table()


    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Выберите файл", '', 'Текстовый файл (*.txt);;Все файлы (*)')[0]
        print(file_name)

    def input_dialog(self):
        var = QInputDialog.getText(self, 'Введите имя', 'Как вас зовут?')
        print(var)

    def item_dialog(self):
        var = QInputDialog.getItem(self, "Выберите страну",
                                   "Откуда ты?",
                                   ("Россия", "Германия", "США"), 1, False)
        print(var)

    def color_dialog(self):
        color = QColorDialog.getColor()
        print(color)

    def load_table(self):
        self.table_is_changeable = False
        patients = self.session.query(Patient).all()
        self.tableWidget.setRowCount(0)
        for patient in patients:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            tmp = QTableWidgetItem(str(patient.id))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row_position, 0, tmp)
            tmp = QTableWidgetItem(str(patient.name))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row_position, 1, tmp)
            tmp = QTableWidgetItem(str(patient.bdate))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row_position, 2, tmp)
            tmp = QTableWidgetItem(str(patient.insurance.name))
            tmp.setFlags(tmp.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row_position, 3, tmp)
        self.table_is_changeable = True

    def cell_changed(self, row, col):
        if self.table_is_changeable:
            id_ = int(self.tableWidget.item(row, 0).text())
            patient = self.session.query(Patient).\
                filter(Patient.id == id_).first()
            if col == 1:
                patient.name = self.tableWidget.item(row, col).text()
                self.session.commit()
            elif col == 2:
                patient.bdate = self.tableWidget.item(row, col).text()
                self.session.commit()


class PatientUpdater(QDialog, Ui_Dialog):
    def __init__(self, patient_id):
        super().__init__()
        self.setupUi(self)

        self.session = create_session()
        self.patient = self.session.query(Patient).get(patient_id)
        self.label_id_2.setText(str(self.patient.id))
        self.lineEdit_name.setText(str(self.patient.name))
        self.lineEdit_bdate.setText(str(self.patient.bdate))
        insurances = self.session.query(Insurance).filter(Insurance.id != self.patient.insurance_id).all()
        self.comboBox.addItem(self.patient.insurance.name, self.patient.insurance.id)
        for insurance in insurances:
            self.comboBox.addItem(insurance.name, insurance.id)

        self.pushButton.clicked.connect(self.save_data)
        self.pushButton1.clicked.connect(self.delete_data)

    def save_data(self):
        self.patient.name = self.lineEdit_name.text()
        self.patient.bdate = self.lineEdit_bdate.text()
        cb_ci = self.comboBox.currentIndex()
        insurance_id = self.comboBox.itemData(cb_ci)
        self.patient.insurance_id = insurance_id
        self.session.commit()
        self.close()

    def delete_data(self):
        self.session.delete(self.patient)
        self.session.commit()
        self.close()


class PatientCreator(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.session = create_session()

        #self.patient = self.session.query(Patient).get(patient_id)
        #self.label_id_2.setText(str(self.patient.id))
        #self.lineEdit_name.setText(str(self.patient.name))
        #self.lineEdit_bdate.setText(str(self.patient.bdate))
        insurances = self.session.query(Insurance).all()#.filter(Insurance.id != self.patient.insurance_id).all()
        #self.comboBox.addItem(self.patient.insurance.name, self.patient.insurance.id)
        for insurance in insurances:
            self.comboBox.addItem(insurance.name, insurance.id)

        self.pushButton.clicked.connect(self.insert_data)

    def insert_data(self):
        cb_ci = self.comboBox.currentIndex()
        insurance_id = self.comboBox.itemData(cb_ci)
        #self.patient.insurance_id = insurance_id
        self.patient = Patient(name = self.lineEdit_name.text(), bdate = self.lineEdit_bdate.text(), insurance_id = insurance_id)
        #self.patient.name = self.lineEdit_name.text()
        #self.patient.bdate = self.lineEdit_bdate.text()

        #print(self.patient)
        #print(insurance_id)
        self.session.add(self.patient)
        self.session.commit()
        self.close()
        # parent = Parent(name="Родитель Пупы Лупина")
        # session.add(parent)
        # session.commit()

        #self.session.add(self.patient)




def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TableViewer()
    ex.show()
    sys.exit(app.exec())