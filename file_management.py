import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import sys
from shutil import copy2, make_archive, rmtree

from openpyxl import load_workbook
import pandas as pd

class FileManagement:
	""" Tools needed to deal files """

	def __init__(self):
		self.main = 'QB-Inventory-MultiStore-2018-Import.xlsx'

	def select_directory(self):
		""" Retruns string of directory selected """
		
		root = tk.Tk()
		root.withdraw()

		self.directory = Path(filedialog.askdirectory())
		root.destroy()

		return self.directory

	def verify_main_exists(self):
		""" Verify that necesary main file for export exists """

		self.main_spreadsheet = self.directory.parent.joinpath(self.main)
		if not self.main_spreadsheet.is_file():
			msg = self.main, ' is missing. Aborting.'
			print(msg)
			messagebox.showinfo('Error!', msg)
			sys.exit()

	def export_to_excel(self, dataframe):
		""" Append DataFrame to copy of main spreadsheet """

		export_filename = self.main_spreadsheet.stem + '-' + self.directory.name + '.xlsx'
		export_file = self.directory.parent.joinpath(export_filename)

		# make copy of main workbook
		copy2(self.main_spreadsheet, export_file)

		book = load_workbook(export_file)
		writer = pd.ExcelWriter(export_file, engine='openpyxl') 
		writer.book = book
		writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

		dataframe.to_excel(writer, index=False)

		writer.save()
		msg = 'Export Complete'
		print(msg)
		messagebox.showinfo('Info Message', msg)

	def archive_files(self):
		""" Compress the source folder of proccessed documents """

		archive_file = self.directory.parent.joinpath(self.directory.name + '-Completed')
		make_archive(archive_file, 'zip', self.directory)

		rmtree(self.directory)
		
		msg = 'Compression Complete'
		print(msg)
		messagebox.showinfo('Info Messege', msg)
