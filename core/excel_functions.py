import openpyxl
from logging import getLogger

from openpyxl.worksheet.worksheet import Worksheet

from core.constants import ExcelItem

# Today as 30-Mar-19
DATE_FORMAT = "dd-mmm-yy"

COMMA_FORMAT = "#,##0"
RP_FORMAT = u'_("Rp"* #,##0_);_("Rp"* (#,##0);_("Rp"* "-"_);_(@_)'

cat_sheets = {"LIST", "ITEM LIST", "Fresh", "Sundries", "Packaging",
              "Utensils", "Appliances", "Cleaning"}


def init_catsheet(file, categories: dict, logger):
    logger = logger if logger else getLogger()
    # Load excel file path
    # Due to openpyxl's structure, we need the data_only=False wb to save
    # formula
    input_wb = openpyxl.load_workbook(file, data_only=False)

    # Clear out all category sheets, leaving the header only
    for category in categories["CATEGORIES"]:
        category_sheet = input_wb[category]
        max_row = max(category_sheet.max_row, 3)
        logger.debug(f"Clearing {category} from 3 to {max_row}")
        category_sheet.delete_rows(3, max_row)
    input_wb.save(file)

    # default dict
    done_set = {"None", " "}
    skip_list = categories["CATEGORIES"] + categories["MISC"]

    # Iterate over all vendor sheets
    vendor_sheets = [_ for _ in input_wb.sheetnames if _ not in skip_list]
    logger.debug(f"VENDORS: {vendor_sheets}")
    for sheet_name in vendor_sheets:
        sheet: Worksheet = input_wb[sheet_name]
        logger.info(f"Sheet: {sheet}")
        items = next(sheet.iter_cols(min_col=2, max_col=2, min_row=3, values_only=True))
        for item in items:
            # Early check done_list to skip checking in cat sheet
            if not item or item in done_set:
                logger.debug("Skipping item")
                continue

            row = items.index(item) + 3
            logger.debug(f"ROW: {row}, item: {item}")

            # Try to get data from row. If missing data, give defaults
            try:
                isi_unit = sheet[f"I{row}"].value
                if not isi_unit:
                    isi_unit = sheet[f"E{row}"].value

            except IndexError:
                logger.error("Isi error, assigning g")
                isi_unit = "g"

            # Check for common typos in categories
            try:
                categ: str = sheet[f"K{row}"].value
                if not categ:
                    logger.debug("Assigning to default")
                    categ = "Fresh"

                corrections = {
                    "Utensil": "Utensils",
                    "Packing": "Packaging",
                    "Sundry": "Sundries",
                    "Alat tulis": "Stationary",
                    "Stationery": "Stationary",
                    "Appliance": "Appliances"
                }

                category_check = categ.strip().lower().capitalize()
                if category_check in corrections.keys():
                    categ = corrections[category_check]

            except IndexError:
                logger.error("category error, assigning Fresh")
                categ = "Fresh"

            logger.debug(f"Category: {categ}")

            # Check if item is already in cat sheet
            cat_items = next(input_wb[categ].iter_cols(1, 1, values_only=True))
            if item in cat_items:
                logger.info("Item already in category, skipping")
                continue

            logger.info(f"Appending {item} to {categ}")
            excel_item = ExcelItem(
                name=item, vendor=sheet_name, isi_unit=isi_unit, category=categ
            )
            update_cat_avg(excel_item, input_wb, skip_list, logger)
            done_set.add(item)
    input_wb.save(file)
    logger.info("All done with init")


