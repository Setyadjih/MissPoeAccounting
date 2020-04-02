import openpyxl

from logging import getLogger

from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import numbers

# Today as 30-Mar-19
DATE_FORMAT = "dd-mmm-yy"

COMMA_FORMAT = "#,##0"
RP_FORMAT = u'_("Rp"* #,##0_);_("Rp"* (#,##0);_("Rp"* "-"_);_(@_)'


def write_to_excel(date, file, vendor, item, quantity, unit, cost, isi,
                   category, logger=None):
    """
    Write the given data to the purchasing excel sheet

    :param date: date of purchase
    :param file: file path to excel sheet to edit
    :param vendor: Vendor WS to edit
    :param item: name of item
    :param quantity: # of items
    :param unit: unit for item quantity
    :param cost: Cost of purchase
    :param isi: how many units per item purchase
    :param category: category of purchase
    :param logger: logger pass through
    """
    logger = logger if logger else getLogger()
    # Load excel file path
    purchase_wb = openpyxl.load_workbook(file, data_only=True)

    # Create vendor sheet if new
    vendor_sheet = purchase_wb[vendor]

    last_row = vendor_sheet.max_row + 1
    logger.debug(f"last row = {last_row}")

    # check for empty row error
    if not vendor_sheet[f"B{last_row-1}"].value:
        last_row -= 1

    total_formula = cost * quantity
    per_unit_formula = total_formula / isi

    logger.debug(f"Appending item data")

    vendor_sheet[f"A{last_row}"] = date
    vendor_sheet[f"B{last_row}"] = item
    vendor_sheet[f"C{last_row}"] = quantity
    vendor_sheet[f"D{last_row}"] = unit
    vendor_sheet[f"E{last_row}"] = cost
    vendor_sheet[f"F{last_row}"] = total_formula
    vendor_sheet[f"G{last_row}"] = isi
    vendor_sheet[f"H{last_row}"] = per_unit_formula

    # format cells for Rupiah
    logger.debug("Assigning format strings")
    date_cell = vendor_sheet.cell(last_row, 1)
    date_cell.number_format = DATE_FORMAT

    cost_cell = vendor_sheet.cell(last_row, 5)
    cost_cell.number_format = RP_FORMAT

    total_cell = vendor_sheet.cell(last_row, 6)
    total_cell.number_format = RP_FORMAT

    isi_cell = vendor_sheet.cell(last_row, 7)
    isi_cell.number_format = COMMA_FORMAT

    per_unit_cell = vendor_sheet.cell(last_row, 8)
    per_unit_cell.number_format = RP_FORMAT

    # Append to costing according to category
    try:
        cat_sheet = purchase_wb[category]
    except KeyError:
        purchase_wb.create_sheet(category)
        cat_sheet: Worksheet = purchase_wb[category]

    average, current_qty = calc_totals(purchase_wb, item, logger=logger)
    cs = cat_sheet.iter_rows(min_row=3, min_col=2, max_col=2, values_only=True)

    # check if item already in sheet
    # Row num at two due to Excel sheet format
    item_exist = False
    row_num = 3

    for row in cs:
        item_name = row[0]
        if item == item_name:
            item_exist = True
            break
        row_num += 1

    if item_exist:
        # update cell data
        logger.info("Updating CAT entry")
        date_cell = f"A{row_num}"
        qty_cell = f"E{row_num}"
        price_cell = f"E{row_num}"
        cogs_cell = f"F{row_num}"

        cat_sheet[date_cell] = date
        cat_sheet[qty_cell] = current_qty
        cat_sheet[price_cell] = average
        cat_sheet[cogs_cell] = average * 1.2

    if not item_exist:
        logger.info("Item is new, creating CAT entry")
        cat_sheet.append(
            {
                'A': date,
                'B': item,
                'C': quantity,
                'D': unit,
                'E': average,
                'F': average * 1.2
            }
        )

    price_cell_obj = cat_sheet.cell(row=row_num, column=5)
    price_cell_obj.number_format = RP_FORMAT

    cogs_cell_obj = cat_sheet.cell(row_num, 6)
    cogs_cell_obj.number_format = RP_FORMAT

    date_cell_obj = cat_sheet.cell(row_num, column=1)
    date_cell_obj.number_format = DATE_FORMAT

    purchase_wb.save(filename=file)
    purchase_wb.close()


def calc_totals(workbook: Workbook, item_name: str, logger=None):
    """Calculate average price for each item, total quantity, total units

    :param workbook: worksheet to read from
    :param item_name: name of item to check
    :param logger: logger pass through
    :return average
    """
    logger = logger if logger else getLogger()
    logger.info("Calculating totals...")
    row_count = 2
    price_count = 0
    qty_count = 0

    prices_list = []
    unit_list = []

    calc_sheets = ['Fresh', 'Sundries', 'Packaging']
    vendor_sheets = [_ for _ in workbook.sheetnames if _ not in calc_sheets]

    # Iterating through each worksheet to find all entries of item
    try:
        for vendor in vendor_sheets:
            ws = workbook[vendor]
            for row in ws.iter_rows(min_row=3, values_only=True):
                row_count += 1
                if row[1] == item_name:
                    logger.debug(f"Found entry in {ws}")

                    logger.debug(f"Found price: {row[4]}, qty: {row[2]}, "
                                 f"row: {row_count}")

                    # List for debugging purpose
                    # TODO: Remove for future release
                    prices_list.append(row[4])
                    unit_list.append(row[2])

                    price_count += row[4]
                    qty_count += row[2]
            row_count = 2

        logger.debug(
            f"""
Prices found: {prices_list}
Price avg : {price_count/qty_count}
Qty found: {unit_list}
Qty total: {qty_count}
            """
        )
        average = price_count/qty_count

        return average, qty_count
    except Exception as e:
        logger.error(f"ERROR: {e}")


# TODO: This Might not be needed going forward.
def update_formulas(excel_file):
    """This should take the materials in the 'Material - *' sheets and
    update any recipes using the listed ingredient's cost

    excel_file: path to file to edit
    """
    # Load the excel file
    workbook = openpyxl.load_workbook(excel_file)

    material_names = [
        "Material - Sundries",
        "Material - Fresh",
        "Material - Packaging"
    ]

    for sheets in material_names:
        worksheet: Worksheet = workbook[sheets]
        for row in range(6, worksheet.max_row):
            cell_value = worksheet.cell(row=row, column=2).value
            if cell_value:
                mat_name = cell_value
                mat_price_cell = worksheet.cell(row, 9).coordinate
                print(mat_name, mat_price_cell)


if __name__ == '__main__':
    wb = openpyxl.load_workbook("Pembelian 2020.xlsx")
    calc_totals(
        wb,
        "Cemara Minyak Goreng 1L"
    )

