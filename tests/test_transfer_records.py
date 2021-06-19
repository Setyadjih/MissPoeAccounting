from core.excel_functions import transfer_records
from core.constants import DEFAULT_CATEGORIES


def main():
    old_wb_path = r"D:\Miss Poe\Costings\tests\_test_resources\transfer_records\Pembelian 2020.xlsx"
    new_wb_path = r"D:\Miss Poe\Costings\tests\_test_resources\transfer_records\Pembelian 2021.xlsx"
    transfer_records(old_wb_path, new_wb_path, categories=DEFAULT_CATEGORIES)


if __name__ == '__main__':
    main()
