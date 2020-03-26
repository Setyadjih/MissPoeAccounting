import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import NamedStyle

# Today as 30-Mar-19
DATE_FORMAT = "[$-en-US]d-mmm-yy;@"

RP_FORMAT = '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-'

rp_format = NamedStyle("Rupiah")
rp_format.number_format = '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-'


def write_to_excel(date, file, vendor, item, quantity, unit, cost, isi):
    """
    Write the given data to the purchasing excel sheet

    :param file: file path to excel sheet to edit
    :param vendor: Vendor WS to edit
    :param item: name of item
    :param quantity: # of items
    :param unit: unit for item quantity
    :param cost: Cost of purchase
    :param isi: how many units per item purchase
    """
    # Load excel file path
    purchase_wb = openpyxl.load_workbook(file)

    # Create vendor sheet if new
    vendor_sheet = purchase_wb[vendor]

    last_row = vendor_sheet.max_row + 1
    while not vendor_sheet.cell(row=last_row, column=2).value:
        last_row -= 1

    total_formula = f'=SUM(E{last_row}*C{last_row})'
    per_unit_forumla = f'=F{last_row}/G{last_row}'

    assign_dict = {
        'A': date,
        'B': item,
        'C': quantity,
        'D': unit,
        'E': cost,
        'F': total_formula,
        'G': isi,
        'H': per_unit_forumla
    }
    vendor_sheet.append(assign_dict)

    # format cells for Rupiah
    date_cell = vendor_sheet.cell(last_row, 1)
    date_cell.number_format = DATE_FORMAT

    cost_cell = vendor_sheet.cell(last_row, 5)
    cost_cell.number_format = RP_FORMAT

    total_cell = vendor_sheet.cell(last_row, 6)
    total_cell.number_format = RP_FORMAT

    per_unit_cell = vendor_sheet.cell(last_row, 8)
    per_unit_cell.number_format = RP_FORMAT

    purchase_wb.save(filename=file)
    purchase_wb.close()


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
            # mat_name = worksheet.cell(rows, 2)
            cell_value = worksheet.cell(row=row, column=2).value
            if cell_value:
                mat_name = cell_value
                mat_price_cell = worksheet.cell(row, 9).coordinate
                print(mat_name, mat_price_cell)


if __name__ == '__main__':
    update_formulas("Costing - Desserts (2019.11.20).xlsx")

