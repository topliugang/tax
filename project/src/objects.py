

class User:
	def __init__(self, id, name, username, password, role):
		self.id = id
		self.name = name
		self.username = username
		self.password = password
		self.role = role




class Role:
	def __init__(self, id, name):
		self.id = id
		self.name = name


class Taxdepartment:
	def __init__(self, id, name):
		self.id = id
		self.name = name

class Taxation:
	def __init__(self, id, name):
		self.id = id
		self.name = name

class Taxpayer_class:
	def __init__(self, id, name):
		self.id = id
		self.name = name

class Taxpayer:
	def __init__(self, id, code, name, taxpayer_class, taxdepartment):
		self.id = id
		self.code = code
		self.name = name
		self.taxpayer_class = taxpayer_class
		self.taxdepartment = taxdepartment

class Taxdetail:
	def __init__(self, id, taxdepartment, taxation, taxcode, taxpayer, taxmoney, \
		tax_belong_start_date, tax_belong_end_date, record_datetime, \
		which_year, which_month, upload_user, upload_date):
		self.id = id
		self.taxdepartment = taxdepartment
		self.taxation = taxation
		self.taxcode = taxcode
		self.taxpayer = taxpayer
		self.taxmoney = taxmoney

		self.tax_belong_start_date = tax_belong_start_date
		self.tax_belong_end_date = tax_belong_end_date
		
		self.record_datetime = record_datetime
		self.which_year = which_year
		self.which_month = which_month
		self.upload_user = upload_user
		self.upload_date = upload_date