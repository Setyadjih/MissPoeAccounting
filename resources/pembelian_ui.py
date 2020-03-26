# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Poe_Excel_automator.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_pembelian(object):
    def setupUi(self, pembelian):
        if pembelian.objectName():
            pembelian.setObjectName(u"pembelian")
        pembelian.resize(1210, 421)
        self.verticalLayout_6 = QVBoxLayout(pembelian)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
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
        self.label = QLabel(pembelian)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.vendor_label = QLabel(pembelian)
        self.vendor_label.setObjectName(u"vendor_label")

        self.verticalLayout.addWidget(self.vendor_label)

        self.item_label = QLabel(pembelian)
        self.item_label.setObjectName(u"item_label")

        self.verticalLayout.addWidget(self.item_label)

        self.qty_label = QLabel(pembelian)
        self.qty_label.setObjectName(u"qty_label")

        self.verticalLayout.addWidget(self.qty_label)

        self.harga_label = QLabel(pembelian)
        self.harga_label.setObjectName(u"harga_label")

        self.verticalLayout.addWidget(self.harga_label)

        self.isi_label = QLabel(pembelian)
        self.isi_label.setObjectName(u"isi_label")

        self.verticalLayout.addWidget(self.isi_label)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.date_line = QLineEdit(pembelian)
        self.date_line.setObjectName(u"date_line")
        self.date_line.setMaximumSize(QSize(500, 16777215))

        self.verticalLayout_2.addWidget(self.date_line)

        self.vendor_line = QLineEdit(pembelian)
        self.vendor_line.setObjectName(u"vendor_line")
        self.vendor_line.setMinimumSize(QSize(200, 0))
        self.vendor_line.setMaximumSize(QSize(500, 16777215))

        self.verticalLayout_2.addWidget(self.vendor_line)

        self.item_line = QLineEdit(pembelian)
        self.item_line.setObjectName(u"item_line")
        self.item_line.setMaximumSize(QSize(500, 16777215))

        self.verticalLayout_2.addWidget(self.item_line)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.qty_spin = QSpinBox(pembelian)
        self.qty_spin.setObjectName(u"qty_spin")
        self.qty_spin.setMinimumSize(QSize(50, 0))
        self.qty_spin.setMaximumSize(QSize(100, 16777215))
        self.qty_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.qty_spin.setMinimum(0)

        self.horizontalLayout_7.addWidget(self.qty_spin)

        self.unit_label = QLabel(pembelian)
        self.unit_label.setObjectName(u"unit_label")
        self.unit_label.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_7.addWidget(self.unit_label)

        self.unit_line = QLineEdit(pembelian)
        self.unit_line.setObjectName(u"unit_line")
        self.unit_line.setMinimumSize(QSize(10, 0))
        self.unit_line.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_7.addWidget(self.unit_line)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.harga_spin = QSpinBox(pembelian)
        self.harga_spin.setObjectName(u"harga_spin")
        self.harga_spin.setMaximumSize(QSize(50, 16777215))
        self.harga_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.harga_spin.setMinimum(0)
        self.harga_spin.setMaximum(999999999)
        self.harga_spin.setValue(1)

        self.verticalLayout_2.addWidget(self.harga_spin)

        self.isi_spin = QSpinBox(pembelian)
        self.isi_spin.setObjectName(u"isi_spin")
        self.isi_spin.setMaximumSize(QSize(50, 16777215))
        self.isi_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.isi_spin.setMinimum(1)
        self.isi_spin.setMaximum(999999999)

        self.verticalLayout_2.addWidget(self.isi_spin)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.add_vendor_button = QPushButton(pembelian)
        self.add_vendor_button.setObjectName(u"add_vendor_button")

        self.horizontalLayout_4.addWidget(self.add_vendor_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.commit_table = QTableWidget(pembelian)
        if (self.commit_table.columnCount() < 8):
            self.commit_table.setColumnCount(8)
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
        self.commit_table.setObjectName(u"commit_table")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commit_table.sizePolicy().hasHeightForWidth())
        self.commit_table.setSizePolicy(sizePolicy)
        self.commit_table.setMinimumSize(QSize(500, 300))
        self.commit_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.commit_table.horizontalHeader().setCascadingSectionResizes(True)
        self.commit_table.horizontalHeader().setMinimumSectionSize(10)
        self.commit_table.horizontalHeader().setDefaultSectionSize(70)
        self.commit_table.horizontalHeader().setStretchLastSection(True)
        self.commit_table.verticalHeader().setVisible(False)
        self.commit_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_3.addWidget(self.commit_table)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.confirm_button = QPushButton(pembelian)
        self.confirm_button.setObjectName(u"confirm_button")

        self.horizontalLayout_3.addWidget(self.confirm_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")

        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.file_select_label = QLabel(pembelian)
        self.file_select_label.setObjectName(u"file_select_label")

        self.horizontalLayout_2.addWidget(self.file_select_label)

        self.xls_file_browser = QLineEdit(pembelian)
        self.xls_file_browser.setObjectName(u"xls_file_browser")
        self.xls_file_browser.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.xls_file_browser)

        self.file_browse_button = QPushButton(pembelian)
        self.file_browse_button.setObjectName(u"file_browse_button")

        self.horizontalLayout_2.addWidget(self.file_browse_button)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

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
        self.unit_label.setText(QCoreApplication.translate("pembelian", u"Unit", None))
        self.unit_line.setText(QCoreApplication.translate("pembelian", u"kg", None))
        self.add_vendor_button.setText(QCoreApplication.translate("pembelian", u"Add", None))
        ___qtablewidgetitem = self.commit_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("pembelian", u"Date", None));
        ___qtablewidgetitem1 = self.commit_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("pembelian", u"Vendor", None));
        ___qtablewidgetitem2 = self.commit_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("pembelian", u"Quantity", None));
        ___qtablewidgetitem3 = self.commit_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("pembelian", u"Unit", None));
        ___qtablewidgetitem4 = self.commit_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("pembelian", u"Harga", None));
        ___qtablewidgetitem5 = self.commit_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("pembelian", u"Total", None));
        ___qtablewidgetitem6 = self.commit_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("pembelian", u"Isi", None));
        ___qtablewidgetitem7 = self.commit_table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("pembelian", u"Harga/Unit", None));
        self.confirm_button.setText(QCoreApplication.translate("pembelian", u"Confirm", None))
        self.file_select_label.setText(QCoreApplication.translate("pembelian", u"Excel file:", None))
        self.file_browse_button.setText(QCoreApplication.translate("pembelian", u"Browse", None))
        self.status_bar.setText(QCoreApplication.translate("pembelian", u"status bar...", None))
    # retranslateUi

