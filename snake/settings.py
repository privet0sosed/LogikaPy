
from PyQt5 import QtCore, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setMaximumSize(225, 160) # size y 190
        Dialog.setMinimumSize(225, 160) # size y 190
        
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 120, 200, 32)) #pos x 150
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(20, 40, 190, 22)) #size x 100
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        # self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 100, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 100, 13)) # pos y 100
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(20, 90, 42, 22))  # pos y 120
        self.spinBox.setMaximum(30)
        self.spinBox.setProperty("value", 14)
        self.spinBox.setObjectName("spinBox")
        # self.pushButton = QtWidgets.QPushButton(Dialog)
        # self.pushButton.setGeometry(QtCore.QRect(130, 40, 75, 22))
        # self.pushButton.setObjectName("pushButton")
        # self.lineEdit = QtWidgets.QLineEdit(Dialog)
        # self.lineEdit.setGeometry(QtCore.QRect(20, 70, 185, 20))
        # self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(120, 70, 100, 13)) # pos y 100
        self.label_3.setObjectName("label_3")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(120, 90, 69, 22)) # pos y 120
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        # self.lineEdit.setDisabled(True)
        # self.pushButton.setDisabled(True)
        
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore

        # def __cboxce(idx):
        #     if idx == 2:
        #         self.lineEdit.setDisabled(False)
        #         self.pushButton.setDisabled(False)
        #     else:
        #         self.lineEdit.setDisabled(True)
        #         self.pushButton.setDisabled(True)

        # def __pbp():
        #     filedl = QtWidgets.QFileDialog(Dialog)
        #     file = filedl.getOpenFileName(Dialog, "Select image...", None, "Image Files (*.png *.jpg *.bmp)")
        #     self.lineEdit.setText(file[0])

        # self.pushButton.clicked.connect(__pbp)
        # self.comboBox.currentIndexChanged.connect(__cboxce)
        self.comboBox_2.setCurrentIndex(2)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.comboBox.setItemText(0, _translate("Dialog", "None"))
        self.comboBox.setItemText(1, _translate("Dialog", "Minecraft"))
        # self.comboBox.setItemText(2, _translate("Dialog", "Custom"))
        self.label.setText(_translate("Dialog", "Background:"))
        self.label_2.setText(_translate("Dialog", "Number of cells:"))
        # self.pushButton.setText(_translate("Dialog", "Browse..."))
        self.label_3.setText(_translate("Dialog", "Cell Resolution:"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "16"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "24"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "32"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "48"))
        self.comboBox_2.setItemText(4, _translate("Dialog", "64"))

app = QtWidgets.QApplication([])
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)

def Accept():
    cells = ui.spinBox.value()
    cell_sz = int(ui.comboBox_2.currentText())
    if ui.comboBox.currentIndex() == 1:
        bg = True
    else:
        bg = False

    import main
    Dialog.hide()
    main.RunGame(cells, cell_sz, bg)
    app.exit()

Dialog.accept = Accept
Dialog.show()
app.exec_()
