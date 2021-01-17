from datetime import date

APP_VERSION = 'v0.2.10'
DATE = date.today().strftime("%d-%b-%y")

CAT_REF = "excel_categories.txt"
DEFAULT_CATEGORIES = """[MISC]
LIST
ITEM LIST

[CATEGORIES]
Fresh
Sundries
Packaging
Utensils
Appliances
Cleaning
Stationary
Advertising
"""


class ExcelItem:
    """Basic class to hold item data"""
    def __init__(
        self,
        name=None,
        vendor=None,
        brand=None,
        quantity=None,
        unit=None,
        cost=None,
        isi=None,
        isi_unit=None,
        category=None
    ):
        self.name = name
        self.vendor = vendor
        self.brand = brand
        self.quantity = quantity
        self.unit = unit
        self.cost = cost
        self.isi = isi
        self.isi_unit = isi_unit
        self.category = category
