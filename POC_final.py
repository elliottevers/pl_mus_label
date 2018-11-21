from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys


class Fret(QFrame):

    fretted = pyqtSignal(bool, name='fretted')

    def __init__(self, parent=None):
        super(Fret, self).__init__(parent=parent)
        self.fretted.connect(self.fret)

    def fret(self, val):
        self.setProperty('Fretted', val)
        self.setStyle(self.style())


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1558, 622)
        Dialog.setStyleSheet("#line, #line_2, #line_3, #line_4, #line_5, #line_6, #line_7, #line_8, #line_9, #line_10, #line_11 {\n"
"    background-color: rgb(107, 126, 140);\n"
"}")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 180, 1333, 84))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Fret1 = Fret(self.horizontalLayoutWidget)
        self.Fret1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret1.setObjectName("Fret1")
        self.Fret1.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret1)
        self.line_11 = Fret(self.horizontalLayoutWidget)
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.horizontalLayout.addWidget(self.line_11)
        self.Fret2 = Fret(self.horizontalLayoutWidget)
        self.Fret2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret2.setObjectName("Fret2")
        self.Fret2.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret2)
        self.line_10 = Fret(self.horizontalLayoutWidget)
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.horizontalLayout.addWidget(self.line_10)
        self.Fret3 = Fret(self.horizontalLayoutWidget)
        self.Fret3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret3.setObjectName("Fret3")
        self.Fret3.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret3)
        self.line_9 = Fret(self.horizontalLayoutWidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.horizontalLayout.addWidget(self.line_9)
        self.Fret4 = Fret(self.horizontalLayoutWidget)
        self.Fret4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret4.setObjectName("Fret4")
        self.Fret4.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret4)
        self.line_8 = Fret(self.horizontalLayoutWidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.horizontalLayout.addWidget(self.line_8)
        self.Fret5 = Fret(self.horizontalLayoutWidget)
        self.Fret5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret5.setObjectName("Fret5")
        self.Fret5.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret5)
        self.line_7 = Fret(self.horizontalLayoutWidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout.addWidget(self.line_7)
        self.Fret6 = Fret(self.horizontalLayoutWidget)
        self.Fret6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret6.setObjectName("Fret6")
        self.Fret6.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret6)
        self.line_6 = Fret(self.horizontalLayoutWidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout.addWidget(self.line_6)
        self.Fret7 = Fret(self.horizontalLayoutWidget)
        self.Fret7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret7.setObjectName("Fret7")
        self.Fret7.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret7)
        self.line_5 = Fret(self.horizontalLayoutWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout.addWidget(self.line_5)
        self.Fret8 = Fret(self.horizontalLayoutWidget)
        self.Fret8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret8.setObjectName("Fret8")
        self.Fret8.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret8)
        self.line_2 = Fret(self.horizontalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.Fret9 = Fret(self.horizontalLayoutWidget)
        self.Fret9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret9.setObjectName("Fret9")
        self.Fret9.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret9)
        self.line = Fret(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.Fret10 = Fret(self.horizontalLayoutWidget)
        self.Fret10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret10.setObjectName("Fret10")
        self.Fret10.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret10)
        self.line_4 = Fret(self.horizontalLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        self.Fret11 = Fret(self.horizontalLayoutWidget)
        self.Fret11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret11.setObjectName("Fret11")
        self.Fret11.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret11)
        self.line_3 = Fret(self.horizontalLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.Fret12 = Fret(self.horizontalLayoutWidget)
        self.Fret12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Fret12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Fret12.setObjectName("Fret12")
        self.Fret12.setStyleSheet('QFrame[Fretted=true] {background-color: rgb(231, 239, 69)}')
        self.horizontalLayout.addWidget(self.Fret12)
        self.FretLabel5 = QtWidgets.QPushButton(Dialog)
        self.FretLabel5.setGeometry(QtCore.QRect(470, 140, 69, 32))
        self.FretLabel5.setObjectName("FretLabel5")
        self.FretLabel7 = QtWidgets.QPushButton(Dialog)
        self.FretLabel7.setGeometry(QtCore.QRect(690, 140, 73, 32))
        self.FretLabel7.setObjectName("FretLabel7")
        self.FretLabel9 = QtWidgets.QPushButton(Dialog)
        self.FretLabel9.setGeometry(QtCore.QRect(910, 140, 79, 32))
        self.FretLabel9.setObjectName("FretLabel9")
        self.FretLabel12 = QtWidgets.QPushButton(Dialog)
        self.FretLabel12.setGeometry(QtCore.QRect(1250, 140, 85, 32))
        self.FretLabel12.setObjectName("FretLabel12")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.FretLabel5.setText(_translate("Dialog", "5"))
        self.FretLabel7.setText(_translate("Dialog", "7"))
        self.FretLabel9.setText(_translate("Dialog", "9"))
        self.FretLabel12.setText(_translate("Dialog", "12"))


class OscServer(QObject):

    def start(self):
            
        def handler_note(*args):

            note_midi = args[1]
            note = note_midi % 12

            ui = fretboard
            frets = [
                ui.Fret8,
                ui.Fret9,
                ui.Fret10,
                ui.Fret11,
                ui.Fret12,
                ui.Fret1,
                ui.Fret2,
                ui.Fret3,
                ui.Fret4,
                ui.Fret5,
                ui.Fret6,
                ui.Fret7
            ]

            ui.Fret1.fretted.emit(True)

            for i, fret in enumerate(frets):
                fret.fretted.emit(True) if i == note else fret.fretted.emit(False)
        
        from pythonosc import dispatcher
        from pythonosc import osc_server

        dispatcher = dispatcher.Dispatcher()

        dispatcher.map("/Note1", handler_note)

        ip = "127.0.0.1"
        
        port = 9990

        server = osc_server.ThreadingOSCUDPServer(
            (ip, port),
            dispatcher
        )

        server.serve_forever()
        
        
class Window(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    fretboard = Ui_Dialog()
    fretboard.setupUi(window)

    server = OscServer()
    thread = QThread()

    server.moveToThread(thread)
    thread.started.connect(server.start)
    thread.start()
    window.show()

    sys.exit(app.exec_())

    