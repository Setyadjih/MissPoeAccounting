from datetime import date
from dataclasses import dataclass

APP_VERSION = 'v0.2.12'
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
        "Stationary",
        "Advertising",
        "Utility",
    ]
}


@dataclass
class ExcelItem:
    """Basic class to hold item data"""
    name: str
    vendor: str
    brand: str
    quantity: int
    unit: str
    cost: int
    isi: int
    isi_unit: str
    category: str
