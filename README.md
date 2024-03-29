# Excel Automator for Miss Poe
A PySide application to automate Excel record keeping and accounting. Primarily designed for use by Ernawati Poedijono, owner of Miss Poe cafe in Indonesia. The design of the application was made in close cooperation with her, and feedback from other users of the application

## How it works
The application dynamically generates the vendor and item list based on the excel sheet, using a txt file editable by users for specific category names. These names identify the category worksheets in the workbook, to differentiate from the vendor sheets. 

The application also allows for quick initialization of all items in the vendor sheets, using Excel macros to avoid tedious recalculation. After an item is input into the category sheet, it's rolling price average will be updated as more entries of purchase are added to the vendor sheet.

Item purchase input can also be handled through the program, to better avoid typos and missing data entries.