def write_to_excel(skips, date, file, excel_item, logger=None):
    """ Write the given data to the purchasing excel sheet

    :param skips sheets to skip
    :type skips: List[str]
    :param str date: date of purchase
    :param str file: file path to excel sheet to edit
    :param excel_item: ExcelItem with data
    :type excel_item: ExcelItem
    :param logger: logger pass through
    """
    logger = logger if logger else getLogger()

    # Load excel file path
    # Need the data_only=False wb to save formula
    input_wb = openpyxl.load_workbook(file, data_only=False)

    # Create vendor sheet if new
    input_vendor = input_wb[excel_item.vendor]
    input_row = input_vendor.max_row + 1

    # iterate backwards until last_row is after a row with data
    while not input_vendor[f"B{input_row-1}"].value:
        input_row -= 1

    # Hard coded minimum to not clash with merged cells:
    if input_row < 3:
        input_row = 3

    logger.debug(f"max row = {input_vendor.max_row}, input row = {input_row}")
    logger.debug(f"Appending item data")
    input_vendor[f"A{input_row}"] = date
    input_vendor[f"B{input_row}"] = excel_item.name
    input_vendor[f"C{input_row}"] = excel_item.brand
    input_vendor[f"D{input_row}"] = excel_item.quantity
    input_vendor[f"E{input_row}"] = excel_item.unit
    input_vendor[f"F{input_row}"] = excel_item.cost
    input_vendor[f"G{input_row}"] = f'=D{input_row}*F{input_row}'
    input_vendor[f"H{input_row}"] = excel_item.isi
    input_vendor[f"I{input_row}"] = excel_item.isi_unit
    input_vendor[f"J{input_row}"] = f"=G{input_row}/H{input_row}"
    input_vendor[f"K{input_row}"] = excel_item.category

    # format cells for Rupiah
    logger.debug("Assigning format strings")
    date_cell = input_vendor.cell(input_row, 1)
    date_cell.number_format = DATE_FORMAT

    cost_cell = input_vendor.cell(input_row, 6)
    cost_cell.number_format = RP_FORMAT

    total_cell = input_vendor.cell(input_row, 7)
    total_cell.number_format = RP_FORMAT

    isi_cell = input_vendor.cell(input_row, 8)
    isi_cell.number_format = COMMA_FORMAT

    per_unit_cell = input_vendor.cell(input_row, 10)
    per_unit_cell.number_format = RP_FORMAT

    logger.debug(f"Assigning {excel_item.name} to {excel_item.category}")
    update_cat_avg(excel_item, input_wb, skips, logger)

    input_wb.save(file)


def update_cat_avg(excel_item, workbook, skips, logger=None):
    """Calculate average price for each item, total quantity, total units
    Average formula template:
    SUM(
        SUMIF('[VENDORSHEET]'!B:B, A[ROW], '[VENDORSHEET]'!J:J),
        SUMIF('[VENDERSHEET]'!....
    )
    /
    SUM(
        COUNTIF('[VENDORSHEET]'!B:B, A[ROW]),
        COUNTIF('[VENDORSHEET]'!....
    )
    Note that this assumes J is the price/unit column, and B is the name column
    :param excel_item: ExcelItem with data
    :param workbook: workbook to read from
    :param skips: sheets to avoid
    :param logger: logger pass through
    :return average
    """
    # Check for item in each ws
    # for each ws with item, add SUMIF to final formula
    logger = logger if logger else getLogger()

    category = excel_item.category
    vendor_check = excel_item.vendor

    # check if item in list
    cat_items = next(workbook[category].iter_cols(1, 1, values_only=True))
    if excel_item.name in cat_items:
        logger.debug("Item exists, checking vendor in formula")

        # compensate for 1 based index
        row = cat_items.index(excel_item.name) + 1
        avg_formula: str = workbook[category][f"C{row}"].value
        if not avg_formula:
            logger.debug("Item exists, but missing formula; Initializing...")
            init_formula(excel_item, workbook, skips, logger, row)

        elif vendor_check in avg_formula:
            logger.debug("Vendor already in formula")

        else:
            logger.debug("Vendor is new, adding to formula")
            sumif_str = f"SUMIF('{vendor_check}'!B:B, A{row}, '{vendor_check}'!J:J),"
            countif_str = f"COUNTIF('{vendor_check}'!B:B, A{row}),"

            # add sumif to sum of dividend
            # add countif to sum of divisor
            # Rewrite formula back to wb
            sumif_formula = avg_formula.replace(")/", f"{sumif_str}) /")
            full_avg_formula = sumif_formula[:-1] + countif_str + ")"
            workbook[category][f"C{row}"] = full_avg_formula

    else:
        logger.debug("Item is new, adding and initializing formula")
        init_formula(excel_item, workbook, skips, logger)


