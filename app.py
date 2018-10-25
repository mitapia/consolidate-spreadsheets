import pandas as pd
import xlrd
from sqlalchemy import create_engine

# Create DB engine.
engine = create_engine('sqlite:///testing.db')

files_dir = './source/'
Store01_file = '1001-Berry-2018-Inventory-Count.xlsx'
Store02_file = '1002-Lancaster-2018-Inventory-Count.xlsx'
Store03_file = '1003-Arlington-2018-Inventory-Count.xlsx'
# not in used
# Store04_file = '1004-Jefferson-2018-Inventory-Count.xlsx'
Store05_file = '1005-HarryHines-2018-Inventory-Count.xlsx'

final_xls = './QB-MultiStore-2018-Import.xls'
store_file = './sample.xlsx'

store_id = 'Qty01'

product_info_headers = ['Style', 'Color', 'Online_Color']
inventory_df = pd.read_excel('./sample_worksheets/sample.xlsx')

for row in inventory_df.iterrows():
	product = row[1].dropna()	# Removes empty values

	# loads style info into DataFrame and sets index to 0 so we can join this later
	prduct_info_df = pd.DataFrame(
						[product.filter(product_info_headers)]
					).rename(
						{row[0]: 0}, axis='index'
					)

	#inv = product.drop(style_).value_counts()
	product_qty = product.drop(product_info_headers).value_counts()

	for item in product_qty.items():
		product_qty_df = pd.DataFrame([item], columns=['Item_Size', store_id])
		product_df = prduct_info_df.join(product_qty_df)

		# check for an existing entrie
		sql_statement = 'SELECT * FROM inventory'
						+' WHERE Style='+ product_df.at[0, 'Style']
						+' AND Online_Color='+ product_df.at[0, 'Online_Color']
						+' AND Item_Size='+ product_df.at[0, 'Item_Size']
		# not using EXISTS
		query_for_existance 	   = pd.read_sql_query(sql_statement, con=engine)
		number_of_records_returned = len(query_for_existance.index)

		if number_of_records_returned == 0:
			product_df.to_sql('inventory', con=engine, if_exists='append', index=False)
		elif number_of_records_returned == 1:
			pass
			# sql = """
			#     UPDATE inventory AS inv
			#     SET store_id = 
			#     FROM temp_table AS t
			#     WHERE f.id = t.id
			# """

			# with engine.begin() as conn:     # TRANSACTION
			#     conn.execute(sql)
