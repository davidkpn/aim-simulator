from PyQt5 import QtCore, QtGui, QtWidgets
from multiprocessing import Process
import aimbot


class Ui_Dialog(object):

    # Initialize all the ui
    def setupUi(self, Dialog):
        Dialog.setObjectName("AimBot")
        Dialog.resize(400, 300)
        self.fps_label = QtWidgets.QLabel(Dialog)
        self.fps_label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.fps_label.setObjectName("fps_label")


        self.t_check_box = QtWidgets.QCheckBox(Dialog)
        self.t_check_box.setGeometry(QtCore.QRect(10, 70, 41, 17))
        self.t_check_box.setObjectName("t_check_box")


        self.ct_check_box = QtWidgets.QCheckBox(Dialog)
        self.ct_check_box.setGeometry(QtCore.QRect(10, 90, 41, 17))
        self.ct_check_box.setObjectName("ct_check_box")


        self.aim_text_label = QtWidgets.QLabel(Dialog)
        self.aim_text_label.setGeometry(QtCore.QRect(10, 50, 47, 13))
        self.aim_text_label.setObjectName("aim_text_label")


        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(210, 10, 200, 13))
        self.label.setObjectName("label")


        self.run_button = QtWidgets.QPushButton(Dialog)
        self.run_button.setGeometry(QtCore.QRect(160, 260, 75, 23))
        self.run_button.setObjectName("run_button")
        self.run_button.clicked.connect(self.run)


        self.label_pixmap = QtWidgets.QLabel(Dialog)
        pixmap = QtGui.QPixmap('./1.jpg')
        pixmap = pixmap.scaled(300, 280, QtCore.Qt.KeepAspectRatio)
        self.label_pixmap.setPixmap(pixmap)
        self.label_pixmap.move(80,30)

        self.ab = aimbot.AimBot()
        self.running = False
        # Added shortcut - DEL button to stop the program - Need to make it work outside the window
        stop_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), Dialog)
        stop_shortcut.activated.connect(self.run)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # setting the text to the objects
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AimBot"))
        self.fps_label.setText(_translate("Dialog", "Current FPS:"))
        self.t_check_box.setText(_translate("Dialog", "T"))
        self.ct_check_box.setText(_translate("Dialog", "CT"))
        self.aim_text_label.setText(_translate("Dialog", "Aim on:"))
        self.label.setText(_translate("Dialog", "status:"))
        self.run_button.setText(_translate("Dialog", "Run"))


    # Methods
    def run(self):
        t = self.t_check_box.isChecked()
        ct = self.ct_check_box.isChecked()
        if self.running:
            self.ct_check_box.setEnabled(True)
            self.t_check_box.setEnabled(True)
            self.label.setText("status: Stoped")
            self.run_button.setText("Run")
            self.running = False
            self.p.terminate()
            self.p.kill()
            self.p.join()

        else:
            print("Running")
            # handle the checkboxes
            self.ct_check_box.setEnabled(False)
            self.t_check_box.setEnabled(False)
            self.label.setText("status: Runing")
            self.fps_label.setText("Current FPS: {}".format(0))
            self.run_button.setText("Stop")
            self.running = True
            self.p = Process(target=self.ab.run_aimbot, args=(ct,t))
            self.p.start()

        print("T:{}, CT:{}".format(t, ct))
        # p = Process(target=self.ab.run_aimbot, args=('',None))
        # self.p = Process(target=self.ab.run_aimbot, args=())
        # self.p.start()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()

    sys.exit(app.exec_())
