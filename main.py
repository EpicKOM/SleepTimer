# Coding : UTF-8
# Author : EpicKOM

# ------Import Modules -------------------------------------------------------------------------------------------------

import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from countdownscreen import Ui_CountdownTimer
from homescreen import Ui_HomeScreen
from edittimerscreen import Ui_EditTimerScreen

# ------Custom Color ---------------------------------------------------------------------------------------------------
"""
You can modify theme color by changing the RGB code below.

Examples : 

Blue(default): RGB = [57, 192, 237]
Green: RGB = [0, 183, 74]
Pink: RGB = [255, 0, 127]
"""

RGB = [57, 192, 237]

# ----------------------------------------------------------------------------------------------------------------------


class HomeScreenWindow(QtWidgets.QMainWindow, Ui_HomeScreen):
    def __init__(self, edit_timer):
        super(HomeScreenWindow, self).__init__()
        self.setupUi(self)
        self.edit_timer = edit_timer
        self.total_time = self.edit_timer.total
        self.Select_Time_Button.clicked.connect(self.edit_time)
        self.Start_Button.clicked.connect(self.run)
        self.custom_screen()

    def custom_screen(self):
        _translate = QtCore.QCoreApplication.translate
        self.Select_Time_Label.setStyleSheet("QLabel{\n"
                                             f"    color: rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                             "}")
        self.StartButtonBase.setStyleSheet("QFrame{\n"
                                           f"    border: 4px solid rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                           "    border-radius: 35px;\n"
                                           "    background-color: rgb(80, 80, 80);\n"
                                           "}")
        quotient, second = divmod(self.total_time, 60)
        hour, minute = divmod(quotient, 60)
        self.Select_Time_Label.setText(_translate("HomeScreen", f"<strong>{hour:02d} : {minute:02d} : {second:02d}</strong>"))

    def edit_time(self):
        widget.setWindowTitle("SleepTimer - Edit Timer")
        edittimerscreen = EditTimerWindow(self)
        widget.addWidget(edittimerscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def run(self):
        widget.setWindowTitle("SleepTimer - Running")
        countdown_screen = CountdownWindow(self)
        widget.addWidget(countdown_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)


class EditTimerWindow(QtWidgets.QMainWindow, Ui_EditTimerScreen):
    def __init__(self, *args, **kwargs):
        super(EditTimerWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.custom_screen()
        self.Valid_Button.clicked.connect(self.edit_time)
        if len(memory) < 1:
            self.total = 1800
        else:
            self.total = memory[0]
        self.update_date_edit()

    def custom_screen(self):
        self.Hours_spinBox.setStyleSheet("QSpinBox{\n"
                                         f"    border: 2px solid rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                         "    border-top-left-radius: 8px;\n"
                                         "    border-bottom-left-radius: 8px;\n"
                                         f"    color: rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                         "    padding-left: 55px;\n"
                                         "}")

        self.Minutes_spinBox.setStyleSheet("QSpinBox{\n"
                                           f"    border: 2px solid rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                           "    border-top-left-radius: 8px;\n"
                                           "    border-bottom-left-radius: 8px;\n"
                                           f"    color: rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                           "    padding-left: 55px;\n"
                                           "}")

        self.Seconds_spinBox.setStyleSheet("QSpinBox{\n"
                                           f"    border: 2px solid rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                           "    border-top-left-radius: 8px;\n"
                                           "    border-bottom-left-radius: 8px;\n"
                                           f"    color: rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                           "    padding-left: 55px;\n"
                                           "}")

        self.ValidButtonBase.setStyleSheet("QFrame{\n"
                                           f"    border: 4px solid rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                           "    border-radius: 35px;\n"
                                           "    background-color: rgb(80, 80, 80);\n"
                                           "}")

    def update_date_edit(self):
        quotient, second = divmod(self.total, 60)
        hour, minute = divmod(quotient, 60)
        self.Hours_spinBox.setProperty("value", hour)
        self.Minutes_spinBox.setProperty("value", minute)
        self.Seconds_spinBox.setProperty("value", second)

    def edit_time(self):
        widget.setWindowTitle("SleepTimer")
        hrs_in_secs = self.Hours_spinBox.value() * 3600
        mins_in_secs = self.Minutes_spinBox.value() * 60
        secs = self.Seconds_spinBox.value()
        self.total = hrs_in_secs + mins_in_secs + secs
        if len(memory) < 1:
            memory.append(self.total)
        else:
            del memory[0]
            memory.append(self.total)
        home_screen = HomeScreenWindow(self)
        widget.addWidget(home_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CountdownWindow(QtWidgets.QMainWindow, Ui_CountdownTimer):
    def __init__(self, selectwindow):
        super(CountdownWindow, self).__init__()
        self.setupUi(self)
        self.selectwindow = selectwindow
        self.custom_screen()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.countdown)
        self.total_time = self.selectwindow.total_time
        self.current_time = self.total_time
        self.Stop_Button.clicked.connect(self.stop)
        self.countdown()
        self.start()

    def custom_screen(self):
        self.StopButtonBase.setStyleSheet("QFrame{\n"
                                          f"    border: 4px solid rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                          "    border-radius: 35px;\n"
                                          "    background-color: rgb(80, 80, 80);\n"
                                          "}")

        self.PauseButtonBase.setStyleSheet("QFrame{\n"
                                           f"    border: 4px solid rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                           "    border-radius: 35px;\n"
                                           "    background-color: rgb(80, 80, 80);\n"
                                           "}")

    def start(self):
        self.Pause_Button.disconnect()
        widget.setWindowTitle("SleepTimer - Running")
        _translate = QtCore.QCoreApplication.translate
        quotient, second = divmod(self.total_time, 60)
        hour, minute = divmod(quotient, 60)
        self.Total_Time_Label.setText(_translate("SleepTimerGUI",
                                                 f"<html><head/><body><p><span style=\" font-weight:600; color:rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\">TOTAL:</span> {hour:02d} : {minute:02d} : {second:02d}</p></body></html>"))
        self.timer.start(1000)
        self.Pause_Button_Label.setPixmap(QtGui.QPixmap("img/pause.png"))
        self.Pause_Button_Label.setGeometry(QtCore.QRect(16, 16, 38, 39))
        self.Pause_Button.clicked.connect(self.pause)

    def pause(self):
        self.Pause_Button.disconnect()
        widget.setWindowTitle("SleepTimer - Pause")
        self.Pause_Button_Label.setPixmap(QtGui.QPixmap("img/play.png"))
        self.Pause_Button_Label.setGeometry(QtCore.QRect(17, 14, 38, 42))
        self.timer.stop()
        self.Pause_Button.clicked.connect(self.start)

    def shutdown(self):
        _translate = QtCore.QCoreApplication.translate
        self.Time_Percent.setText(_translate("SleepTimerGUI",
                                             "<p><span style=\" font-size:25pt;\">100</span><span style=\" font-size:19pt; vertical-align:super;\">%</span></p>"))
        self.CircularProgress.setStyleSheet("QFrame{\n"
                                            "    border-radius: 150px;\n"
                                            f"background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:1.0 rgba({RGB[0]}, {RGB[1]}, {RGB[2]}, 255), stop:1.0 rgba(255, 255, 255, 0));\n"
                                            "}")
        self.Time_Label.setText(_translate("SleepTimerGUI", "<strong>00 : 00 : 00</strong>"))
        os.system("shutdown.exe -s -t 5")

    def upgrade_progressbar(self):
        _translate = QtCore.QCoreApplication.translate
        percent = 100-(self.current_time * 100)/self.total_time
        percent_round = round(percent)
        self.Time_Percent.setText(_translate("SleepTimerGUI",
                                             f"<p><span style=\" font-size:25pt;\">{percent_round}</span><span style=\" font-size:19pt; vertical-align:super;\">%</span></p>"))
        self.Time_Percent.setStyleSheet("QLabel{\n"
                                        f"    color: rgb({RGB[0]}, {RGB[1]}, {RGB[2]});\n"
                                        "    background-color: none;\n"
                                        "}")
        gradient_color_coef1 = percent/100
        gradient_color_coef2 = gradient_color_coef1 - 0.001
        self.CircularProgress.setStyleSheet("QFrame{\n"
                                            "    border-radius: 150px;\n"
                                            f"background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{gradient_color_coef1} rgba({RGB[0]}, {RGB[1]}, {RGB[2]}, 255), stop:{gradient_color_coef2} rgba(255, 255, 255, 0));\n"
                                            "}")
        quotient, second = divmod(self.current_time, 60)
        hour, minute = divmod(quotient, 60)
        self.Time_Label.setText(_translate("SleepTimerGUI", f"<strong>{hour:02d} : {minute:02d} : {second:02d}</strong>"))

    def countdown(self):
        self.upgrade_progressbar()
        self.current_time -= 1

        if self.current_time < 0:
            self.timer.stop()
            self.shutdown()

    def stop(self):
        self.timer.stop()
        if len(memory) < 1:
            memory.append(self.total_time)
        else:
            del memory[0]
            memory.append(self.total_time)
        widget.setWindowTitle("SleepTimer")
        home_screen = HomeScreenWindow(EditTimerWindow())
        widget.addWidget(home_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


memory = []

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
window = HomeScreenWindow(EditTimerWindow())
widget.addWidget(window)
widget.setWindowTitle("SleepTimer")
widget.setWindowIcon(QtGui.QIcon('img/icon.png'))
widget.setFixedSize(430, 550)
widget.show()
app.exec()
