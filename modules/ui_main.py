# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpinBox, QStackedWidget,
    QVBoxLayout, QWidget)
from modules import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 560)
        MainWindow.setMinimumSize(QSize(836, 470))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid #0c79af;\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background-color: rgb"
                        "(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: #0c79af; }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: #0c79af;\n"
"	color: rgb(255, 2"
                        "55, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: #0c79af;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: #0c79af;\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#title"
                        "RightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: #0c79af;\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus *"
                        "/\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: #0c79af;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { backg"
                        "round-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: #0c79af; }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: #0c79af;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* //////////////////////////////////////////////////////////////////"
                        "///////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: #0c79af;\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;"
                        "\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: #0c79af;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: #0c79af;\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:ho"
                        "rizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: #0c79af;\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: "
                        "4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: #0c79af;\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	b"
                        "order-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////"
                        "////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
""
                        "	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: #0c79af;	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: #0c79af;\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
""
                        "QSlider::handle:horizontal:pressed {\n"
"    background-color: #0c79af;\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: #0c79af;\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: #0c79af;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLinkButton {	\n"
"	color: #0c79af;\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, "
                        "60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: #0c79af;\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.Shape.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.bgApp)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.Shape.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy)
        self.leftBox.setFrameShape(QFrame.Shape.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy1)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setBold(True)
        font1.setItalic(False)
        self.titleRightInfo.setFont(font1)
        self.titleRightInfo.setStyleSheet(u"QLabel {\n"
"    font-weight: bold;\n"
"	font-size: 20px;\n"
"}")
        self.titleRightInfo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.Shape.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeAppBtn.setIcon(icon)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font2)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeRestoreAppBtn.setIcon(icon1)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeAppBtn.setIcon(icon2)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.Shape.NoFrame)
        self.content.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.Shape.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.pagesContainer)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"background-image: url(:/images/images/images/PyDracula_vertical.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;")
        self.stackedWidget.addWidget(self.home)
        self.widgets = QWidget()
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.widgets)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.row_1 = QFrame(self.widgets)
        self.row_1.setObjectName(u"row_1")
        self.row_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.row_1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.row_1)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.row_2 = QFrame(self.row_1)
        self.row_2.setObjectName(u"row_2")
        self.row_2.setMinimumSize(QSize(0, 150))
        self.row_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.row_2.setFrameShadow(QFrame.Shadow.Raised)
        self.row_3 = QFrame(self.row_2)
        self.row_3.setObjectName(u"row_3")
        self.row_3.setGeometry(QRect(0, 10, 821, 411))
        self.row_3.setMinimumSize(QSize(0, 150))
        self.row_3.setStyleSheet(u"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1e1e1e;\n"
"    color: #ff79c6;\n"
"    border: 1px solid #444444;\n"
"    selection-background-color: #44475a;\n"
"    selection-color: #ffffff;\n"
"    z-index: 1000;  /* \ub4dc\ub86d\ub2e4\uc6b4\uc774 \ud56d\uc0c1 \uc704\uc5d0 \uc624\ub3c4\ub85d \uc124\uc815 */\n"
"}")
        self.row_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.row_3.setFrameShadow(QFrame.Shadow.Raised)
        self.layoutWidget = QWidget(self.row_3)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(30, 10, 216, 199))
        self.verticalLayout_18 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.labelBoxBlenderInstalation_3 = QLabel(self.layoutWidget)
        self.labelBoxBlenderInstalation_3.setObjectName(u"labelBoxBlenderInstalation_3")
        self.labelBoxBlenderInstalation_3.setFont(font1)
        self.labelBoxBlenderInstalation_3.setStyleSheet(u"QWidget {\n"
"    font-weight: bold;\n"
"	font-size: 20px;\n"
"}\n"
"")

        self.verticalLayout_18.addWidget(self.labelBoxBlenderInstalation_3)

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_4, 0, 2, 1, 1)

        self.b_workspace_height = QDoubleSpinBox(self.layoutWidget)
        self.b_workspace_height.setObjectName(u"b_workspace_height")
        self.b_workspace_height.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.b_workspace_height.setMaximum(1000.000000000000000)

        self.gridLayout_3.addWidget(self.b_workspace_height, 1, 1, 1, 1)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_5, 1, 2, 1, 1)

        self.a_workspace_width = QDoubleSpinBox(self.layoutWidget)
        self.a_workspace_width.setObjectName(u"a_workspace_width")
        self.a_workspace_width.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.a_workspace_width.setMaximum(1000.000000000000000)

        self.gridLayout_3.addWidget(self.a_workspace_width, 0, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)


        self.verticalLayout_17.addLayout(self.gridLayout_3)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)

        self.c_danger_width = QDoubleSpinBox(self.layoutWidget)
        self.c_danger_width.setObjectName(u"c_danger_width")
        self.c_danger_width.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.c_danger_width.setMaximum(1000.000000000000000)

        self.gridLayout_4.addWidget(self.c_danger_width, 0, 1, 1, 1)

        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_7, 0, 2, 1, 1)

        self.label_8 = QLabel(self.layoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)

        self.d_danger_height = QDoubleSpinBox(self.layoutWidget)
        self.d_danger_height.setObjectName(u"d_danger_height")
        self.d_danger_height.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.d_danger_height.setMaximum(1000.000000000000000)

        self.gridLayout_4.addWidget(self.d_danger_height, 1, 1, 1, 1)

        self.label_9 = QLabel(self.layoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_9, 1, 2, 1, 1)


        self.verticalLayout_17.addLayout(self.gridLayout_4)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_10 = QLabel(self.layoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)

        self.e_danger_zone_x = QDoubleSpinBox(self.layoutWidget)
        self.e_danger_zone_x.setObjectName(u"e_danger_zone_x")
        self.e_danger_zone_x.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.e_danger_zone_x.setMaximum(1000.000000000000000)

        self.gridLayout_5.addWidget(self.e_danger_zone_x, 0, 1, 1, 1)

        self.label_11 = QLabel(self.layoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_11, 0, 2, 1, 1)

        self.label_12 = QLabel(self.layoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_12, 1, 0, 1, 1)

        self.f_danger_zone_y = QDoubleSpinBox(self.layoutWidget)
        self.f_danger_zone_y.setObjectName(u"f_danger_zone_y")
        self.f_danger_zone_y.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.f_danger_zone_y.setMaximum(1000.000000000000000)

        self.gridLayout_5.addWidget(self.f_danger_zone_y, 1, 1, 1, 1)

        self.label_13 = QLabel(self.layoutWidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_13, 1, 2, 1, 1)


        self.verticalLayout_17.addLayout(self.gridLayout_5)


        self.verticalLayout_18.addLayout(self.verticalLayout_17)

        self.layoutWidget1 = QWidget(self.row_3)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(34, 230, 517, 109))
        self.gridLayout_2 = QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelBoxBlenderInstalation_4 = QLabel(self.layoutWidget1)
        self.labelBoxBlenderInstalation_4.setObjectName(u"labelBoxBlenderInstalation_4")
        self.labelBoxBlenderInstalation_4.setFont(font1)
        self.labelBoxBlenderInstalation_4.setStyleSheet(u"QWidget {\n"
"    font-weight: bold;\n"
"	font-size: 20px;\n"
"}\n"
"")

        self.gridLayout_2.addWidget(self.labelBoxBlenderInstalation_4, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelBoxBlenderInstalation_14 = QLabel(self.layoutWidget1)
        self.labelBoxBlenderInstalation_14.setObjectName(u"labelBoxBlenderInstalation_14")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labelBoxBlenderInstalation_14.sizePolicy().hasHeightForWidth())
        self.labelBoxBlenderInstalation_14.setSizePolicy(sizePolicy2)
        self.labelBoxBlenderInstalation_14.setFont(font)
        self.labelBoxBlenderInstalation_14.setStyleSheet(u"")
        self.labelBoxBlenderInstalation_14.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.labelBoxBlenderInstalation_14, 1, 0, 1, 2)

        self.j_anchorX = QDoubleSpinBox(self.layoutWidget1)
        self.j_anchorX.setObjectName(u"j_anchorX")
        self.j_anchorX.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.j_anchorX.setMaximum(1000.000000000000000)

        self.gridLayout.addWidget(self.j_anchorX, 1, 6, 1, 1)

        self.h_tagNum = QSpinBox(self.layoutWidget1)
        self.h_tagNum.setObjectName(u"h_tagNum")

        self.gridLayout.addWidget(self.h_tagNum, 0, 4, 1, 2)

        self.i2_tagSelect = QComboBox(self.layoutWidget1)
        self.i2_tagSelect.setObjectName(u"i2_tagSelect")
        self.i2_tagSelect.setStyleSheet(u"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1e1e1e;\n"
"    color: #00B7FF;\n"
"    border: 1px solid #444444;\n"
"    selection-background-color: #44475a;\n"
"    selection-color: #ffffff;\n"
"    z-index: 1000;  /* \ub4dc\ub86d\ub2e4\uc6b4\uc774 \ud56d\uc0c1 \uc704\uc5d0 \uc624\ub3c4\ub85d \uc124\uc815 */\n"
"}")
        self.i2_tagSelect.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.i2_tagSelect, 0, 7, 1, 2)

        self.k_anchorY = QDoubleSpinBox(self.layoutWidget1)
        self.k_anchorY.setObjectName(u"k_anchorY")
        self.k_anchorY.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.k_anchorY.setMaximum(1000.000000000000000)

        self.gridLayout.addWidget(self.k_anchorY, 1, 8, 1, 1)

        self.i_anchorSelect = QComboBox(self.layoutWidget1)
        self.i_anchorSelect.setObjectName(u"i_anchorSelect")
        self.i_anchorSelect.setStyleSheet(u"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1e1e1e;\n"
"    color: #00B7FF;\n"
"    border: 1px solid #444444;\n"
"    selection-background-color: #44475a;\n"
"    selection-color: #ffffff;\n"
"    z-index: 1000;  /* \ub4dc\ub86d\ub2e4\uc6b4\uc774 \ud56d\uc0c1 \uc704\uc5d0 \uc624\ub3c4\ub85d \uc124\uc815 */\n"
"}")
        self.i_anchorSelect.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.i_anchorSelect, 1, 2, 1, 3)

        self.tagName = QLineEdit(self.layoutWidget1)
        self.tagName.setObjectName(u"tagName")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tagName.sizePolicy().hasHeightForWidth())
        self.tagName.setSizePolicy(sizePolicy3)
        self.tagName.setStyleSheet(u"#tagName {\n"
"    border: none; /* \ubaa8\ub4e0 \ud14c\ub450\ub9ac\ub97c \ucd08\uae30\ud654 */\n"
"    border-bottom: 1px solid black; /* \uc544\ub798\ucabd \ud14c\ub450\ub9ac\ub9cc \uc124\uc815 (\uad75\uae30, \uc2a4\ud0c0\uc77c, \uc0c9\uc0c1 \uc9c0\uc815) */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.tagName, 0, 9, 1, 1)

        self.labelBoxBlenderInstalation_16 = QLabel(self.layoutWidget1)
        self.labelBoxBlenderInstalation_16.setObjectName(u"labelBoxBlenderInstalation_16")
        self.labelBoxBlenderInstalation_16.setFont(font)
        self.labelBoxBlenderInstalation_16.setStyleSheet(u"")

        self.gridLayout.addWidget(self.labelBoxBlenderInstalation_16, 1, 7, 1, 1)

        self.g_anchorNum = QSpinBox(self.layoutWidget1)
        self.g_anchorNum.setObjectName(u"g_anchorNum")

        self.gridLayout.addWidget(self.g_anchorNum, 0, 1, 1, 2)

        self.label_14 = QLabel(self.layoutWidget1)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_14, 0, 6, 1, 1)

        self.labelBoxBlenderInstalation_13 = QLabel(self.layoutWidget1)
        self.labelBoxBlenderInstalation_13.setObjectName(u"labelBoxBlenderInstalation_13")
        self.labelBoxBlenderInstalation_13.setFont(font)
        self.labelBoxBlenderInstalation_13.setStyleSheet(u"")

        self.gridLayout.addWidget(self.labelBoxBlenderInstalation_13, 0, 3, 1, 1)

        self.labelBoxBlenderInstalation_15 = QLabel(self.layoutWidget1)
        self.labelBoxBlenderInstalation_15.setObjectName(u"labelBoxBlenderInstalation_15")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.labelBoxBlenderInstalation_15.sizePolicy().hasHeightForWidth())
        self.labelBoxBlenderInstalation_15.setSizePolicy(sizePolicy4)
        self.labelBoxBlenderInstalation_15.setFont(font)
        self.labelBoxBlenderInstalation_15.setStyleSheet(u"")

        self.gridLayout.addWidget(self.labelBoxBlenderInstalation_15, 1, 5, 1, 1)

        self.labelBoxBlenderInstalation_12 = QLabel(self.layoutWidget1)
        self.labelBoxBlenderInstalation_12.setObjectName(u"labelBoxBlenderInstalation_12")
        sizePolicy2.setHeightForWidth(self.labelBoxBlenderInstalation_12.sizePolicy().hasHeightForWidth())
        self.labelBoxBlenderInstalation_12.setSizePolicy(sizePolicy2)
        self.labelBoxBlenderInstalation_12.setFont(font)
        self.labelBoxBlenderInstalation_12.setStyleSheet(u"")

        self.gridLayout.addWidget(self.labelBoxBlenderInstalation_12, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.layoutWidget2 = QWidget(self.row_3)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(30, 360, 761, 41))
        self.gridLayout_6 = QGridLayout(self.layoutWidget2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.layoutWidget2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/cil-folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon3)
        self.pushButton.setIconSize(QSize(13, 13))

        self.gridLayout_6.addWidget(self.pushButton, 0, 0, 1, 1)

        self.pushButton_4 = QPushButton(self.layoutWidget2)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_4.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/cil-save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_4.setIcon(icon4)
        self.pushButton_4.setIconSize(QSize(13, 13))

        self.gridLayout_6.addWidget(self.pushButton_4, 0, 1, 1, 1)

        self.pushButton_3 = QPushButton(self.layoutWidget2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_3.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/icons/cil-pencil.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_3.setIcon(icon5)
        self.pushButton_3.setIconSize(QSize(13, 13))

        self.gridLayout_6.addWidget(self.pushButton_3, 0, 2, 1, 1)


        self.verticalLayout_16.addWidget(self.row_2)


        self.verticalLayout.addWidget(self.row_1)

        self.stackedWidget.addWidget(self.widgets)
        self.new_page = QWidget()
        self.new_page.setObjectName(u"new_page")
        self.gridLayout_20 = QGridLayout(self.new_page)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.workspace = QFrame(self.new_page)
        self.workspace.setObjectName(u"workspace")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.workspace.sizePolicy().hasHeightForWidth())
        self.workspace.setSizePolicy(sizePolicy5)
        self.workspace.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.workspace.setFrameShape(QFrame.Shape.StyledPanel)
        self.workspace.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_19.addWidget(self.workspace, 2, 0, 1, 4)

        self.wsLog = QFrame(self.new_page)
        self.wsLog.setObjectName(u"wsLog")
        self.wsLog.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.wsLog.setFrameShape(QFrame.Shape.StyledPanel)
        self.wsLog.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_19.addWidget(self.wsLog, 2, 4, 1, 2)

        self.portList = QComboBox(self.new_page)
        self.portList.setObjectName(u"portList")
        self.portList.setStyleSheet(u"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1e1e1e;\n"
"    color: #00B7FF;\n"
"    border: 1px solid #444444;\n"
"    selection-background-color: #44475a;\n"
"    selection-color: #ffffff;\n"
"    z-index: 1000;  /* \ub4dc\ub86d\ub2e4\uc6b4\uc774 \ud56d\uc0c1 \uc704\uc5d0 \uc624\ub3c4\ub85d \uc124\uc815 */\n"
"}")

        self.gridLayout_19.addWidget(self.portList, 0, 5, 1, 1)

        self.calibrationCheckBox = QCheckBox(self.new_page)
        self.calibrationCheckBox.setObjectName(u"calibrationCheckBox")
        self.calibrationCheckBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.calibrationCheckBox.setStyleSheet(u"#calibrationCheckBox {\n"
"    color: white; /* \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    font-size: 16px; /* \ud14d\uc2a4\ud2b8 \ud06c\uae30 */\n"
"	font-weight: 600;\n"
"    padding-left: 8px; /* \ud14d\uc2a4\ud2b8\uc640 \uc544\uc774\ucf58 \uac04 \uac04\uaca9 */\n"
"    background-color: transparent; /* \ubc30\uacbd\uc0c9 \uc81c\uac70 */\n"
"    border: none; /* \ud14c\ub450\ub9ac \uc81c\uac70 */\n"
"    outline: none; /* \ud3ec\ucee4\uc2a4 \ud14c\ub450\ub9ac \uc81c\uac70 */\n"
"    spacing: 7px; /* \ud14d\uc2a4\ud2b8\uc640 \uc544\uc774\ucf58 \uac04 \uc5ec\ubc31 */\n"
"}\n"
"\n"
"#calibrationCheckBox::indicator {\n"
"    width: 40px; /* \uc544\uc774\ucf58 \ub108\ube44 */\n"
"    height: 40px; /* \uc544\uc774\ucf58 \ub192\uc774 */\n"
"    background-color: transparent; /* \uc778\ub514\ucf00\uc774\ud130 \ubc30\uacbd \uc81c\uac70 */\n"
"    border: none; /* \uc778\ub514\ucf00\uc774\ud130 \ud14c\ub450\ub9ac \uc81c\uac70 */\n"
"    outline: none; /* \ud3ec\ucee4\uc2a4 \ud14c\ub450\ub9ac \uc81c\uac70 */\n"
"}\n"
""
                        "\n"
"#calibrationCheckBox::indicator:unchecked {\n"
"    image: url(:/images/images/images/switch_off.png); /* OFF \uc0c1\ud0dc \uc544\uc774\ucf58 */\n"
"    background: none; /* \ubc30\uacbd \uc81c\uac70 */\n"
"    border: none; /* \ud14c\ub450\ub9ac \uc81c\uac70 */\n"
"}\n"
"\n"
"#calibrationCheckBox::indicator:checked {\n"
"    image: url(:/images/images/images/switch_on.png); /* ON \uc0c1\ud0dc \uc544\uc774\ucf58 */\n"
"    background: none; /* \ubc30\uacbd \uc81c\uac70 */\n"
"    border: none; /* \ud14c\ub450\ub9ac \uc81c\uac70 */\n"
"}\n"
"")
        self.calibrationCheckBox.setCheckable(True)

        self.gridLayout_19.addWidget(self.calibrationCheckBox, 0, 0, 1, 1)

        self.inactiveButton = QPushButton(self.new_page)
        self.inactiveButton.setObjectName(u"inactiveButton")
        sizePolicy2.setHeightForWidth(self.inactiveButton.sizePolicy().hasHeightForWidth())
        self.inactiveButton.setSizePolicy(sizePolicy2)
        self.inactiveButton.setStyleSheet(u"#inactiveButton {\n"
"    color: white; /* \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    font-size: 16px; /* \ud14d\uc2a4\ud2b8 \ud06c\uae30 */\n"
"	font-weight: bold;\n"
"}")

        self.gridLayout_19.addWidget(self.inactiveButton, 0, 3, 1, 1)

        self.activeButton = QPushButton(self.new_page)
        self.activeButton.setObjectName(u"activeButton")
        sizePolicy2.setHeightForWidth(self.activeButton.sizePolicy().hasHeightForWidth())
        self.activeButton.setSizePolicy(sizePolicy2)
        self.activeButton.setStyleSheet(u"#activeButton {\n"
"    color: white; /* \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    font-size: 16px; /* \ud14d\uc2a4\ud2b8 \ud06c\uae30 */\n"
"	font-weight: bold;\n"
"}")

        self.gridLayout_19.addWidget(self.activeButton, 0, 2, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_19, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.new_page)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.gridLayout_7.addWidget(self.contentBox, 0, 1, 1, 1)

        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.Shape.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.Shape.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Shadow.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.Shape.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Shadow.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI Semibold"])
        font3.setPointSize(12)
        font3.setBold(False)
        font3.setItalic(False)
        self.titleLeftApp.setFont(font3)
        self.titleLeftApp.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(8)
        font4.setBold(False)
        font4.setItalic(False)
        self.titleLeftDescription.setFont(font4)
        self.titleLeftDescription.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.Shape.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy6)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy6.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy6)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_widgets = QPushButton(self.topMenu)
        self.btn_widgets.setObjectName(u"btn_widgets")
        sizePolicy6.setHeightForWidth(self.btn_widgets.sizePolicy().hasHeightForWidth())
        self.btn_widgets.setSizePolicy(sizePolicy6)
        self.btn_widgets.setMinimumSize(QSize(0, 45))
        self.btn_widgets.setFont(font)
        self.btn_widgets.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_widgets.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_widgets.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-settings.png);")

        self.verticalLayout_8.addWidget(self.btn_widgets)

        self.btn_new = QPushButton(self.topMenu)
        self.btn_new.setObjectName(u"btn_new")
        sizePolicy6.setHeightForWidth(self.btn_new.sizePolicy().hasHeightForWidth())
        self.btn_new.setSizePolicy(sizePolicy6)
        self.btn_new.setMinimumSize(QSize(0, 45))
        self.btn_new.setFont(font)
        self.btn_new.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_new.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_new.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-file.png);")

        self.verticalLayout_8.addWidget(self.btn_new)

        self.btn_exit = QPushButton(self.topMenu)
        self.btn_exit.setObjectName(u"btn_exit")
        sizePolicy6.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        self.btn_exit.setSizePolicy(sizePolicy6)
        self.btn_exit.setMinimumSize(QSize(0, 45))
        self.btn_exit.setFont(font)
        self.btn_exit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_exit.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x.png);")

        self.verticalLayout_8.addWidget(self.btn_exit)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.gridLayout_7.addWidget(self.leftMenuBg, 0, 0, 1, 1)


        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)
        QWidget.setTabOrder(self.a_workspace_width, self.b_workspace_height)
        QWidget.setTabOrder(self.b_workspace_height, self.c_danger_width)
        QWidget.setTabOrder(self.c_danger_width, self.d_danger_height)
        QWidget.setTabOrder(self.d_danger_height, self.e_danger_zone_x)
        QWidget.setTabOrder(self.e_danger_zone_x, self.f_danger_zone_y)
        QWidget.setTabOrder(self.f_danger_zone_y, self.g_anchorNum)
        QWidget.setTabOrder(self.g_anchorNum, self.h_tagNum)
        QWidget.setTabOrder(self.h_tagNum, self.i2_tagSelect)
        QWidget.setTabOrder(self.i2_tagSelect, self.tagName)
        QWidget.setTabOrder(self.tagName, self.i_anchorSelect)
        QWidget.setTabOrder(self.i_anchorSelect, self.j_anchorX)
        QWidget.setTabOrder(self.j_anchorX, self.k_anchorY)
        QWidget.setTabOrder(self.k_anchorY, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.pushButton_4)
        QWidget.setTabOrder(self.pushButton_4, self.pushButton_3)
        QWidget.setTabOrder(self.pushButton_3, self.btn_exit)
        QWidget.setTabOrder(self.btn_exit, self.minimizeAppBtn)
        QWidget.setTabOrder(self.minimizeAppBtn, self.maximizeRestoreAppBtn)
        QWidget.setTabOrder(self.maximizeRestoreAppBtn, self.closeAppBtn)
        QWidget.setTabOrder(self.closeAppBtn, self.toggleButton)
        QWidget.setTabOrder(self.toggleButton, self.btn_widgets)
        QWidget.setTabOrder(self.btn_widgets, self.btn_home)
        QWidget.setTabOrder(self.btn_home, self.btn_new)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"UWB Monitoring System", None))
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.labelBoxBlenderInstalation_3.setText(QCoreApplication.translate("MainWindow", u"Workspace Settings", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.a_workspace_width.setSuffix("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Workspace Width", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Workspace Height", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Danger Zone Width", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Danger Zone Height", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Danger Zone X", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Danger Zone Y", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.labelBoxBlenderInstalation_4.setText(QCoreApplication.translate("MainWindow", u"Anchor - Tag Settings", None))
        self.labelBoxBlenderInstalation_14.setText(QCoreApplication.translate("MainWindow", u"Anchor Position", None))
        self.j_anchorX.setPrefix("")
        self.j_anchorX.setSuffix("")
        self.k_anchorY.setSuffix("")
        self.tagName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"None", None))
        self.labelBoxBlenderInstalation_16.setText(QCoreApplication.translate("MainWindow", u"Y:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Tag Name", None))
        self.labelBoxBlenderInstalation_13.setText(QCoreApplication.translate("MainWindow", u"Tag", None))
        self.labelBoxBlenderInstalation_15.setText(QCoreApplication.translate("MainWindow", u"X:", None))
        self.labelBoxBlenderInstalation_12.setText(QCoreApplication.translate("MainWindow", u"Anchor", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u" Open Existing Workspace", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u" Save as New Workspace", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u" Edit Workspace", None))
        self.calibrationCheckBox.setText(QCoreApplication.translate("MainWindow", u"\ubcf4\uc815 \uc2dc\uc791", None))
        self.inactiveButton.setText(QCoreApplication.translate("MainWindow", u"\ube44\uac00\ub3d9", None))
        self.activeButton.setText(QCoreApplication.translate("MainWindow", u"\uac00\ub3d9", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"2025. 01. 18 Version", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"UWB Monitoring", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"UWB Based Indoor positioning system", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_widgets.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.btn_new.setText(QCoreApplication.translate("MainWindow", u"Workspace", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
    # retranslateUi

