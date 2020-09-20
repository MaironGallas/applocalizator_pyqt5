import sys
import os
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
#import win32gui, win32con

# HIDE CONSOLE

# hide_console = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(hide_console , win32con.SW_HIDE)

## MAIN MENU
from crud_db import get_user_db
from ui_login import *
from ui_splash_screen import *
from ui_main_window import Ui_MainWindow

counter = 0


class Login_Menu(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Login_Menu()
        self.ui.setupUi(self)

        ## REMOVE TITLE BAR

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.show()

        ## FUNCTIONS

        def showMessage(message):
            self.ui.frame_error.show()
            self.ui.label_error.setText(message)

        def checkFields():
            textUser = ""
            textPassword = ""

            # CHECK USER
            if not self.ui.text_username.text():
                textUserError = " User Empty. "
            else:
                textUserError = ""

            # CHECK PASSWORD
            if not self.ui.text_password.text():
                textPasswordError = " Password Empty. "
            else:
                textPasswordError = ""

            # CHECK FIELDS
            if textUserError + textPasswordError != '':
                text = textUserError + textPasswordError
                showMessage(text)
            else:
                username = (self.ui.text_username.text())
                password = (self.ui.text_password.text())
                text, username_db, password_db = get_user_db(username)

                user_verify(username, password, username_db, password_db)

        def button_CloseClicked():
            window.close()


        def user_verify(username, password, username_db, password_db):
            if username == username_db and password == password_db:
                self.splash = SplashScreen()
                self.splash.show()
                self.close()
            else:
                text = 'Username or Password Incorrect'
                showMessage(text)

        #HIDE POPUP ERROR
        self.ui.frame_error.hide()

        self.ui.button_close.clicked.connect(button_CloseClicked)
        self.ui.button_login.clicked.connect(checkFields)
        self.ui.text_password.returnPressed.connect(checkFields)

        #CLOSE POPUP ERROR
        self.ui.button_close_popup.clicked.connect(lambda: self.ui.frame_error.hide())


## YOUR APPLICATION
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MAIN WINDOW LABEL
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label.setText("<strong>THANKS</strong> FOR WATCHING"))
        QtCore.QTimer.singleShot(1500, lambda: self.setStyleSheet("background-color: #222; color: #FFF"))

## SPLASH SCREEN
#######################################################################
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        ## UI ==> INTERFACE CODES
        ######################################################################

        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        ## CHANGE DESCRIPTION

        # Initial Text
        self.ui.label_description.setText("<strong>WELCOME</strong> TO HIFL")

        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ##==> APP FUNCTIONS
    ############################################################################
    def progress(self):

        global counter

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREEN AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login_Menu()
    sys.exit(app.exec_())
