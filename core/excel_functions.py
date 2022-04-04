import openpyxl

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font

from core.constants import ExcelItem, AVG_PRICE_FORMULA
from core.utils import get_logger, get_skip_list

# Today as 30-Mar-19
DATE_FORMAT = "dd-mmm-yy"

COMMA_FORMAT = "#,##0"
RP_FORMAT = u'_("Rp"* #,##0_);_("Rp"* (#,##0);_("Rp"* "-"_);_(@_)'

cat_sheets = {"LIST", "ITEM LIST", "Fresh", "Sundries", "Packaging", "Utensils", "Appliances", "Cleaning"}


def clean_item_names(vendor_sheet: Worksheet, logger=None):
    """Some entries have extra whitespace. This can mess with the cat entries, so we need to strip the names."""
    logger = logger if logger else get_logger("clean_item_names")

    for row in range(3, vendor_sheet.max_row + 1):
        item_name = vendor_sheet[f"B{row}"].value
        if not item_name:
            continue

        if item_name != item_name.strip():
            logger.debug(f"'{item_name}' is not clean, stripping to {item_name.strip()}")
            vendor_sheet[f"B{row}"] = item_name


# TODO: test that this works!
def create_category_sheet(workbook, category, logger=None):
    logger = logger if logger else get_logger("create_category_sheet")
    logger.info(f"Creating {category} in workbook")

    workbook.create_sheet(category)
    new_sheet: Worksheet = workbook[category]

    new_sheet["A1"] = "ITEM"
    new_sheet["A1"].font = Font(bold=True)
    new_sheet.merge_cells("A1:A2")

    new_sheet["B1"] = "UNIT"
    new_sheet["B1"].font = Font(bold=True)
    new_sheet.merge_cells("B1:B2")

    new_sheet["C1"] = "MOV AVER"
    new_sheet["C1"].font = Font(bold=True)
    new_sheet["C2"] = "PRICE/UNIT"
    new_sheet["C2"].font = Font(bold=True)


def init_catsheet(file, categories: dict, logger=None):
    """Clear out category sheets and recreate the entries"""
    logger = logger if logger else get_logger("init_catsheet")
    # Due to openpyxl's structure, we need the data_only=False wb to save formula
    input_wb = openpyxl.load_workbook(file, data_only=False)
    clean_category_sheets(categories, input_wb, logger)

    # default dict
    done_set = {"None", " "}
    skip_list = get_skip_list()

    # Iterate over all vendor sheets
    vendor_sheets = [_ for _ in input_wb.sheetnames if _ not in skip_list]
    logger.debug(f"VENDORS: {vendor_sheets}")
    for sheet_name in vendor_sheets:
        sheet: Worksheet = input_wb[sheet_name]
        logger.info(f"Sheet: {sheet}")

        clean_item_names(sheet, logger)
        vendor_items = next(sheet.iter_cols(min_col=2, max_col=2, min_row=3, values_only=True))
        for item in vendor_items:
            if not item or item in done_set:
                logger.debug(f"{item} is done, skipping")
                continue

            logger.debug(f"Look for '{item}' in {sheet_name}")
            row = vendor_items.index(item) + 3
            logger.debug(f"ROW: {row}, ITEM: {item}")
            excel_item = row_to_excel_item(sheet, row, logger)

            # Check if item is already in cat sheet
            category_items = next(input_wb[excel_item.category].iter_cols(1, 1, values_only=True))
            if item in category_items:
                logger.info("Item already in category, skipping")
                continue

            logger.info(f"Appending {excel_item.name} to {excel_item.category}")
            update_cat_avg(excel_item, input_wb, logger)
            done_set.add(item)
    input_wb.save(file)
    logger.info("All done with init")


def row_to_excel_item(sheet: Worksheet, row, logger=None):
    """Try to get data from row with clean up. If missing data, give defaults"""
    logger = logger if logger else get_logger("row_to_excel_item")

    item_name = sheet[f"B{row}"].value
    sheet_title = sheet.title

    # Guard against missing units
    try:
        isi_unit = sheet[f"I{row}"].value
        if not isi_unit:
            isi_unit = sheet[f"E{row}"].value
    except IndexError:
        logger.error("Isi error, assigning g")
        isi_unit = "g"

    # Check for common typos in categories
    try:
        category_value: str = sheet[f"K{row}"].value
    except IndexError:
        logger.error("Error getting Category, assigning Fresh")
        category_value = "Fresh"

    logger.debug(f"Category: {category_value}")
    return ExcelItem(name=item_name, vendor=sheet_title, isi_unit=isi_unit, category=category_value)


def clean_category_sheets(category_dict, input_wb, logger):
    # Clear out all category sheets, leaving the header only
    for category in category_dict["CATEGORIES"]:
        # Create all missing category sheets
        try:
            category_sheet = input_wb[category]
        except KeyError:
            logger.warning(f"{category} not in workbook!")
            create_category_sheet(input_wb, category, logger)
            category_sheet = input_wb[category]

        max_row = max(category_sheet.max_row, 3)
        logger.debug(f"Clearing {category} from 3 to {max_row}")
        category_sheet.delete_rows(3, max_row)


def write_to_excel(date, file, excel_item, logger=None):
    """Write the given data to the purchasing excel sheet

    :param str date: date of purchase
    :param str file: file path to excel sheet to edit
    :param excel_item: ExcelItem with data
    :type excel_item: ExcelItem
    :param logger: logger pass through
    """
    logger = logger if logger else get_logger("write_to_excel")

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
    input_vendor[f"G{input_row}"] = f"=D{input_row}*F{input_row}"
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
    update_cat_avg(excel_item, input_wb, logger)

    input_wb.save(file)


