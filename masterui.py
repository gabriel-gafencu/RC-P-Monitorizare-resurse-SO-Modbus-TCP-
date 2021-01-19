from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QPieSeries, QChart, QChartView
from PyQt5.QtWidgets import QDialog
from QLed import QLed

stylestatus = "QStatusBar{padding-left:8px;background:rgba(255,255,255,0.9);color:black;font-weight:bold;}"


class Ui_Master(object):
    def setupUi(self, Master):
        Master.setObjectName("Master")
        Master.resize(600, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Master.sizePolicy().hasHeightForWidth())
        Master.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(Master)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_g = QtWidgets.QLabel(Master)
        self.label_g.setObjectName("label_g")
        self.gridLayout_2.addWidget(self.label_g, 0, 1, 1, 1)
        self.frame = QtWidgets.QFrame(Master)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.cpu_btn = QtWidgets.QPushButton(self.frame)
        self.cpu_btn.setObjectName("cpu_btn")
        self.gridLayout.addWidget(self.cpu_btn, 0, 0, 1, 1)
        self.memory_btn = QtWidgets.QPushButton(self.frame)
        self.memory_btn.setObjectName("memory_btn")
        self.gridLayout.addWidget(self.memory_btn, 1, 0, 1, 1)
        self.disk_btn = QtWidgets.QPushButton(self.frame)
        self.disk_btn.setObjectName("disk_btn")
        self.gridLayout.addWidget(self.disk_btn, 2, 0, 1, 1)
        self.login = QtWidgets.QPushButton(self.frame)
        self.login.setObjectName("login")
        self.gridLayout.addWidget(self.login, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 3, 1)
        self.graphicsView = QChartView(Master)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 1, 1, 1, 1)
        self.label_s = QtWidgets.QLabel(Master)
        self.label_s.setObjectName("label_s")
        self.gridLayout_2.addWidget(self.label_s, 2, 1, 1, 1)
        self.status = QtWidgets.QStatusBar(Master)
        self.status.setObjectName("status")
        self.status.setStyleSheet(stylestatus)
        self.status.showMessage("hello ")
        self.led = QLed(Master, onColour=QLed.Green, shape=QLed.Circle)
        self.led.setFixedSize(30, 30)
        self.led.value = False
        self.gridLayout.addWidget(self.led, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.status, 3, 1, 1, 1)

        self.retranslateUi(Master)
        QtCore.QMetaObject.connectSlotsByName(Master)

    def retranslateUi(self, Master):
        _translate = QtCore.QCoreApplication.translate
        Master.setWindowTitle(_translate("Master", "Master"))
        self.label_g.setText(_translate("Master", "Graphics:"))
        self.cpu_btn.setText(_translate("Master", "CPU"))
        self.memory_btn.setText(_translate("Master", "Memory"))
        self.disk_btn.setText(_translate("Master", "Disk usage"))
        self.login.setText(_translate("Master", "Login"))
        self.label_s.setText(_translate("Master", "Status:"))

# doar pentru verificarea interfetei
'''class  MainMaster(QDialog):
    def __init__(self):
        super(MainMaster,self).__init__()
        ui = Ui_Master()
        ui.setupUi(self)
        self.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mm=MainMaster()
    sys.exit(app.exec_())'''