def init_formula(excel_item, workbook, skips, logger=None, row=None):
    """Generate full average formula. Get the row as a check in the book."""
    logger = logger if logger else getLogger()
    category = excel_item.category

    if not row:
        logger.info(f"Item is new, creating {category} entry")
        workbook[category].append({'A': excel_item.name, 'B': excel_item.isi_unit})
        row = workbook[category].max_row

    else:
        logger.info("Item exists, creating average formula...")

    if row < 3:
        row = 3

    # Iterating through each worksheet to find all vendors with item
    logger.debug(f"Beginning iteration")
    price_count = ""
    entry_count = ""

    try:
        vendors = [_ for _ in workbook.sheetnames if _ not in skips]
        # Check each vendor for item
        for vendor in vendors:
            items = next(workbook[vendor].iter_cols(2, 2, values_only=True))
            if excel_item.name in items:
                price_count += f"SUMIF('{vendor}'!B:B, A{row}, '{vendor}'!J:J),"
                entry_count += f"COUNTIF('{vendor}'!B:B, A{row}),"

        # Combine average formula and apply to workbook
        avg_formula = f"=SUM({price_count})/SUM({entry_count})"
        workbook[category][f"C{row}"] = avg_formula

        price_cell_obj = workbook[category].cell(row=row, column=3)
        price_cell_obj.number_format = RP_FORMAT
    except Exception as e:
        logger.error(f"ERROR: {e}")


def transfer_records(old_workbook_path, new_workbook_path, categories: dict, logger=None):
    """Check entries from old to new, append any missing to new"""
    logger = logger if logger else getLogger()
    old_workbook = openpyxl.load_workbook(old_workbook_path, data_only=True)
    new_workbook = openpyxl.load_workbook(new_workbook_path, data_only=True)

    # Get item entries as sets
    logger.debug("Generating item lists")
    old_cat_items = get_items_in_category(old_workbook, categories, logger)
    new_cat_items = get_items_in_category(new_workbook, categories, logger)

    # Create row dict for items not in new workbook
    missing_items = []
    for item_name in old_cat_items.keys():
        if item_name not in new_cat_items.keys():
            logger.debug(f"Found missing item: {item_name}")
            missing_items.append({
                "B": item_name,
                "I": old_cat_items[item_name]["unit"],
                "J": old_cat_items[item_name]["unit_price"],
                "K": old_cat_items[item_name]["category"]
            })

    # Copy missing data from old to new
    new_workbook = openpyxl.load_workbook(new_workbook_path)
    for item in missing_items:
        try:
            # Use old wb name as a fake vendor
            item_category = new_workbook["_IMPORT_"]
        except KeyError:
            new_workbook.create_sheet("_IMPORT_")
            item_category = new_workbook["_IMPORT_"]

        item_category.append(item)

    logger.debug("Saving and beginning init")
    new_workbook.save(new_workbook_path)
    init_catsheet(new_workbook_path, categories, logger)
    logger.debug("Finished transfer!")


def get_items_in_category(workbook, categories, logger):
    # Get new entries
    category_items = {}
    logger.debug("Checking info from workbook")
    for category in categories["CATEGORIES"]:
        category_sheet: Worksheet = workbook[category]
        for row in range(3, category_sheet.max_row):
            item = {
                "category": category,
                "name": category_sheet[f'A{row}'].value,
                "unit": category_sheet[f'B{row}'].value,
                "unit_price": category_sheet[f'C{row}'].value,
            }
            category_items[item['name']] = item

    return category_items
