# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 926)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabDivination = QWidget()
        self.tabDivination.setObjectName(u"tabDivination")
        self.widget = QWidget(self.tabDivination)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 110, 1182, 678))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupInputMode = QGroupBox(self.widget)
        self.groupInputMode.setObjectName(u"groupInputMode")
        self.groupInputMode.setEnabled(True)
        self.groupInputMode.setMinimumSize(QSize(5, 100))
        self.groupInputMode.setMaximumSize(QSize(1164, 100))
        self.groupInputMode.setFlat(False)
        self.layoutWidget = QWidget(self.groupInputMode)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(80, 10, 353, 81))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.rbSixLines = QRadioButton(self.layoutWidget)
        self.rbSixLines.setObjectName(u"rbSixLines")
        self.rbSixLines.setChecked(True)

        self.horizontalLayout.addWidget(self.rbSixLines)

        self.rbHexagramName = QRadioButton(self.layoutWidget)
        self.rbHexagramName.setObjectName(u"rbHexagramName")

        self.horizontalLayout.addWidget(self.rbHexagramName)

        self.rbHexagramNumber = QRadioButton(self.layoutWidget)
        self.rbHexagramNumber.setObjectName(u"rbHexagramNumber")

        self.horizontalLayout.addWidget(self.rbHexagramNumber)

        self.rbTrigrams = QRadioButton(self.layoutWidget)
        self.rbTrigrams.setObjectName(u"rbTrigrams")

        self.horizontalLayout.addWidget(self.rbTrigrams)


        self.verticalLayout_2.addWidget(self.groupInputMode)

        self.groupLinesInput = QGroupBox(self.widget)
        self.groupLinesInput.setObjectName(u"groupLinesInput")
        self.groupLinesInput.setMaximumSize(QSize(16777215, 500))
        self.horizontalLayoutWidget = QWidget(self.groupLinesInput)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 40, 661, 51))
        self.groupLine6 = QHBoxLayout(self.horizontalLayoutWidget)
        self.groupLine6.setObjectName(u"groupLine6")
        self.groupLine6.setContentsMargins(10, 0, 0, 0)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")

        self.groupLine6.addWidget(self.label)

        self.rb6YoungYang = QPushButton(self.horizontalLayoutWidget)
        self.rb6YoungYang.setObjectName(u"rb6YoungYang")
        self.rb6YoungYang.setCheckable(True)

        self.groupLine6.addWidget(self.rb6YoungYang)

        self.rb6YoungYin = QPushButton(self.horizontalLayoutWidget)
        self.rb6YoungYin.setObjectName(u"rb6YoungYin")
        self.rb6YoungYin.setCheckable(True)

        self.groupLine6.addWidget(self.rb6YoungYin)

        self.rb6OldYang = QPushButton(self.horizontalLayoutWidget)
        self.rb6OldYang.setObjectName(u"rb6OldYang")
        self.rb6OldYang.setCheckable(True)

        self.groupLine6.addWidget(self.rb6OldYang)

        self.rb6OldYin = QPushButton(self.horizontalLayoutWidget)
        self.rb6OldYin.setObjectName(u"rb6OldYin")
        self.rb6OldYin.setCheckable(True)

        self.groupLine6.addWidget(self.rb6OldYin)

        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.groupLine6.addWidget(self.label_2)

        self.horizontalLayoutWidget_2 = QWidget(self.groupLinesInput)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 100, 661, 51))
        self.groupLine5 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.groupLine5.setObjectName(u"groupLine5")
        self.groupLine5.setContentsMargins(10, 0, 0, 0)
        self.label_3 = QLabel(self.horizontalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.groupLine5.addWidget(self.label_3)

        self.rb5YoungYang = QPushButton(self.horizontalLayoutWidget_2)
        self.rb5YoungYang.setObjectName(u"rb5YoungYang")
        self.rb5YoungYang.setCheckable(True)

        self.groupLine5.addWidget(self.rb5YoungYang)

        self.rb5YoungYin = QPushButton(self.horizontalLayoutWidget_2)
        self.rb5YoungYin.setObjectName(u"rb5YoungYin")
        self.rb5YoungYin.setCheckable(True)

        self.groupLine5.addWidget(self.rb5YoungYin)

        self.rb5OldYang = QPushButton(self.horizontalLayoutWidget_2)
        self.rb5OldYang.setObjectName(u"rb5OldYang")
        self.rb5OldYang.setCheckable(True)

        self.groupLine5.addWidget(self.rb5OldYang)

        self.rb5OldYin = QPushButton(self.horizontalLayoutWidget_2)
        self.rb5OldYin.setObjectName(u"rb5OldYin")
        self.rb5OldYin.setCheckable(True)

        self.groupLine5.addWidget(self.rb5OldYin)

        self.label_4 = QLabel(self.horizontalLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.groupLine5.addWidget(self.label_4)

        self.horizontalLayoutWidget_3 = QWidget(self.groupLinesInput)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 160, 661, 51))
        self.groupLine4 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.groupLine4.setObjectName(u"groupLine4")
        self.groupLine4.setContentsMargins(10, 0, 0, 0)
        self.label_5 = QLabel(self.horizontalLayoutWidget_3)
        self.label_5.setObjectName(u"label_5")

        self.groupLine4.addWidget(self.label_5)

        self.rb4YoungYang = QPushButton(self.horizontalLayoutWidget_3)
        self.rb4YoungYang.setObjectName(u"rb4YoungYang")
        self.rb4YoungYang.setCheckable(True)

        self.groupLine4.addWidget(self.rb4YoungYang)

        self.rb4YoungYin = QPushButton(self.horizontalLayoutWidget_3)
        self.rb4YoungYin.setObjectName(u"rb4YoungYin")
        self.rb4YoungYin.setCheckable(True)

        self.groupLine4.addWidget(self.rb4YoungYin)

        self.rb4OldYang = QPushButton(self.horizontalLayoutWidget_3)
        self.rb4OldYang.setObjectName(u"rb4OldYang")
        self.rb4OldYang.setCheckable(True)

        self.groupLine4.addWidget(self.rb4OldYang)

        self.rb4OldYin = QPushButton(self.horizontalLayoutWidget_3)
        self.rb4OldYin.setObjectName(u"rb4OldYin")
        self.rb4OldYin.setCheckable(True)

        self.groupLine4.addWidget(self.rb4OldYin)

        self.label_6 = QLabel(self.horizontalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")

        self.groupLine4.addWidget(self.label_6)

        self.horizontalLayoutWidget_4 = QWidget(self.groupLinesInput)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(10, 220, 661, 51))
        self.groupLine3 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.groupLine3.setObjectName(u"groupLine3")
        self.groupLine3.setContentsMargins(10, 0, 0, 0)
        self.label_7 = QLabel(self.horizontalLayoutWidget_4)
        self.label_7.setObjectName(u"label_7")

        self.groupLine3.addWidget(self.label_7)

        self.rb3YoungYang = QPushButton(self.horizontalLayoutWidget_4)
        self.rb3YoungYang.setObjectName(u"rb3YoungYang")
        self.rb3YoungYang.setCheckable(True)

        self.groupLine3.addWidget(self.rb3YoungYang)

        self.rb3YoungYin = QPushButton(self.horizontalLayoutWidget_4)
        self.rb3YoungYin.setObjectName(u"rb3YoungYin")
        self.rb3YoungYin.setCheckable(True)

        self.groupLine3.addWidget(self.rb3YoungYin)

        self.rb3OldYang = QPushButton(self.horizontalLayoutWidget_4)
        self.rb3OldYang.setObjectName(u"rb3OldYang")
        self.rb3OldYang.setCheckable(True)

        self.groupLine3.addWidget(self.rb3OldYang)

        self.rb3OldYin = QPushButton(self.horizontalLayoutWidget_4)
        self.rb3OldYin.setObjectName(u"rb3OldYin")
        self.rb3OldYin.setCheckable(True)

        self.groupLine3.addWidget(self.rb3OldYin)

        self.label_8 = QLabel(self.horizontalLayoutWidget_4)
        self.label_8.setObjectName(u"label_8")

        self.groupLine3.addWidget(self.label_8)

        self.horizontalLayoutWidget_5 = QWidget(self.groupLinesInput)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(10, 280, 661, 51))
        self.groupLine2 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.groupLine2.setObjectName(u"groupLine2")
        self.groupLine2.setContentsMargins(10, 0, 0, 0)
        self.label_9 = QLabel(self.horizontalLayoutWidget_5)
        self.label_9.setObjectName(u"label_9")

        self.groupLine2.addWidget(self.label_9)

        self.rb2YoungYang = QPushButton(self.horizontalLayoutWidget_5)
        self.rb2YoungYang.setObjectName(u"rb2YoungYang")
        self.rb2YoungYang.setCheckable(True)

        self.groupLine2.addWidget(self.rb2YoungYang)

        self.rb2YoungYin = QPushButton(self.horizontalLayoutWidget_5)
        self.rb2YoungYin.setObjectName(u"rb2YoungYin")
        self.rb2YoungYin.setCheckable(True)

        self.groupLine2.addWidget(self.rb2YoungYin)

        self.rb2OldYang = QPushButton(self.horizontalLayoutWidget_5)
        self.rb2OldYang.setObjectName(u"rb2OldYang")
        self.rb2OldYang.setCheckable(True)

        self.groupLine2.addWidget(self.rb2OldYang)

        self.rb2OldYin = QPushButton(self.horizontalLayoutWidget_5)
        self.rb2OldYin.setObjectName(u"rb2OldYin")
        self.rb2OldYin.setCheckable(True)

        self.groupLine2.addWidget(self.rb2OldYin)

        self.label_10 = QLabel(self.horizontalLayoutWidget_5)
        self.label_10.setObjectName(u"label_10")

        self.groupLine2.addWidget(self.label_10)

        self.horizontalLayoutWidget_6 = QWidget(self.groupLinesInput)
        self.horizontalLayoutWidget_6.setObjectName(u"horizontalLayoutWidget_6")
        self.horizontalLayoutWidget_6.setGeometry(QRect(10, 340, 661, 51))
        self.groupLine1 = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.groupLine1.setObjectName(u"groupLine1")
        self.groupLine1.setContentsMargins(10, 0, 0, 0)
        self.label_11 = QLabel(self.horizontalLayoutWidget_6)
        self.label_11.setObjectName(u"label_11")

        self.groupLine1.addWidget(self.label_11)

        self.rb1YoungYang = QPushButton(self.horizontalLayoutWidget_6)
        self.rb1YoungYang.setObjectName(u"rb1YoungYang")
        self.rb1YoungYang.setCheckable(True)

        self.groupLine1.addWidget(self.rb1YoungYang)

        self.rb1YoungYin = QPushButton(self.horizontalLayoutWidget_6)
        self.rb1YoungYin.setObjectName(u"rb1YoungYin")
        self.rb1YoungYin.setCheckable(True)

        self.groupLine1.addWidget(self.rb1YoungYin)

        self.rb1OldYang = QPushButton(self.horizontalLayoutWidget_6)
        self.rb1OldYang.setObjectName(u"rb1OldYang")
        self.rb1OldYang.setCheckable(True)

        self.groupLine1.addWidget(self.rb1OldYang)

        self.rb1OldYin = QPushButton(self.horizontalLayoutWidget_6)
        self.rb1OldYin.setObjectName(u"rb1OldYin")
        self.rb1OldYin.setCheckable(True)

        self.groupLine1.addWidget(self.rb1OldYin)

        self.label_12 = QLabel(self.horizontalLayoutWidget_6)
        self.label_12.setObjectName(u"label_12")

        self.groupLine1.addWidget(self.label_12)


        self.verticalLayout_2.addWidget(self.groupLinesInput)

        self.horizontalLayoutWidget_7 = QWidget(self.tabDivination)
        self.horizontalLayoutWidget_7.setObjectName(u"horizontalLayoutWidget_7")
        self.horizontalLayoutWidget_7.setGeometry(QRect(10, 40, 481, 80))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_13 = QLabel(self.horizontalLayoutWidget_7)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_2.addWidget(self.label_13)

        self.editQuestion = QLineEdit(self.horizontalLayoutWidget_7)
        self.editQuestion.setObjectName(u"editQuestion")

        self.horizontalLayout_2.addWidget(self.editQuestion)

        self.tabWidget.addTab(self.tabDivination, "")
        self.tab_interpretation = QWidget()
        self.tab_interpretation.setObjectName(u"tab_interpretation")
        self.verticalLayoutInterpretation = QVBoxLayout(self.tab_interpretation)
        self.verticalLayoutInterpretation.setObjectName(u"verticalLayoutInterpretation")
        self.formInfo = QFormLayout()
        self.formInfo.setObjectName(u"formInfo")
        self.label_lblMainName = QLabel(self.tab_interpretation)
        self.label_lblMainName.setObjectName(u"label_lblMainName")

        self.formInfo.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_lblMainName)

        self.lblMainName = QLabel(self.tab_interpretation)
        self.lblMainName.setObjectName(u"lblMainName")

        self.formInfo.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lblMainName)

        self.label_lblMainNumber = QLabel(self.tab_interpretation)
        self.label_lblMainNumber.setObjectName(u"label_lblMainNumber")

        self.formInfo.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_lblMainNumber)

        self.lblMainNumber = QLabel(self.tab_interpretation)
        self.lblMainNumber.setObjectName(u"lblMainNumber")

        self.formInfo.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lblMainNumber)

        self.label_lblChangedName = QLabel(self.tab_interpretation)
        self.label_lblChangedName.setObjectName(u"label_lblChangedName")

        self.formInfo.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_lblChangedName)

        self.lblChangedName = QLabel(self.tab_interpretation)
        self.lblChangedName.setObjectName(u"lblChangedName")

        self.formInfo.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lblChangedName)

        self.label_lblChangedNumber = QLabel(self.tab_interpretation)
        self.label_lblChangedNumber.setObjectName(u"label_lblChangedNumber")

        self.formInfo.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_lblChangedNumber)

        self.lblChangedNumber = QLabel(self.tab_interpretation)
        self.lblChangedNumber.setObjectName(u"lblChangedNumber")

        self.formInfo.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lblChangedNumber)

        self.label_lblMovingLines = QLabel(self.tab_interpretation)
        self.label_lblMovingLines.setObjectName(u"label_lblMovingLines")

        self.formInfo.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_lblMovingLines)

        self.lblMovingLines = QLabel(self.tab_interpretation)
        self.lblMovingLines.setObjectName(u"lblMovingLines")

        self.formInfo.setWidget(4, QFormLayout.ItemRole.FieldRole, self.lblMovingLines)


        self.verticalLayoutInterpretation.addLayout(self.formInfo)

        self.grp_txtJudgment = QGroupBox(self.tab_interpretation)
        self.grp_txtJudgment.setObjectName(u"grp_txtJudgment")
        self.layout_txtJudgment = QVBoxLayout(self.grp_txtJudgment)
        self.layout_txtJudgment.setObjectName(u"layout_txtJudgment")
        self.txtJudgment = QPlainTextEdit(self.grp_txtJudgment)
        self.txtJudgment.setObjectName(u"txtJudgment")

        self.layout_txtJudgment.addWidget(self.txtJudgment)


        self.verticalLayoutInterpretation.addWidget(self.grp_txtJudgment)

        self.grp_txtTuan = QGroupBox(self.tab_interpretation)
        self.grp_txtTuan.setObjectName(u"grp_txtTuan")
        self.layout_txtTuan = QVBoxLayout(self.grp_txtTuan)
        self.layout_txtTuan.setObjectName(u"layout_txtTuan")
        self.txtTuan = QPlainTextEdit(self.grp_txtTuan)
        self.txtTuan.setObjectName(u"txtTuan")

        self.layout_txtTuan.addWidget(self.txtTuan)


        self.verticalLayoutInterpretation.addWidget(self.grp_txtTuan)

        self.grp_txtXiang = QGroupBox(self.tab_interpretation)
        self.grp_txtXiang.setObjectName(u"grp_txtXiang")
        self.layout_txtXiang = QVBoxLayout(self.grp_txtXiang)
        self.layout_txtXiang.setObjectName(u"layout_txtXiang")
        self.txtXiang = QPlainTextEdit(self.grp_txtXiang)
        self.txtXiang.setObjectName(u"txtXiang")

        self.layout_txtXiang.addWidget(self.txtXiang)


        self.verticalLayoutInterpretation.addWidget(self.grp_txtXiang)

        self.grp_txtWenyan = QGroupBox(self.tab_interpretation)
        self.grp_txtWenyan.setObjectName(u"grp_txtWenyan")
        self.layout_txtWenyan = QVBoxLayout(self.grp_txtWenyan)
        self.layout_txtWenyan.setObjectName(u"layout_txtWenyan")
        self.txtWenyan = QPlainTextEdit(self.grp_txtWenyan)
        self.txtWenyan.setObjectName(u"txtWenyan")

        self.layout_txtWenyan.addWidget(self.txtWenyan)


        self.verticalLayoutInterpretation.addWidget(self.grp_txtWenyan)

        self.grp_txtTranslation = QGroupBox(self.tab_interpretation)
        self.grp_txtTranslation.setObjectName(u"grp_txtTranslation")
        self.layout_txtTranslation = QVBoxLayout(self.grp_txtTranslation)
        self.layout_txtTranslation.setObjectName(u"layout_txtTranslation")
        self.txtTranslation = QPlainTextEdit(self.grp_txtTranslation)
        self.txtTranslation.setObjectName(u"txtTranslation")

        self.layout_txtTranslation.addWidget(self.txtTranslation)


        self.verticalLayoutInterpretation.addWidget(self.grp_txtTranslation)

        self.grp_txtAIAnalysis = QGroupBox(self.tab_interpretation)
        self.grp_txtAIAnalysis.setObjectName(u"grp_txtAIAnalysis")
        self.layout_txtAIAnalysis = QVBoxLayout(self.grp_txtAIAnalysis)
        self.layout_txtAIAnalysis.setObjectName(u"layout_txtAIAnalysis")
        self.txtAIAnalysis = QPlainTextEdit(self.grp_txtAIAnalysis)
        self.txtAIAnalysis.setObjectName(u"txtAIAnalysis")

        self.layout_txtAIAnalysis.addWidget(self.txtAIAnalysis)


        self.verticalLayoutInterpretation.addWidget(self.grp_txtAIAnalysis)

        self.grp_txtNotes = QGroupBox(self.tab_interpretation)
        self.grp_txtNotes.setObjectName(u"grp_txtNotes")
        self.layout_txtNotes = QVBoxLayout(self.grp_txtNotes)
        self.layout_txtNotes.setObjectName(u"layout_txtNotes")
        self.txtNotes = QPlainTextEdit(self.grp_txtNotes)
        self.txtNotes.setObjectName(u"txtNotes")

        self.layout_txtNotes.addWidget(self.txtNotes)


        self.verticalLayoutInterpretation.addWidget(self.grp_txtNotes)

        self.tabWidget.addTab(self.tab_interpretation, "")
        self.tab_history = QWidget()
        self.tab_history.setObjectName(u"tab_history")
        self.verticalLayoutWidget = QWidget(self.tab_history)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, -1, 1161, 831))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.listHistory = QListWidget(self.verticalLayoutWidget)
        self.listHistory.setObjectName(u"listHistory")

        self.verticalLayout_3.addWidget(self.listHistory)

        self.tabWidget.addTab(self.tab_history, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u6613\u7d93\u5360\u535c\u7cfb\u7d71", None))
        self.groupInputMode.setTitle(QCoreApplication.translate("MainWindow", u"\u8f38\u5165\u6a21\u5f0f", None))
        self.rbSixLines.setText(QCoreApplication.translate("MainWindow", u"\u516d\u723b\u8f38\u5165", None))
        self.rbHexagramName.setText(QCoreApplication.translate("MainWindow", u"\u5366\u540d", None))
        self.rbHexagramNumber.setText(QCoreApplication.translate("MainWindow", u"\u5366\u5e8f", None))
        self.rbTrigrams.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4e0b\u5366", None))
        self.groupLinesInput.setTitle(QCoreApplication.translate("MainWindow", u"\u516d\u723b\u8f38\u5165", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u723b", None))
        self.rb6YoungYang.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u967d", None))
        self.rb6YoungYin.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u9670", None))
        self.rb6OldYang.setText(QCoreApplication.translate("MainWindow", u"\u8001\u967d", None))
        self.rb6OldYin.setText(QCoreApplication.translate("MainWindow", u"\u8001\u9670", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u4e00", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4e94\u723b", None))
        self.rb5YoungYang.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u967d", None))
        self.rb5YoungYin.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u9670", None))
        self.rb5OldYang.setText(QCoreApplication.translate("MainWindow", u"\u8001\u967d", None))
        self.rb5OldYin.setText(QCoreApplication.translate("MainWindow", u"\u8001\u9670", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u4e00", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u56db\u723b", None))
        self.rb4YoungYang.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u967d", None))
        self.rb4YoungYin.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u9670", None))
        self.rb4OldYang.setText(QCoreApplication.translate("MainWindow", u"\u8001\u967d", None))
        self.rb4OldYin.setText(QCoreApplication.translate("MainWindow", u"\u8001\u9670", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u4e00", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u4e09\u723b", None))
        self.rb3YoungYang.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u967d", None))
        self.rb3YoungYin.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u9670", None))
        self.rb3OldYang.setText(QCoreApplication.translate("MainWindow", u"\u8001\u967d", None))
        self.rb3OldYin.setText(QCoreApplication.translate("MainWindow", u"\u8001\u9670", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u4e00", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u723b", None))
        self.rb2YoungYang.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u967d", None))
        self.rb2YoungYin.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u9670", None))
        self.rb2OldYang.setText(QCoreApplication.translate("MainWindow", u"\u8001\u967d", None))
        self.rb2OldYin.setText(QCoreApplication.translate("MainWindow", u"\u8001\u9670", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u4e00", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u521d\u723b", None))
        self.rb1YoungYang.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u967d", None))
        self.rb1YoungYin.setText(QCoreApplication.translate("MainWindow", u"\u5c11\u9670", None))
        self.rb1OldYang.setText(QCoreApplication.translate("MainWindow", u"\u8001\u967d", None))
        self.rb1OldYin.setText(QCoreApplication.translate("MainWindow", u"\u8001\u9670", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u4e00", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u5360\u535c\u554f\u984c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDivination), QCoreApplication.translate("MainWindow", u"\u8d77\u5366", None))
        self.label_lblMainName.setText(QCoreApplication.translate("MainWindow", u"\u672c\u5366", None))
        self.lblMainName.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_lblMainNumber.setText(QCoreApplication.translate("MainWindow", u"\u672c\u5366\u7de8\u865f", None))
        self.lblMainNumber.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_lblChangedName.setText(QCoreApplication.translate("MainWindow", u"\u8b8a\u5366", None))
        self.lblChangedName.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_lblChangedNumber.setText(QCoreApplication.translate("MainWindow", u"\u8b8a\u5366\u7de8\u865f", None))
        self.lblChangedNumber.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_lblMovingLines.setText(QCoreApplication.translate("MainWindow", u"\u52d5\u723b", None))
        self.lblMovingLines.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.grp_txtJudgment.setTitle(QCoreApplication.translate("MainWindow", u"\u5366\u8fad", None))
        self.grp_txtTuan.setTitle(QCoreApplication.translate("MainWindow", u"\u5f56\u50b3", None))
        self.grp_txtXiang.setTitle(QCoreApplication.translate("MainWindow", u"\u8c61\u50b3", None))
        self.grp_txtWenyan.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u8a00", None))
        self.grp_txtTranslation.setTitle(QCoreApplication.translate("MainWindow", u"\u767d\u8a71\u7ffb\u8b6f", None))
        self.grp_txtAIAnalysis.setTitle(QCoreApplication.translate("MainWindow", u"AI\u5206\u6790", None))
        self.grp_txtNotes.setTitle(QCoreApplication.translate("MainWindow", u"\u6211\u7684\u5fc3\u5f97", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_interpretation), QCoreApplication.translate("MainWindow", u"\u89e3\u5366", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_history), QCoreApplication.translate("MainWindow", u"\u6b77\u53f2\u7d00\u9304", None))
    # retranslateUi

