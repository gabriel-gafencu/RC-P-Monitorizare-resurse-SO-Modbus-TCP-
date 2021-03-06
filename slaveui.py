from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog
from QLed import QLed

stylestatus = "QStatusBar{padding-left:8px;background:rgba(255,255,255,0.9);color:black;font-weight:bold;}"


class Ui_Slave(object):
    def setupUi(self, Slave):
        Slave.setObjectName("Slave")
        Slave.resize(600, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Slave.sizePolicy().hasHeightForWidth())
        Slave.setSizePolicy(sizePolicy)
        Slave.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.gridLayout = QtWidgets.QGridLayout(Slave)
        self.gridLayout.setObjectName("gridLayout")
        self.data = QtWidgets.QTabWidget(Slave)
        self.data.setObjectName("data")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tcoils = QtWidgets.QTableWidget(self.tab)
        self.tcoils.setObjectName("tcoils")
        self.tcoils.setColumnCount(2)
        self.tcoils.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tcoils.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tcoils.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tcoils, 0, 0, 1, 1)
        self.data.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tdinp = QtWidgets.QTableWidget(self.tab_2)
        self.tdinp.setObjectName("tdinp")
        self.tdinp.setColumnCount(2)
        self.tdinp.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tdinp.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tdinp.setHorizontalHeaderItem(1, item)
        self.gridLayout_3.addWidget(self.tdinp, 0, 0, 1, 1)
        self.data.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tinreg_2 = QtWidgets.QTableWidget(self.tab_3)
        self.tinreg_2.setObjectName("tinreg_2")
        self.tinreg_2.setColumnCount(2)
        self.tinreg_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tinreg_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tinreg_2.setHorizontalHeaderItem(1, item)
        self.gridLayout_4.addWidget(self.tinreg_2, 0, 0, 1, 1)
        self.data.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tholreg = QtWidgets.QTableWidget(self.tab_4)
        self.tholreg.setObjectName("tholreg")
        self.tholreg.setColumnCount(2)
        self.tholreg.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tholreg.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tholreg.setHorizontalHeaderItem(1, item)
        self.gridLayout_5.addWidget(self.tholreg, 0, 0, 1, 1)
        self.data.addTab(self.tab_4, "")
        self.gridLayout.addWidget(self.data, 0, 0, 1, 1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.led = QLed(Slave, onColour=QLed.Green, shape=QLed.Circle)
        self.led.setFixedSize(30, 30)
        self.led.value = False
        self.verticalLayout.addWidget(self.led)
        self.save_btn = QtWidgets.QPushButton(Slave)
        self.save_btn.setObjectName("save_btn")
        self.verticalLayout.addWidget(self.save_btn)
        self.pushButton = QtWidgets.QPushButton(Slave)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.label_s = QtWidgets.QLabel(Slave)
        self.label_s.setObjectName("label_s")

        self.gridLayout.addWidget(self.label_s, 1, 0, 1, 1)
        self.statusbar = QtWidgets.QStatusBar(Slave)
        self.statusbar.setObjectName("listWidget")
        self.statusbar.setStyleSheet(stylestatus)
        self.gridLayout.addWidget(self.statusbar, 2, 0, 1, 1)

        self.retranslateUi(Slave)
        self.data.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Slave)
        self.pushButton.clicked.connect(self.show_info)

    def retranslateUi(self, Slave):
        _translate = QtCore.QCoreApplication.translate
        Slave.setWindowTitle(_translate("Slave", "Slave"))
        item = self.tcoils.horizontalHeaderItem(0)
        item.setText(_translate("Slave", "address"))
        item = self.tcoils.horizontalHeaderItem(1)
        item.setText(_translate("Slave", "value"))
        self.data.setTabText(self.data.indexOf(self.tab), _translate("Slave", "Coils"))
        item = self.tdinp.horizontalHeaderItem(0)
        item.setText(_translate("Slave", "address"))
        item = self.tdinp.horizontalHeaderItem(1)
        item.setText(_translate("Slave", "value"))
        self.data.setTabText(self.data.indexOf(self.tab_2), _translate("Slave", "Discrete Inputs"))
        item = self.tinreg_2.horizontalHeaderItem(0)
        item.setText(_translate("Slave", "address"))
        item = self.tinreg_2.horizontalHeaderItem(1)
        item.setText(_translate("Slave", "value"))
        self.data.setTabText(self.data.indexOf(self.tab_3), _translate("Slave", "Input Registers"))
        item = self.tholreg.horizontalHeaderItem(0)
        item.setText(_translate("Slave", "address"))
        item = self.tholreg.horizontalHeaderItem(1)
        item.setText(_translate("Slave", "value"))
        self.data.setTabText(self.data.indexOf(self.tab_4), _translate("Slave", "Holding Registers"))
        self.save_btn.setText(_translate("Slave", "Save logfile"))
        self.pushButton.setText(_translate("Slave", "Info"))
        self.label_s.setText(_translate("Slave", "Status:"))


    def show_info(self):
        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setText("Proiect realizat de Ichim Ioana si Gafencu Gabriel")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()



# pentru verificare
'''class MainSlave(QDialog):
    def __init__(self):
        super(MainSlave, self).__init__()
        ui = Ui_Slave()
        ui.setupUi(self)
        self.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ms = MainSlave()
    sys.exit(app.exec_())
'''