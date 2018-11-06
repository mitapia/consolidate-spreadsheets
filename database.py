from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, func
from sqlalchemy.sql import select
from sqlalchemy.schema import UniqueConstraint

from sqlalchemy import exc

class Database:
	""" Create and modify databse """

	def __init__(self):
		# Create DB engine.
		# self.engine = create_engine('sqlite:///testing.db')
		self.engine = create_engine('sqlite:///:memory:', echo=True)

		self.metadata = MetaData()
		self.inventory_table = Table('inventory', self.metadata,
				Column('Style', String, primary_key=True, nullable=False, default='EMPTY'),
				Column('Color', String, nullable=False),
				Column('Online_Color', String, primary_key=True, nullable=False),
				Column('Item_Size', Float, primary_key=True, nullable=False),

				Column('1090-Warehouse-Qty', Integer, nullable=False, default=0),
				Column('1001-Berry-Qty', Integer, nullable=False, default=0),
				Column('1002-Lancaster-Qty', Integer, nullable=False, default=0),
				Column('1003-Arlington-Qty', Integer, nullable=False, default=0),
				Column('1004-Jefferson-Qty', Integer, nullable=False, default=0),
				Column('1005-HarryHines-Qty', Integer, nullable=False, default=0),

				UniqueConstraint('Style', 'Online_Color', 'Item_Size')
			)
		self.metadata.create_all(self.engine)
		# self.inventory_table.create(self.engine, checkfirst=True)
		self.conn = self.engine.connect()

	def add_new_product(self, data_dict):
		""" Adds entry into database """

		insert = self.inventory_table.insert()
		try:
			self.conn.execute(insert, data_dict)
		except exc.SQLAlchemyError:
			print('Error inserting item into database.')

	def add_product(self, data_dict, store_id):
		""" Adds item to database """

		identifier = (self.inventory_table.c.Style == data_dict['Style']) & \
			(self.inventory_table.c.Online_Color == data_dict['Online_Color']) & \
			(self.inventory_table.c.Item_Size == data_dict['Item_Size'])

		item_select = self.inventory_table.select().where(identifier)

		# Check for existing entry
		item_found = self.conn.execute(item_select).fetchone()

		if item_found is None:
			insert_item = self.inventory_table.insert()
			self.conn.execute(insert_item, data_dict)
		else:
			# sum_qty
			total_qty = int(item_found[store_id]) + int(data_dict[store_id])

			update_qty = self.inventory_table.update()\
						.where(identifier)\
						.values({store_id:total_qty})
			self.conn.execute(update_qty)
	