def update_cat_avg(excel_item, workbook, logger=None):
    """Calculate average price for each item, total quantity, total units
    Average formula template:
    SUM(
        SUMIF('[VENDORSHEET]'!B:B, A[ROW], '[VENDORSHEET]'!J:J),
        SUMIF('[VENDORSHEET]'!B:B, A[ROW], '[VENDORSHEET]'!J:J),
        ...
    )
    /
    SUM(
        COUNTIF('[VENDORSHEET]'!B:B, A[ROW]),
        COUNTIF('[VENDORSHEET]'!B:B, A[ROW]),
        ...
    )

    Note that this assumes J is the price/unit column, and B is the name column

    :param excel_item: ExcelItem with data
    :param workbook: workbook to read from
    :param logger: logger pass through
    :return: average
    """
    # Check for item in each ws
    # for each ws with item, add SUMIF to final formula

    # TODO: Have a "Vendors" named range in a "data" sheet
    #   Replace Formula with
    #  =SUMPRODUCT(SUMIF(INDIRECT("'"&Vendors&"'!"&"B:B"),A[ROW], INDIRECT("'"&Vendors&"'!"&"J:J")))
    #     / SUMPRODUCT(COUNTIF(INDIRECT("'"&Vendors&"'!"&"B:B"), A[ROW]))
    #  No longer need to count each vendor


    logger = logger if logger else get_logger("update_cat_average")

    category = excel_item.category
    vendor = excel_item.vendor
    logger.debug(f"Updating {excel_item.name} in {excel_item.category} with {excel_item.vendor}")

    # check if item in list
    cat_items = next(workbook[category].iter_cols(1, 1, values_only=True))
    if excel_item.name in cat_items:
        logger.debug("Item exists, checking vendor in formula")

        # compensate for 1 based index
        row = cat_items.index(excel_item.name) + 1
        avg_formula: str = workbook[category][f"C{row}"].value
        if not avg_formula:
            logger.debug("Item exists, but missing formula; Initializing...")
            init_formula(excel_item, workbook, logger, row)

        elif vendor in avg_formula:
            logger.debug("Vendor already in formula")

        else:
            logger.debug(f"Vendor is new [{vendor}], adding to formula")
            sumif_str = f"SUMIF('{vendor}'!B:B, A{row}, '{vendor}'!J:J),"
            countif_str = f"COUNTIF('{vendor}'!B:B, A{row}),"

            # add sumif to sum of dividend
            # add countif to sum of divisor
            # Rewrite formula back to wb
            sumif_formula = avg_formula.replace(")/", f"{sumif_str}) /")
            full_avg_formula = sumif_formula[:-1] + countif_str + ")"
            workbook[category][f"C{row}"] = full_avg_formula

    else:
        init_formula(excel_item, workbook, logger)


def init_formula(excel_item, workbook, logger=None, row=None):
    """Generate full average formula. Get the row as a check in the book."""
    logger.info("Item is new, adding and initializing formula")
    logger = logger if logger else get_logger("init_formula")
    category = excel_item.category

    # Set row to given, max_row, or minimum 3
    if not row:
        logger.debug(f"Creating {category} entry")
        workbook[category].append({"A": excel_item.name, "B": excel_item.isi_unit})
        row = workbook[category].max_row
    row = row if row > 3 else 3

    workbook[category][f"C{row}"] = AVG_PRICE_FORMULA


def transfer_records(old_workbook_path, new_workbook_path, categories: dict, logger=None):
    """Check entries from old to new, append any missing to new"""
    logger = logger if logger else get_logger()
    old_workbook = openpyxl.load_workbook(old_workbook_path, data_only=True)
    new_workbook = openpyxl.load_workbook(new_workbook_path, data_only=True)
    new_workbook_input = openpyxl.load_workbook(new_workbook_path, data_only=False)
    try:
        # Use old wb name as a fake vendor
        item_category = new_workbook_input["_IMPORT_"]
    except KeyError:
        new_workbook_input.create_sheet("_IMPORT_")
        item_category = new_workbook_input["_IMPORT_"]

    # Get item entries as sets
    logger.debug("Generating item lists...")
    logger.debug("Getting items from old workbook...")
    old_cat_items = get_items_in_category(old_workbook, categories, logger)
    logger.debug("Getting items from new workbook...")
    new_cat_items = get_items_in_category(new_workbook, categories, logger)

    # Append missing items to new workbook
    for item_name in old_cat_items.keys():
        if item_name not in new_cat_items.keys():
            logger.debug(f"Found missing item: {item_name.strip()}")
            item_column_details = {
                "B": item_name.strip(),
                "I": old_cat_items[item_name]["unit"],
                "J": old_cat_items[item_name]["unit_price"],
                "K": old_cat_items[item_name]["category"],
            }
            item_category.append(item_column_details)

    logger.debug("Saving and beginning init")
    new_workbook_input.save(new_workbook_path)
    init_catsheet(new_workbook_path, categories, logger)
    logger.debug("Finished transfer!")


def get_items_in_category(workbook, categories, logger=None):
    logger = logger if logger else get_logger("get_items_in_cat")
    # Get new entries
    category_items = {}
    logger.debug("Checking info from workbook")
    for category in categories["CATEGORIES"]:
        try:
            category_sheet: Worksheet = workbook[category]
        except KeyError:
            logger.warning(f"Could not find Worksheet '{category}'. Will skip this.")
            continue

        for row in range(3, category_sheet.max_row):
            item = {
                "category": category,
                "name": category_sheet[f"A{row}"].value,
                "unit": category_sheet[f"B{row}"].value,
                "unit_price": category_sheet[f"C{row}"].value,
            }
            category_items[item["name"]] = item

    return category_items
