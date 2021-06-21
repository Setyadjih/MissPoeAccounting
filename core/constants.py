from datetime import date
from dataclasses import dataclass

APP_VERSION = "v0.2.16"
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
        "Storage",
    ],
}


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
