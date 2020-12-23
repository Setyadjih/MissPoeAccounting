# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Poe_Excel_automator_ss.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_pembelian(object):
    def setupUi(self, pembelian):
        if not pembelian.objectName():
            pembelian.setObjectName(u"pembelian")
        pembelian.resize(1325, 436)
        pembelian.setMinimumSize(QSize(1325, 0))
        pembelian.setStyleSheet(u"QWidget#pembelian{	\n"
"background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #b8dbb4, stop:.9 rgba(255, 255, 255, 255));\n"
"}\n"
"\n"
"QFrame#inner_frame{\n"
"background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #e8f5e9, stop:.9 rgba(255, 255, 255, 255));\n"
"border-radius: 5px\n"
"}\n"
"QFrame#inner_frame_3{\n"
"background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #e8f5e9, stop:.9 rgba(255, 255, 255, 255));\n"
"border-radius: 5px\n"
"}\n"
"QPushButton {\n"
"background-color:#a5d6a7;\n"
"border:none;\n"
"border-radius: 2px;\n"
"min-width: 75px;\n"
"max-width: 75px;\n"
"min-height: 20px;\n"
"max-height: 20px;\n"
"}\n"
"QPushButton:hover {\n"
"background-color:#afe2b2;\n"
"}\n"
"QPushButton#file_browse_button{\n"
"background-color:#75a478;\n"
"}\n"
"QPushButton#file_browse_button:hover{\n"
"background-color:#7eb082;\n"
"}\n"
"QPushButton#file_browse_button:Pressed{\n"
"background-color:#d7ffd9;\n"
"}\n"
"QPushButton:Pressed {\n"
""
                        "background-color:#d7ffd9;\n"
"}")
        self.verticalLayout_6 = QVBoxLayout(pembelian)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.outer_frame = QFrame(pembelian)
        self.outer_frame.setObjectName(u"outer_frame")
        self.outer_frame.setMaximumSize(QSize(501, 16777215))
        font = QFont()
        font.setFamily(u"HelveticaNeue")
        self.outer_frame.setFont(font)
        self.outer_frame.setFrameShape(QFrame.StyledPanel)
        self.outer_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.outer_frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.inner_frame = QFrame(self.outer_frame)
        self.inner_frame.setObjectName(u"inner_frame")
        self.inner_frame.setMinimumSize(QSize(0, 0))
        self.inner_frame.setMaximumSize(QSize(500, 16777215))
        self.inner_frame.setFrameShape(QFrame.StyledPanel)
        self.inner_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.inner_frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.inner_frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamily(u"MS Shell Dlg 2")
        font1.setItalic(False)
        self.label.setFont(font1)

        self.verticalLayout.addWidget(self.label)

        self.vendor_label = QLabel(self.inner_frame)
        self.vendor_label.setObjectName(u"vendor_label")
        self.vendor_label.setFont(font1)

        self.verticalLayout.addWidget(self.vendor_label)

        self.item_label = QLabel(self.inner_frame)
        self.item_label.setObjectName(u"item_label")

        self.verticalLayout.addWidget(self.item_label)

        self.qty_label = QLabel(self.inner_frame)
        self.qty_label.setObjectName(u"qty_label")

        self.verticalLayout.addWidget(self.qty_label)

        self.harga_label = QLabel(self.inner_frame)
        self.harga_label.setObjectName(u"harga_label")

        self.verticalLayout.addWidget(self.harga_label)

        self.isi_label = QLabel(self.inner_frame)
        self.isi_label.setObjectName(u"isi_label")

        self.verticalLayout.addWidget(self.isi_label)

        self.label_2 = QLabel(self.inner_frame)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.inner_frame)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.input_layout = QVBoxLayout()
        self.input_layout.setObjectName(u"input_layout")
        self.date_line = QLineEdit(self.inner_frame)
        self.date_line.setObjectName(u"date_line")
        self.date_line.setMaximumSize(QSize(500, 16777215))

        self.input_layout.addWidget(self.date_line)

        self.vendor_combo = QComboBox(self.inner_frame)
        self.vendor_combo.setObjectName(u"vendor_combo")

        self.input_layout.addWidget(self.vendor_combo)

        self.item_line = QLineEdit(self.inner_frame)
        self.item_line.setObjectName(u"item_line")
        self.item_line.setMaximumSize(QSize(500, 16777215))

        self.input_layout.addWidget(self.item_line)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.qty_spin = QDoubleSpinBox(self.inner_frame)
        self.qty_spin.setObjectName(u"qty_spin")
        self.qty_spin.setMinimumSize(QSize(50, 0))
        self.qty_spin.setMaximumSize(QSize(100, 16777215))
        self.qty_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.qty_spin.setDecimals(3)
        self.qty_spin.setMaximum(9999999.000000000000000)
        self.qty_spin.setValue(1.000000000000000)

        self.horizontalLayout_7.addWidget(self.qty_spin)

        self.unit_label = QLabel(self.inner_frame)
        self.unit_label.setObjectName(u"unit_label")
        self.unit_label.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_7.addWidget(self.unit_label)

        self.unit_combo = QComboBox(self.inner_frame)
        self.unit_combo.addItem("")
        self.unit_combo.addItem("")
        self.unit_combo.addItem("")
        self.unit_combo.addItem("")
        self.unit_combo.addItem("")
        self.unit_combo.addItem("")
        self.unit_combo.addItem("")
        self.unit_combo.addItem("")
        self.unit_combo.setObjectName(u"unit_combo")

        self.horizontalLayout_7.addWidget(self.unit_combo)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)


        self.input_layout.addLayout(self.horizontalLayout_7)

        self.harga_spin = QDoubleSpinBox(self.inner_frame)
        self.harga_spin.setObjectName(u"harga_spin")
        self.harga_spin.setMinimumSize(QSize(63, 0))
        self.harga_spin.setMaximumSize(QSize(50, 16777215))
        self.harga_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.harga_spin.setProperty("showGroupSeparator", True)
        self.harga_spin.setMaximum(999999999999.000000000000000)
        self.harga_spin.setValue(20000.000000000000000)

        self.input_layout.addWidget(self.harga_spin)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.isi_spin = QDoubleSpinBox(self.inner_frame)
        self.isi_spin.setObjectName(u"isi_spin")
        self.isi_spin.setMinimumSize(QSize(63, 0))
        self.isi_spin.setMaximumSize(QSize(50, 16777215))
        self.isi_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.isi_spin.setMaximum(9999999999999.000000000000000)
        self.isi_spin.setValue(1000.000000000000000)

        self.horizontalLayout_8.addWidget(self.isi_spin)

        self.isi_unit_label = QLabel(self.inner_frame)
        self.isi_unit_label.setObjectName(u"isi_unit_label")

        self.horizontalLayout_8.addWidget(self.isi_unit_label)

        self.isi_unit_combo = QComboBox(self.inner_frame)
        self.isi_unit_combo.addItem("")
        self.isi_unit_combo.addItem("")
        self.isi_unit_combo.addItem("")
        self.isi_unit_combo.addItem("")
        self.isi_unit_combo.addItem("")
        self.isi_unit_combo.setObjectName(u"isi_unit_combo")

        self.horizontalLayout_8.addWidget(self.isi_unit_combo)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.input_layout.addLayout(self.horizontalLayout_8)

        self.category_combo = QComboBox(self.inner_frame)
        self.category_combo.setObjectName(u"category_combo")
        self.category_combo.setMaximumSize(QSize(100, 16777215))

        self.input_layout.addWidget(self.category_combo)

        self.merek_line = QLineEdit(self.inner_frame)
        self.merek_line.setObjectName(u"merek_line")

        self.input_layout.addWidget(self.merek_line)


        self.horizontalLayout.addLayout(self.input_layout)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(self.inner_frame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.add_vendor_button = QPushButton(self.inner_frame)
        self.add_vendor_button.setObjectName(u"add_vendor_button")

        self.horizontalLayout_4.addWidget(self.add_vendor_button)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_5)


        self.verticalLayout_2.addWidget(self.inner_frame)


        self.horizontalLayout_5.addWidget(self.outer_frame)

        self.outer_frame_2 = QFrame(pembelian)
        self.outer_frame_2.setObjectName(u"outer_frame_2")
        self.outer_frame_2.setMaximumSize(QSize(16777215, 16777215))
        self.outer_frame_2.setFont(font)
        self.outer_frame_2.setFrameShape(QFrame.StyledPanel)
        self.outer_frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.outer_frame_2)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(3, 3, 3, 3)
        self.inner_frame_3 = QFrame(self.outer_frame_2)
        self.inner_frame_3.setObjectName(u"inner_frame_3")
        self.inner_frame_3.setMinimumSize(QSize(0, 0))
        self.inner_frame_3.setMaximumSize(QSize(16777215, 16777215))
        self.inner_frame_3.setFrameShape(QFrame.StyledPanel)
        self.inner_frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.inner_frame_3)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.commit_table = QTableWidget(self.inner_frame_3)
        if (self.commit_table.columnCount() < 12):
            self.commit_table.setColumnCount(12)
        __qtablewidgetitem = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.commit_table.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        self.commit_table.setObjectName(u"commit_table")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commit_table.sizePolicy().hasHeightForWidth())
        self.commit_table.setSizePolicy(sizePolicy)
        self.commit_table.setMinimumSize(QSize(850, 300))
        self.commit_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.commit_table.horizontalHeader().setCascadingSectionResizes(True)
        self.commit_table.horizontalHeader().setMinimumSectionSize(10)
        self.commit_table.horizontalHeader().setDefaultSectionSize(70)
        self.commit_table.horizontalHeader().setProperty("showSortIndicator", False)
        self.commit_table.horizontalHeader().setStretchLastSection(True)
        self.commit_table.verticalHeader().setVisible(False)
        self.commit_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_11.addWidget(self.commit_table)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 5, -1, -1)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)

        self.init_button = QPushButton(self.inner_frame_3)
        self.init_button.setObjectName(u"init_button")

        self.horizontalLayout_9.addWidget(self.init_button)

        self.test_button = QPushButton(self.inner_frame_3)
        self.test_button.setObjectName(u"test_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.test_button.sizePolicy().hasHeightForWidth())
        self.test_button.setSizePolicy(sizePolicy1)
        self.test_button.setMinimumSize(QSize(75, 20))
        self.test_button.setMaximumSize(QSize(75, 20))
        self.test_button.setStyleSheet(u"")
        self.test_button.setFlat(False)

        self.horizontalLayout_9.addWidget(self.test_button)

        self.confirm_button = QPushButton(self.inner_frame_3)
        self.confirm_button.setObjectName(u"confirm_button")
        sizePolicy1.setHeightForWidth(self.confirm_button.sizePolicy().hasHeightForWidth())
        self.confirm_button.setSizePolicy(sizePolicy1)
        self.confirm_button.setMinimumSize(QSize(75, 20))

        self.horizontalLayout_9.addWidget(self.confirm_button)


        self.verticalLayout_11.addLayout(self.horizontalLayout_9)


        self.verticalLayout_10.addLayout(self.verticalLayout_11)


        self.verticalLayout_9.addWidget(self.inner_frame_3)


        self.horizontalLayout_5.addWidget(self.outer_frame_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.file_browse_layout = QHBoxLayout()
        self.file_browse_layout.setSpacing(5)
        self.file_browse_layout.setObjectName(u"file_browse_layout")
        self.file_select_label = QLabel(pembelian)
        self.file_select_label.setObjectName(u"file_select_label")

        self.file_browse_layout.addWidget(self.file_select_label)

        self.xls_file_browser = QLineEdit(pembelian)
        self.xls_file_browser.setObjectName(u"xls_file_browser")
        self.xls_file_browser.setReadOnly(True)

        self.file_browse_layout.addWidget(self.xls_file_browser)

        self.file_browse_button = QPushButton(pembelian)
        self.file_browse_button.setObjectName(u"file_browse_button")

        self.file_browse_layout.addWidget(self.file_browse_button)


        self.verticalLayout_6.addLayout(self.file_browse_layout)

        self.line = QFrame(pembelian)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_6.addWidget(self.line)

        self.status_bar = QLabel(pembelian)
        self.status_bar.setObjectName(u"status_bar")

        self.verticalLayout_6.addWidget(self.status_bar)


        self.retranslateUi(pembelian)

        QMetaObject.connectSlotsByName(pembelian)
    # setupUi

    def retranslateUi(self, pembelian):
        pembelian.setWindowTitle(QCoreApplication.translate("pembelian", u"Form", None))
        self.label.setText(QCoreApplication.translate("pembelian", u"Date", None))
        self.vendor_label.setText(QCoreApplication.translate("pembelian", u"Vendor", None))
        self.item_label.setText(QCoreApplication.translate("pembelian", u"Item", None))
        self.qty_label.setText(QCoreApplication.translate("pembelian", u"Quantity", None))
        self.harga_label.setText(QCoreApplication.translate("pembelian", u"Harga", None))
        self.isi_label.setText(QCoreApplication.translate("pembelian", u"Isi", None))
        self.label_2.setText(QCoreApplication.translate("pembelian", u"Category", None))
        self.label_3.setText(QCoreApplication.translate("pembelian", u"Merek", None))
        self.unit_label.setText(QCoreApplication.translate("pembelian", u"Unit", None))
        self.unit_combo.setItemText(0, QCoreApplication.translate("pembelian", u"ctn", None))
        self.unit_combo.setItemText(1, QCoreApplication.translate("pembelian", u"pack", None))
        self.unit_combo.setItemText(2, QCoreApplication.translate("pembelian", u"pcs", None))
        self.unit_combo.setItemText(3, QCoreApplication.translate("pembelian", u"Kg", None))
        self.unit_combo.setItemText(4, QCoreApplication.translate("pembelian", u"g", None))
        self.unit_combo.setItemText(5, QCoreApplication.translate("pembelian", u"L", None))
        self.unit_combo.setItemText(6, QCoreApplication.translate("pembelian", u"ml", None))
        self.unit_combo.setItemText(7, QCoreApplication.translate("pembelian", u"sak", None))

        self.isi_unit_label.setText(QCoreApplication.translate("pembelian", u"Unit", None))
        self.isi_unit_combo.setItemText(0, QCoreApplication.translate("pembelian", u"pcs", None))
        self.isi_unit_combo.setItemText(1, QCoreApplication.translate("pembelian", u"Kg", None))
        self.isi_unit_combo.setItemText(2, QCoreApplication.translate("pembelian", u"g", None))
        self.isi_unit_combo.setItemText(3, QCoreApplication.translate("pembelian", u"L", None))
        self.isi_unit_combo.setItemText(4, QCoreApplication.translate("pembelian", u"ml", None))

        self.add_vendor_button.setText(QCoreApplication.translate("pembelian", u"Add", None))
        ___qtablewidgetitem = self.commit_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("pembelian", u"Date", None));
        ___qtablewidgetitem1 = self.commit_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("pembelian", u"Item", None));
        ___qtablewidgetitem2 = self.commit_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("pembelian", u"Vendor", None));
        ___qtablewidgetitem3 = self.commit_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("pembelian", u"Merek", None));
        ___qtablewidgetitem4 = self.commit_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("pembelian", u"Quantity", None));
        ___qtablewidgetitem5 = self.commit_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("pembelian", u"Unit", None));
        ___qtablewidgetitem6 = self.commit_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("pembelian", u"Harga", None));
        ___qtablewidgetitem7 = self.commit_table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("pembelian", u"Total", None));
        ___qtablewidgetitem8 = self.commit_table.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("pembelian", u"Isi", None));
        ___qtablewidgetitem9 = self.commit_table.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("pembelian", u"Isi Unit", None));
        ___qtablewidgetitem10 = self.commit_table.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("pembelian", u"Harga/Unit", None));
        ___qtablewidgetitem11 = self.commit_table.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("pembelian", u"Category", None));
        self.init_button.setText(QCoreApplication.translate("pembelian", u"Init Data", None))
        self.test_button.setText(QCoreApplication.translate("pembelian", u"TEST", None))
        self.confirm_button.setText(QCoreApplication.translate("pembelian", u"Confirm", None))
        self.file_select_label.setText(QCoreApplication.translate("pembelian", u"Excel file:", None))
        self.file_browse_button.setText(QCoreApplication.translate("pembelian", u"Browse", None))
        self.status_bar.setText(QCoreApplication.translate("pembelian", u"status bar...", None))
    # retranslateUi

