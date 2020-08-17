import openpyxl

from logging import getLogger

from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles.borders import Border, Side

# Today as 30-Mar-19
DATE_FORMAT = "dd-mmm-yy"

COMMA_FORMAT = "#,##0"
RP_FORMAT = u'_("Rp"* #,##0_);_("Rp"* (#,##0);_("Rp"* "-"_);_(@_)'


def init_catsheet(file, logger):
    logger = logger if logger else getLogger()
    # Load excel file path
    # Due to openpyxl's structure, we need the data_only=False wb to save
    # formula
    input_wb = openpyxl.load_workbook(file, data_only=False)

    cat_sheets = ["LIST", "ITEM LIST", "Fresh", "Sundries", "Packaging",
                  "Utensils", "Appliance"]
    done_list = ['None', '']

    # Iterate over all vendor sheets
    vendor_sheets = [_ for _ in input_wb.sheetnames if _ not in cat_sheets]
    for sheet_name in vendor_sheets:
        sheet: Worksheet = input_wb[sheet_name]
        logger.info(f"Sheet: {sheet}")

        logger.info("Starting processing")
        # Once the sheet is settled, start processing
        for row in sheet.iter_rows(min_row=3, max_row=sheet.max_row, values_only=True):
            item = row[1]
            logger.debug(f"ROW: {row}")

            # Early check done_list to skip checking in cat sheet
            # For some reason == None works while  (not item) doesn't??
            if item in done_list or item == None:
                continue
            logger.info(f"READING: {item}")

            # Try to get data from row. If missing data, give defaults
            try:
                isi_unit = row[7]
                if not isi_unit:
                    isi_unit = row[3]

                if type(isi_unit) != str or isi_unit == "kg":
                    isi_unit = "g"

                if isi_unit == "l":
                    isi_unit = "ml"
            except IndexError:
                logger.error("Isi error, assigning g")
                isi_unit = "g"

            try:
                corrections = {
                    "Utensil": "Utensils",
                    "Packing": "Packaging",
                    "Sundry": "Sundries"
                }
                cat: str = row[10]
                if not cat:
                    logger.debug("Assigning to default")
                    cat = "Fresh"
                cat = cat.strip().lower().capitalize()
                if cat in corrections.keys():
                    cat = corrections[cat]

            except IndexError:
                logger.error("category error, assigning Fresh")
                cat = "Fresh"
            logger.debug(f"Category: {cat}")
            cat_sheet = input_wb[cat]

            # Check if item is already in cat sheet
            for cat_row in cat_sheet.iter_rows(min_row=3, values_only=True):
                cat_item = cat_row[0]
                if cat_item == item:
                    logger.info("Item already in category, skipping")
                    continue

            logger.info(f"Appending {item} to sheet")
            update_cat(file, item, isi_unit, input_wb, cat, logger)

            done_list.append(item)

    logger.info("All done with init")


def write_to_excel(date, file, vendor, merek, item, quantity, unit, cost, isi,
                   isi_unit, category, logger=None):
    """
    Write the given data to the purchasing excel sheet

    :param date: date of purchase
    :param file: file path to excel sheet to edit
    :param vendor: Vendor WS to edit
    :param merek: item brand
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
    input_vendor[f"C{last_row}"] = merek
    input_vendor[f"D{last_row}"] = quantity
    input_vendor[f"E{last_row}"] = unit
    input_vendor[f"F{last_row}"] = cost
    input_vendor[f"G{last_row}"] = f'=C{last_row}*E{last_row}'
    input_vendor[f"H{last_row}"] = isi
    input_vendor[f"I{last_row}"] = isi_unit
    input_vendor[f"J{last_row}"] = f"=F{last_row}/G{last_row}"
    input_vendor[f"K{last_row}"] = category

    # format cells for Rupiah
    logger.debug("Assigning format strings")
    date_cell = input_vendor.cell(last_row, 1)
    date_cell.number_format = DATE_FORMAT

    cost_cell = input_vendor.cell(last_row, 6)
    cost_cell.number_format = RP_FORMAT

    total_cell = input_vendor.cell(last_row, 7)
    total_cell.number_format = RP_FORMAT

    isi_cell = input_vendor.cell(last_row, 8)
    isi_cell.number_format = COMMA_FORMAT

    per_unit_cell = input_vendor.cell(last_row, 9)
    per_unit_cell.number_format = RP_FORMAT

    update_cat(file, item, isi_unit, input_wb, category, logger)


def update_cat(file, item, isi_unit, input_wb, category, logger):

    # Append to costing according to category
    try:
        cat_sheet = input_wb[category]
    except KeyError:
        logger.debug(f"{category} not found, creating")
        input_wb.create_sheet(category)
        cat_sheet: Worksheet = input_wb[category]
        cat_sheet['A1'] = category.upper()

        cat_sheet['A2'] = 'MATERIAL'
        cat_sheet['B2'] = 'UNIT'
        cat_sheet['C2'] = 'PRICE'

        # Apply style to docs
        for i in range(1, 4):
            cell = cat_sheet.cell(row=2, column=i)
            cell.border = Border(bottom=Side(style='thick'))

    input_wb.save(file)

    logger.debug(f"Assigning {item} to {category}")
    # average = "=SUM(VENDOR!A1+VENDOR!B3....)/(number of vendors)
    # This workbook is to parse data from formulas (SEPERATE FROM INPUT WB)
    value_wb = openpyxl.load_workbook(file, data_only=True)
    average = calc_totals(value_wb, item, logger)
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

    value_wb.close()

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
    price_count = "SUM("
    entry_count = 0

    try:
        for vendor in workbook.sheetnames:
            ws = workbook[vendor]

            # Do not read from category sheets
            if ws.title in calc_sheets:
                continue

            for row in ws.iter_rows(min_row=4, values_only=True):
                row_count += 1
                if row[1] == item_name:
                    logger.debug(f"Found: {ws.title}, ROW: {row_count}")
                    entry_count += 1

                    # price/unit is already calculated, add it to running
                    price_cell = ws.cell(row_count, column=10).coordinate
                    price_count += f"+'{ws.title}'!{price_cell}"

            # reset row count for next ws
            row_count = 2

        # Close SUM brackets
        price_count += ")"
        avg_formula = f'={price_count}/{entry_count}'
        logger.info(f"returning {avg_formula}")

        return avg_formula
    except Exception as e:
        logger.error(f"ERROR: {e}")
