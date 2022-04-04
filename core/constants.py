from datetime import date
from dataclasses import dataclass

APP_VERSION = "v1.0.0"
DATE = date.today().strftime("%d-%b-%y")

CAT_REF = "excel_categories.txt"
DEFAULT_CATEGORIES = {
    "MISC": [
        "LIST",
        "ITEM LIST",
    ],
    "CATEGORIES": [
        "Fresh",
        "Sundries",
        "Packaging",
        "Utensils",
        "Appliances",
        "Cleaning",
        "Stationery",
        "Advertising",
        "Utility",
        "Storage",
        "Maintenance",
    ],
}

AVG_PRICE_FORMULA = """ =SUMPRODUCT(SUMIF(INDIRECT("'"&Vendors&"'!"&"B:B"),A[ROW], INDIRECT("'"&Vendors&"'!"&"J:J"))) \
/ SUMPRODUCT(COUNTIF(INDIRECT("'"&Vendors&"'!"&"B:B"), A[ROW]))
"""

@dataclass()
class ExcelItem:
    """Basic class to hold item data"""

    name: str = None
    vendor: str = None
    brand: str = None
    quantity: int = None
    unit: str = None
    cost: int = None
    isi: int = None
    isi_unit: str = None
    category: str = None
