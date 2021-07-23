import sys
from datetime import datetime
import shutil
from pathlib import Path

from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidgetItem,
    QFileDialog,
    QAction,
    QMessageBox,
)
from PySide2.QtCore import Qt
from openpyxl import load_workbook

from core.utils import (
    get_logger,
    get_file_handler,
    write_categories_file,
    read_categories_file,
)
from resources.pembelian_ui_ss import Ui_pembelian
from core.excel_functions import write_to_excel, init_catsheet, transfer_records
from core.constants import APP_VERSION, DATE, DEFAULT_CATEGORIES, CAT_REF, ExcelItem


# noinspection SpellCheckingInspection
class PembelianWidget(QWidget):
    def __init__(self, test=False, parent=None):
        super(PembelianWidget, self).__init__(parent)
        self.ui = Ui_pembelian()
        self.ui.setupUi(self)
        self.ui.date_line.setText(DATE)
        self.logger = get_logger("excel_automator")
        self.logger.info("Initializing program")

        self.cat_items_dict = {}

        # Context menu setup
        self.ui.commit_table.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.del_row_action = QAction(self, text="Delete Table Row")

        # noinspection PyUnresolvedReferences
        self.del_row_action.triggered.connect(self.delete_table_row)
        self.ui.commit_table.addAction(self.del_row_action)

        self.setWindowTitle(f"Poe Excel Automator {APP_VERSION}")
        self.ui.status_bar.setText("Ready for input.")
        self.ui.item_line.hide()

        # Default test button to hide
        self.ui.test_button.hide()
        if test:
            self.ui.test_button.show()
            self.ui.test_button.clicked.connect(self.test_func)

        # Setup Category dictionary and file
        self.categories = DEFAULT_CATEGORIES

        if not Path(CAT_REF).exists():
            self.logger.info("Creating new cat ref file")
            write_categories_file()
        else:
            self.categories = read_categories_file()

        self.skip_list = self.categories["CATEGORIES"] + self.categories["MISC"]
        self.ui.category_combo.clear()
        self.ui.category_combo.addItems(self.categories["CATEGORIES"])

        # Hookup buttons
        self.ui.new_item_check.clicked.connect(self.item_input_toggle)
        self.ui.add_vendor_button.clicked.connect(self.add_to_table)
        self.ui.file_browse_button.clicked.connect(self.get_excel_sheet)
        self.ui.confirm_button.clicked.connect(self.confirm_table)
        self.ui.init_button.clicked.connect(self.init_cat_button)
        self.ui.import_button.clicked.connect(self.import_data)
        self.ui.category_combo.currentIndexChanged.connect(self.load_cat_items)

    def load_cat_items(self):
        self.ui.item_combo.clear()
        current_cat = self.ui.category_combo.currentText()
        # incase invalid text
        if not current_cat:
            self.logger.error("Category is empty, could not load items")
            return
        sorted_list = sorted(self.cat_items_dict[current_cat])
        self.ui.item_combo.addItems(sorted_list)

    def item_input_toggle(self):
        """Toggle item input style"""
        if self.ui.new_item_check.isChecked():
            self.ui.item_combo.hide()
            self.ui.item_line.show()
        else:
            self.ui.item_combo.show()
            self.ui.item_line.hide()
            self.ui.item_line.clear()

    def test_func(self):
        """Clear out category sheets"""
        input_wb = load_workbook(self.ui.xls_file_browser.text(), data_only=False)
        for cat in self.categories["CATEGORIES"]:
            category_sheet = input_wb[cat]
            max_row = category_sheet.max_row
            category_sheet.delete_rows(3, max_row)
        input_wb.save(self.ui.xls_file_browser.text())

    def make_backup(self):
        # Create a backup copy just in case
        self.logger.info("Saving backup.")
        file = self.ui.xls_file_browser.text()
        dest = Path(file).with_suffix(".bak")
        shutil.copyfile(file, dest)

    def init_cat_button(self):
        """Start initialization of category sheets"""
        file = self.ui.xls_file_browser.text()
        if not file:
            self.__set_info("No file to write to!", "fail")
            return

        result = QMessageBox.warning(
            self,
            "Are you sure?",
            "Initializing the category data can take a long time, are you sure"
            " you want to do this?\n The category sheets will be cleared out.",
            QMessageBox.Cancel,
            QMessageBox.Ok
        )
        if result != QMessageBox.Ok:
            return

        self.__set_info("Working on data....")
        self.make_backup()
        try:
            init_catsheet(file, self.categories, self.logger)
        except Exception as e:
            self.logger.error(e)
            self.__set_info(f"Failed to init data! Error: {e}", "fail")
            return
        self.logger.info("Finished init")
        self.__set_info("All done!", "done")

    def import_data(self):
        new_workbook = self.ui.xls_file_browser.text()
        if not new_workbook:
            self.__set_info("Please select Workbook to import to!", "fail")

        try:
            old_workbook = QFileDialog.getOpenFileName(filter="Old Workbook (*.xlsx)")[0]
        except KeyError as error:
            self.__set_info(f"Failed to pick sheet! Vendor doesn't exist.", "fail")
            self.logger.error(error)
            return
        except Exception as error:
            self.__set_info(f"Failed to pick sheet! Reason: {error}", "fail")
            self.logger.error(error)
            return
        self.__set_info("Transferring records...")
        transfer_records(old_workbook, new_workbook, self.categories, self.logger)
        self.__set_info("Done Transferring!", "done")

    def delete_table_row(self):
        current_row = self.ui.commit_table.currentRow()
        self.ui.commit_table.removeRow(current_row)

    def get_excel_sheet(self):
        """Load Purchase Excelsheet and get vendors"""
        try:
            file_dir = QFileDialog.getOpenFileName(filter="Excel sheets (*.xlsx)")[0]
        except KeyError as error:
            self.__set_info(f"Failed to pick sheet! Vendor doesn't exist.", "fail")
            self.logger.error(error)
            return
        except Exception as error:
            self.__set_info(f"Failed to pick sheet! Reason: {error}", "fail")
            self.logger.error(error)
            return

        # File check
        self.ui.xls_file_browser.setText(file_dir)
        if not self.ui.xls_file_browser.text():
            self.__set_info("Did not get file path", "fail")
            return

        # Populate vendor drop down
        purchase_book = load_workbook(file_dir)
        skip_list = self.categories["CATEGORIES"] + self.categories["MISC"]
        vendor_sheets = [_ for _ in purchase_book.sheetnames if _ not in skip_list]
        for vendor in vendor_sheets:
            self.ui.vendor_combo.addItem(vendor)

        # populate category selection with item lists
        bad_cats = []
        for category in self.categories["CATEGORIES"]:
            cat_items = []
            try:
                for row in purchase_book[category].iter_rows(min_row=3, values_only=True):
                    if row[0]:
                        cat_items.append(row[0])

                self.cat_items_dict[category] = cat_items
            except KeyError:
                self.logger.info(f"{category} not in Workbook")
                bad_cat_index = self.ui.category_combo.findText(category)
                bad_cats.append(bad_cat_index)

        # Remove invalid categories from loaded sheet
        for cat in reversed(sorted(bad_cats)):
            self.ui.category_combo.removeItem(cat)

        # initial category population
        self.load_cat_items()

        # Add easy to access log with username
        log_dir = Path(file_dir).parent.joinpath("_LOG").as_posix()
        self.logger.addHandler(get_file_handler("excel_automator", log_dir))
        self.logger.debug("Init user logging")

    def clear_inputs(self):
        self.ui.vendor_combo.clear()
        self.ui.item_line.clear()
        self.ui.qty_spin.clear()
        self.ui.harga_spin.clear()
        self.ui.isi_spin.clear()
        self.__set_info("Cleared inputs!", status="done")

    def add_to_table(self):
        # Table entry validation
        if (
            self.ui.harga_spin.value() == 0
            or self.ui.isi_spin.value() == 0
            or self.ui.qty_spin.value() == 0
            or not self.ui.date_line.text()
            or not self.ui.isi_unit_combo.currentText()
            or not self.ui.vendor_combo.currentText()
        ):
            self.__set_info("Values cannot be 0!", "fail")
            return

        # Commit input to table
        row_count = self.ui.commit_table.rowCount()
        self.ui.commit_table.insertRow(row_count)
        new_row = row_count

        details = self.get_ui_details()
        for column, item in enumerate(details):
            self.ui.commit_table.setItem(new_row, column, item)
        self.__set_info("Added item to table")

    def get_ui_details(self):
        date_text = self.ui.date_line.text()
        date = datetime.strptime(date_text, "%d-%b-%y")
        total_cost = self.ui.qty_spin.value() * self.ui.harga_spin.value()
        unit_cost = total_cost / self.ui.isi_spin.value()
        date_data = QTableWidgetItem(self.ui.date_line.text())
        date_data.setData(Qt.UserRole, date)
        vendor_data = QTableWidgetItem(self.ui.vendor_combo.currentText())
        vendor_data.setData(Qt.UserRole, self.ui.vendor_combo.currentText())
        if not self.ui.merek_line.text():
            self.ui.merek_line.setText("")
        merek_data = QTableWidgetItem(self.ui.merek_line.text())
        merek_data.setData(Qt.UserRole, self.ui.merek_line.text())
        item_text = self.ui.item_combo.currentText()
        if self.ui.new_item_check.isChecked():
            item_text = self.ui.item_line.text().strip()
        item_data = QTableWidgetItem(item_text)
        item_data.setData(Qt.UserRole, item_text)
        qty_data = QTableWidgetItem(self.ui.qty_spin.text())
        qty_data.setData(Qt.UserRole, self.ui.qty_spin.value())
        unit_data = QTableWidgetItem(self.ui.unit_combo.currentText())
        unit_data.setData(Qt.UserRole, self.ui.unit_combo.currentText())
        harga_data = QTableWidgetItem(self.ui.harga_spin.text())
        harga_data.setData(Qt.UserRole, self.ui.harga_spin.value())
        total_data = QTableWidgetItem(str(total_cost))
        total_data.setData(Qt.UserRole, total_cost)
        isi_data = QTableWidgetItem(self.ui.isi_spin.text())
        isi_data.setData(Qt.UserRole, self.ui.isi_spin.value())
        isi_unit_data = QTableWidgetItem(self.ui.isi_unit_combo.currentText())
        isi_unit_data.setData(Qt.UserRole, self.ui.isi_unit_combo.currentText())
        unit_harga_data = QTableWidgetItem(str(unit_cost))
        unit_harga_data.setData(Qt.UserRole, unit_cost)
        category_data = QTableWidgetItem(self.ui.category_combo.currentText())
        category_data.setData(Qt.UserRole, self.ui.category_combo.currentText())
        details = (
            date_data,
            item_data,
            vendor_data,
            merek_data,
            qty_data,
            unit_data,
            harga_data,
            total_data,
            isi_data,
            isi_unit_data,
            unit_harga_data,
            category_data,
        )
        return details

    def confirm_table(self):
        """Commit table to excel file"""
        self.logger.info("Executing table to excel file")

        file = self.ui.xls_file_browser.text()
        if not file:
            self.__set_info("No file to write to!", "fail")
            return

        if self.ui.commit_table.rowCount() == 0:
            self.__set_info("Nothing to write")
            return

        self.make_backup()
        for row in range(self.ui.commit_table.rowCount()):
            try:
                # Get values from item ranges as an ExcelItem
                date = self.ui.commit_table.item(row, 0).data(Qt.UserRole)
                excel_item = self.create_excel_item(row)

                if not excel_item.name:
                    self.__set_info("item is empty")
                    raise ValueError

                # Execute table to excel
                self.__set_info("Writing to Excel sheet...")
                write_to_excel(self.skip_list, date, file, excel_item, self.logger)
            except Exception as error:
                self.__set_info(f"Failed writing to excel sheet! Reason: {error}", "fail")
                self.logger.error(f"Failed on " f"{self.ui.commit_table.item(row, 1)}")
                self.logger.error(f"Error: {error}")
                return

        self.clean_table()
        self.logger.debug("Finished writing")
        self.__set_info("All done writing!", status="done")

    def create_excel_item(self, row):
        excel_item = ExcelItem()
        excel_item.name = self.ui.commit_table.item(row, 1).data(Qt.UserRole)
        excel_item.vendor = self.ui.commit_table.item(row, 2).data(Qt.UserRole)
        excel_item.brand = self.ui.commit_table.item(row, 3).data(Qt.UserRole)
        excel_item.quantity = self.ui.commit_table.item(row, 4).data(Qt.UserRole)
        excel_item.unit = self.ui.commit_table.item(row, 5).data(Qt.UserRole)
        excel_item.cost = self.ui.commit_table.item(row, 6).data(Qt.UserRole)
        excel_item.isi = self.ui.commit_table.item(row, 8).data(Qt.UserRole)
        excel_item.isi_unit = self.ui.commit_table.item(row, 9).data(Qt.UserRole)
        excel_item.category = self.ui.commit_table.item(row, 11).data(Qt.UserRole)
        return excel_item

    def clean_table(self):
        self.ui.commit_table.clearContents()
        for row in reversed(range(self.ui.commit_table.rowCount())):
            self.ui.commit_table.removeRow(row)

    def __set_info(self, message, status=""):
        """Display the info on the GUI

        done: green,
        fail: red,
        default: blue

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
        # noinspection PyUnresolvedReferences
        qApp.processEvents()  # update the UI


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PembelianWidget(test=False)
    window.show()

    sys.exit(app.exec_())
