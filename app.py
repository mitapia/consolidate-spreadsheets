import pandas as pd

from database import Database
from file_management import FileManagement

"""
	Final Worksheet columns:
	Style
	Color
	Online_Color
	Item_Size
	1090-Warehouse-Qty
	1001-Berry-Qty
	1002-Lancaster-Qty
	1003-Arlington-Qty
	1004-Jefferson-Qty
	1005-HarryHines-Qty

"""

file = FileManagement()
source_directory = file.select_directory()

product_info_headers = ['Style', 'Color', 'Online_Color']
store_files = {
	# Name on column	  :  Corresponding filename
	'1090-Warehouse-Qty'  : '1090-Warehouse-2018-Inventory-Count.xlsx',
	'1001-Berry-Qty' 	  : '1001-Berry-2018-Inventory-Count.xlsx',
	'1002-Lancaster-Qty'  : '1002-Lancaster-2018-Inventory-Count.xlsx',
	'1003-Arlington-Qty'  : '1003-Arlington-2018-Inventory-Count.xlsx',
	'1004-Jefferson-Qty'  : '1004-Jefferson-2018-Inventory-Count.xlsx',
	'1005-HarryHines-Qty' : '1005-HarryHines-2018-Inventory-Count.xlsx'
}

# be sure main spreadsheet exists
file.verify_main_exists()

# create new database tabel to store inventory items
inventory_db = Database()

for store_id, filename in store_files.items():

	current_file = source_directory.joinpath(filename)

	# check for existane of file
	if not current_file.is_file():
		# skip to next look if does not exists
		print(filename, ' is missing. It will be skipped.')
		continue

	print(store_id, ' file was found and is being processed.')

	inventory_df = pd.read_excel(current_file)

	for row in inventory_df.iterrows():
		product = row[1].dropna()	# Removes empty values

		product_info_s = pd.Series(product.filter(product_info_headers))
		product_qty = product.drop(product_info_headers).value_counts()

		for item in product_qty.items():
			product_qty_s = pd.Series(item, index=['Item_Size', store_id])
			product_s = product_info_s.append(product_qty_s)

			inventory_db.add_product(product_s.to_dict(), store_id)

full_inventory = pd.read_sql_table('inventory', inventory_db.engine)
file.export_to_excel(full_inventory)
file.archive_files()
