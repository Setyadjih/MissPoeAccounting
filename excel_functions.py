import openpyxl

from logging import getLogger

from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import numbers, Font, Alignment
from openpyxl.styles.borders import Border, Side

# Today as 30-Mar-19
DATE_FORMAT = "dd-mmm-yy"

COMMA_FORMAT = "#,##0"
RP_FORMAT = u'_("Rp"* #,##0_);_("Rp"* (#,##0);_("Rp"* "-"_);_(@_)'


def write_to_excel(date, file, vendor, item, quantity, unit, cost, isi,
                   isi_unit, category, logger=None):
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
    :param isi_unit: unit for isi
    :param category: category of purchase
    :param logger: logger pass through
    """
    logger = logger if logger else getLogger()
    # Load excel file path
    # Due to openpyxl's structure, we need the data_only=False wb to save
    # formula
    input_wb = openpyxl.load_workbook(file, data_only=False)

    # Create vendor sheet if new
    input_vendor = input_wb[vendor]

    last_row = input_vendor.max_row + 1
    logger.debug(f"last row = {last_row}")

    # check for empty row error
    while not input_vendor[f"B{last_row-1}"].value:
        logger.debug("Previous row empty, going up one")
        last_row -= 1

    logger.debug(f"Appending item data")

    input_vendor[f"A{last_row}"] = date
    input_vendor[f"B{last_row}"] = item
    input_vendor[f"C{last_row}"] = quantity
    input_vendor[f"D{last_row}"] = unit
    input_vendor[f"E{last_row}"] = cost
    input_vendor[f"F{last_row}"] = f'=C{last_row}*E{last_row}'
    input_vendor[f"G{last_row}"] = isi
    input_vendor[f"H{last_row}"] = isi_unit
    input_vendor[f"I{last_row}"] = f"=F{last_row}/G{last_row}"
    input_vendor[f"J{last_row}"] = category

    # format cells for Rupiah
    logger.debug("Assigning format strings")
    date_cell = input_vendor.cell(last_row, 1)
    date_cell.number_format = DATE_FORMAT

    cost_cell = input_vendor.cell(last_row, 5)
    cost_cell.number_format = RP_FORMAT

    total_cell = input_vendor.cell(last_row, 6)
    total_cell.number_format = RP_FORMAT

    isi_cell = input_vendor.cell(last_row, 7)
    isi_cell.number_format = COMMA_FORMAT

    per_unit_cell = input_vendor.cell(last_row, 8)
    per_unit_cell.number_format = RP_FORMAT

    # Append to costing according to category
    logger.debug(f"Assigning to {category}")
    try:
        cat_sheet = input_wb[category]
    except KeyError:
        input_wb.create_sheet(category)
        cat_sheet: Worksheet = input_wb[category]
        cat_sheet['A1'] = category.upper()
        cat_sheet['B1'] = 'Last Purchase'
        cat_sheet.merge_cells('B1:C1')
        cat_sheet['B1'].font = Font(bold=True)

        cat_sheet['B2'] = 'MATERIAL'
        cat_sheet['D2'] = 'UNIT'
        cat_sheet['E2'] = 'PRICE'

        # Apply style to docs
        for i in range(1, 11):
            cell = cat_sheet.cell(row=2, column=i)
            cell.border = Border(bottom=Side(style='thick'))

    input_wb.save(file)

    # average = "=SUM(VENDOR!A1+VENDOR!B3....)/(number of vendors)
    # This workbook is to parse data from formulas (SEPERATE FROM INPUT WB)
    purchase_wb = openpyxl.load_workbook(file, data_only=True)
    average = calc_totals(purchase_wb, item, logger)
    cs = cat_sheet.iter_rows(min_row=3, min_col=1, max_col=1, values_only=True)

    # check if item already in sheet
    # Row num at three due to Excel sheet format
    item_exist = False
    row_num = 3

    # Check for item
    for row in cs:
        item_name = row[0]
        if item == item_name:
            item_exist = True
            break
        row_num += 1

    if item_exist:
        # update cell data
        logger.info("Updating CAT entry")
        price_cell = f"C{row_num}"
        cat_sheet[price_cell] = average

    if not item_exist:
        logger.info("Item is new, creating CAT entry")
        cat_sheet.append(
            {
                'A': item,
                'B': isi_unit,
                'C': average,
            }
        )

    price_cell_obj = cat_sheet.cell(row=row_num, column=3)
    price_cell_obj.number_format = RP_FORMAT

    purchase_wb.close()

    input_wb.save(filename=file)
    input_wb.close()
    logger.info("Finished writing to workbook")


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
    calc_sheets = ['Fresh', 'Sundries', 'Packaging', 'Appliance', 'Utensils']

    # Iterating through each worksheet to find all entries of item
    logger.debug(f"Beginning iteration")
    qty_count = "SUM("
    price_count = "SUM("
    try:
        for vendor in workbook.sheetnames:
            ws = workbook[vendor]
            if ws.title in calc_sheets:
                continue
            for row in ws.iter_rows(min_row=3, values_only=True):
                row_count += 1
                if row[1] == item_name:
                    logger.debug(f"Found entry in {ws.title}")

                    # Quantity and unit check
                    qty_cell = ws.cell(row_count, column=7).coordinate
                    unit_cell = ws.cell(row_count, column=8).coordinate

                    # set defaults for isi
                    if not ws[unit_cell].value or ws[qty_cell].value:
                        ws[qty_cell] = 0

                        ws[unit_cell] = "g"

                    quantity = ws[qty_cell].value
                    unit = ws[unit_cell].value

                    # unit modification
                    if unit.lower() == "kg":
                        unit = "g"
                        quantity *= 1000

                    if unit.lower() == "l":
                        unit = "ml"
                        quantity *= 1000

                    ws[unit_cell] = unit
                    ws[qty_cell] = quantity

                    qty_count += f"+'{ws.title}'!{qty_cell}"

                    price_cell = ws.cell(row_count, column=5).coordinate
                    logger.debug(f"Price cell: {price_cell}")

                    price_count += f"+'{ws.title}'!{price_cell}"

            # reset row count for next ws
            row_count = 2

        # Close SUM brackets
        qty_count += ")"
        price_count += ")"

        avg_formula = f'={price_count}/{qty_count}'
        logger.info(f"returning {avg_formula}")

        return avg_formula
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
