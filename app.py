import sys
from datetime import datetime

from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidgetItem,
    QFileDialog,
    QAction,
)
from PySide2.QtCore import Qt
from openpyxl import load_workbook

from utils import get_logger
from resources.pembelian_ui_ss import Ui_pembelian
from excel_functions import write_to_excel
import constants


class PembelianWidget(QWidget):
    def __init__(self, parent=None):
        super(PembelianWidget, self).__init__(parent)
        self.ui = Ui_pembelian()
        self.ui.setupUi(self)
        self.ui.date_line.setText(constants.DATE)
        self.logger = get_logger("excel_automator")
        self.logger.info("Initializing program")

        # Context menu setup
        self.ui.commit_table.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.del_row_action = QAction(self, text="Delete Table Row")
        self.del_row_action.triggered.connect(self.delete_table_row)
        self.ui.commit_table.addAction(self.del_row_action)

        self.setWindowTitle(f"Poe Excel Automator {constants.APP_VERSION}")
        self.ui.status_bar.setText("Ready for input.")
        self.ui.confirm_button.setDisabled(True)

        # Hookup buttons
        self.ui.test_button.clicked.connect(self.test_func)

        self.ui.add_vendor_button.clicked.connect(self.add_to_table)
        self.ui.file_browse_button.clicked.connect(self.get_excel_sheet)
        self.ui.confirm_button.clicked.connect(self.confirm_table)

        # # FIXME:
        # # TESTING PARAMS
        # self.ui.xls_file_browser.setText("D:\Miss Poe\Costings\_data\Pembelian 2020 TESTING.xlsx")
        # self.ui.confirm_button.setEnabled(True)

    def test_func(self):
        purchase_book = load_workbook(self.ui.xls_file_browser.text())
        for vendor in purchase_book.sheetnames:
            self.ui.vendor_combo.addItem(vendor)

    def delete_table_row(self):
        current_row = self.ui.commit_table.currentRow()
        self.ui.commit_table.removeRow(current_row)

    def get_excel_sheet(self):
        """Load Purchase Excelsheet and get vendors"""
        try:
            self.ui.xls_file_browser.setText(
                QFileDialog.getOpenFileName(filter="Excel sheets (*.xlsx)")[0]
            )
        except KeyError as error:
            self.__set_info(f"Failed to pick sheet! Vendor doesn't exist.", "fail")
            self.logger.error(error)
            return
        except Exception as error:
            self.__set_info(f"Failed to pick sheet! Reason: {error}", "fail")
            self.logger.error(error)
            return

        if not self.ui.xls_file_browser.text():
            return
        purchase_book = load_workbook(self.ui.xls_file_browser.text())
        for vendor in purchase_book.sheetnames:
            self.ui.vendor_combo.addItem(vendor)

        self.ui.confirm_button.setDisabled(True)

        if self.ui.xls_file_browser.text():
            self.ui.confirm_button.setEnabled(True)

    def clear_inputs(self):
        self.ui.vendor_combo.clear()
        self.ui.item_line.clear()
        self.ui.qty_spin.clear()
        self.ui.unit_line.clear()
        self.ui.harga_spin.clear()
        self.ui.isi_spin.clear()
        self.ui.isi_unit_line.clear()
        self.__set_info("Cleared inputs!", status="done")

    def add_to_table(self):
        if (
            self.ui.harga_spin.value() == 0
            or self.ui.isi_spin.value() == 0
            or self.ui.qty_spin.value() == 0
        ):
            self.__set_info("Values cannot be 0!", "fail")

        date_text = self.ui.date_line.text()
        date = datetime.strptime(date_text, "%d-%b-%y")

        # Commit input to table
        row_count = self.ui.commit_table.rowCount()
        self.ui.commit_table.insertRow(row_count)
        new_row = row_count

        total_cost = self.ui.qty_spin.value() * self.ui.harga_spin.value()
        unit_cost = total_cost / self.ui.isi_spin.value()

        date_data = QTableWidgetItem(self.ui.date_line.text())
        date_data.setData(Qt.UserRole, date)

        vendor_data = QTableWidgetItem(self.ui.vendor_combo.currentText())
        vendor_data.setData(Qt.UserRole, self.ui.vendor_combo.currentText())

        item_data = QTableWidgetItem(self.ui.item_line.text())
        item_data.setData(Qt.UserRole, self.ui.item_line.text())

        qty_data = QTableWidgetItem(self.ui.qty_spin.text())
        qty_data.setData(Qt.UserRole, self.ui.qty_spin.value())

        unit_data = QTableWidgetItem(self.ui.unit_line.text())
        unit_data.setData(Qt.UserRole, self.ui.unit_line.text())

        harga_data = QTableWidgetItem(self.ui.harga_spin.text())
        harga_data.setData(Qt.UserRole, self.ui.harga_spin.value())

        total_data = QTableWidgetItem(str(total_cost))
        total_data.setData(Qt.UserRole, total_cost)

        isi_data = QTableWidgetItem(self.ui.isi_spin.text())
        isi_data.setData(Qt.UserRole, self.ui.isi_spin.value())

        isi_unit_data = QTableWidgetItem(self.ui.isi_unit_line.text())
        isi_unit_data.setData(Qt.UserRole, self.ui.isi_unit_line.text())

        unit_harga_data = QTableWidgetItem(str(unit_cost))
        unit_harga_data.setData(Qt.UserRole, unit_cost)

        category_data = QTableWidgetItem(self.ui.category_combo.currentText())
        category_data.setData(Qt.UserRole, self.ui.category_combo.currentText())

        details = (
            date_data,
            item_data,
            vendor_data,
            qty_data,
            unit_data,
            harga_data,
            total_data,
            isi_data,
            isi_unit_data,
            unit_harga_data,
            category_data,
        )

        for column, item in enumerate(details):
            self.ui.commit_table.setItem(new_row, column, item)

    def confirm_table(self):
        self.logger.info("Executing table")
        file = self.ui.xls_file_browser.text()
        if self.ui.commit_table.rowCount() == 0:
            self.__set_info("Nothing to write")
            return
        try:
            for row in range(self.ui.commit_table.rowCount()):
                # Get values from item ranges
                date = self.ui.commit_table.item(row, 0).data(Qt.UserRole)
                item = self.ui.commit_table.item(row, 1).data(Qt.UserRole)
                vendor = self.ui.commit_table.item(row, 2).data(Qt.UserRole)
                quantity = self.ui.commit_table.item(row, 3).data(Qt.UserRole)
                unit = self.ui.commit_table.item(row, 4).data(Qt.UserRole)
                harga = self.ui.commit_table.item(row, 5).data(Qt.UserRole)
                isi = self.ui.commit_table.item(row, 7).data(Qt.UserRole)
                isi_unit = self.ui.commit_table.item(row, 8).data(Qt.UserRole)
                category = self.ui.commit_table.item(row, 10).data(Qt.UserRole)

                if not item:
                    self.__set_info("item is empty")
                    return

                # Execute table to excel
                write_to_excel(
                    date,
                    file,
                    vendor,
                    item,
                    quantity,
                    unit,
                    harga,
                    isi,
                    isi_unit,
                    category,
                    self.logger,
                )

                self.__set_info("Writing to Excel sheet...")
        except Exception as error:
            self.__set_info(f"Failed writing to excel sheet! Reason: {error}", "fail")
            self.logger.error(f"Error: {error}")
            return
        self.clean_table()

        self.__set_info("All done writing!", status="done")

    def clean_table(self):
        self.ui.commit_table.clearContents()
        for row in reversed(range(self.ui.commit_table.rowCount())):
            self.ui.commit_table.removeRow(row)

    def __set_info(self, message, status=""):
        """Display the info on the GUI

        :param message: message to display on the gui
        :type message: str
        :param status: status of the message which effects the color of text
        :type status: str
        """
        if status == "fail":
            color = "red"
        elif status == "done":
            color = "#00ff06"  # bright green
        else:
            color = "#00b2ff"  # bright blue

        self.ui.status_bar.setText(message)
        self.ui.status_bar.setStyleSheet("color: {}".format(color))
        qApp.processEvents()  # update the UI


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PembelianWidget()
    window.show()

    sys.exit(app.exec_())
