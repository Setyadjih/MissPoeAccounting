from pathlib import Path
import shutil
import os

from core.excel_functions import transfer_records
from core.constants import DEFAULT_CATEGORIES


def main():
    orig_wb_path = r"D:\Miss Poe\Costings\tests\_test_resources\transfer_records\Pembelian 2021_ORIG.xlsx"

    old_wb_path = r"D:\Miss Poe\Costings\tests\_test_resources\transfer_records\Pembelian 2020.xlsx"
    new_wb_path = r"D:\Miss Poe\Costings\tests\_test_resources\transfer_records\Pembelian 2021.xlsx"
    transfer_records(old_wb_path, new_wb_path, categories=DEFAULT_CATEGORIES)

    # Save test result to new name, save
    test_result_name = Path(new_wb_path).with_name(Path(new_wb_path).stem + "_TEST_RESULT.xlsx")
    if test_result_name.exists():
        os.remove(test_result_name)
    Path(new_wb_path).rename(test_result_name)
    shutil.copy(orig_wb_path, new_wb_path)


if __name__ == "__main__":
    main()
