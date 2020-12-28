import openpyxl

from logging import getLogger

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles.borders import Border, Side

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

    # default dict
    done_set = {"None", " "}
    skip_list = categories["CATEGORIES"] + categories["MISC"]

    # Iterate over all vendor sheets
    vendor_sheets = [_ for _ in input_wb.sheetnames if _ not in skip_list]
    logger.debug(f"VENDORS: {vendor_sheets}")
    for sheet_name in vendor_sheets:
        sheet: Worksheet = input_wb[sheet_name]
        logger.info(f"Sheet: {sheet}")

        logger.info("Starting processing...")
        # Once the sheet is settled, start processing
        items = next(sheet.iter_cols(min_col=2, max_col=2, min_row=3, values_only=True))
        for item in items:
            # Early check done_list to skip checking in cat sheet
            if not item or item in done_set:
                logger.debug("Skipping item")
                continue

            row = items.index(item) + 3
            logger.debug(f"ROW: {row}")
            logger.info(f"READING: {item}")

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
                corrections = {
                    "Utensil": "Utensils",
                    "Packing": "Packaging",
                    "Sundry": "Sundries",
                    "Alat tulis": "Stationary",
                    "Stationery": "Stationary",
                    "Appliance": "Appliances"
                }
                cat: str = sheet[f"K{row}"].value
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

            # Check if item is already in cat sheet
            cat_items = next(input_wb[cat].iter_cols(1, 1, values_only=True))
            if item in cat_items:
                logger.info("Item already in category, skipping")
                continue

            logger.info(f"Appending {item} to {cat}")
            update_cat(skip_list, file, item, sheet_name, isi_unit, input_wb, cat, logger)

            done_set.add(item)
    logger.info("All done with init")


def write_to_excel(skips: list, date, file, vendor, merek, item,
                   quantity, unit, cost, isi, isi_unit, category, logger=None):
    """
    Write the given data to the purchasing excel sheet

    :param skips sheets to skip
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
    logger.debug(f"Appending item data")

    input_vendor[f"A{last_row}"] = date
    input_vendor[f"B{last_row}"] = item
    input_vendor[f"C{last_row}"] = merek
    input_vendor[f"D{last_row}"] = quantity
    input_vendor[f"E{last_row}"] = unit
    input_vendor[f"F{last_row}"] = cost
    input_vendor[f"G{last_row}"] = f'=D{last_row}*F{last_row}'
    input_vendor[f"H{last_row}"] = isi
    input_vendor[f"I{last_row}"] = isi_unit
    input_vendor[f"J{last_row}"] = f"=G{last_row}/H{last_row}"
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

    update_cat(skips, file, item, vendor, isi_unit, input_wb, category, logger)


def update_cat(skips, file, item, vendor, isi_unit, input_wb, category, logger):
    # Append to costing according to category
    if category not in input_wb.sheetnames:
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

    # Handle cat sheet updating
    update_avg_formula(item, isi_unit, category, vendor, input_wb, skips, logger)

    input_wb.save(filename=file)
    logger.info("Finished writing to workbook")


def update_avg_formula(item, isi_unit, category, vendor_check, workbook, skips, logger=None):
    """Calculate average price for each item, total quantity, total units
    Average formula template:
    SUM(
        SUMIF([VENDORSHEET]!B:B, A[ROW], [VENDORSHEET]!J:J),
        SUMIF([VENDERSHEET]!....
    )
    /
    SUM(
        COUNTIF([VENDORSHEET]!B:B, A[ROW]),
        COUNTIF([VENDORSHEET]!....
    )
    :param item: name of item to check
    :param isi_unit: unit of item
    :param category: item category
    :param vendor_check: vendor to check
    :param workbook: workbook to read from
    :param skips: sheets to avoid
    :param logger: logger pass through
    :return average
    """
    # Check for item in each ws
    # for each ws with item, add SUMIF to final formula
    logger = logger if logger else getLogger()

    # check if item in list
    cat_items = next(workbook[category].iter_cols(1, 1, values_only=True))
    if item in cat_items:
        logger.debug("Item exists, checking vendor in formula")
        row = cat_items.index(item)
        avg_formula: str = workbook[category][f"C{row}"].value

        if vendor_check in avg_formula:
            logger.debug("Vendor in formula, returning")
            return
        else:
            logger.debug("Vendor is new, adding to formula")
            sumif_str = f"SUMIF('{vendor_check}'!B:B, A{row}, '{vendor_check}'!J:J),"
            countif_str = f"COUNTIF('{vendor_check}'!B:B, A{row}),"

            # Insert at divisor
            avg_formula = avg_formula.replace(") /", f"{sumif_str}) /")

            # add count to divisor sum
            avg_formula = avg_formula[:-1] + countif_str + ")"

            # Rewrite formula back to wb
            workbook[category][f"C{row}"] = avg_formula

    else:
        logger.info(f"Item is new, creating {category} entry")
        workbook[category].append(
            {
                'A': item,
                'B': isi_unit,
            }
        )
        row = workbook[category].max_row
        # Iterating through each worksheet to find all vendors with item
        logger.debug(f"Beginning iteration")
        price_count = ""
        entry_count = ""

        try:
            vendors = [_ for _ in workbook.sheetnames if _ not in skips]
            # Check each vendor for item
            for vendor in vendors:
                items = next(workbook[vendor].iter_cols(2, 2, values_only=True))
                if item in items:
                    price_count += f"SUMIF('{vendor}'!B:B, A{row}, '{vendor}'!J:J),"
                    entry_count += f"COUNTIF('{vendor}'!B:B, A{row}),"

            # Combine average formula and apply to workbook
            avg_formula = f"=SUM({price_count})/SUM({entry_count})"
            workbook[category][f"C{row}"] = avg_formula

            price_cell_obj = workbook[category].cell(row=row, column=3)
            price_cell_obj.number_format = RP_FORMAT
        except Exception as e:
            logger.error(f"ERROR: {e}")
