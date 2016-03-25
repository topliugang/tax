#!/usr/bin/env python
# -*- coding:utf-8 -*-  
import xlrd

from objects import Taxdetail
from objects import Taxdepartment
from objects import Taxation
from objects import Taxpayer_class
from objects import Taxpayer



#parse and return all data from a xls file
#return data, sheet_names
def get_total_data(excelname):
    workbook = xlrd.open_workbook(excelname)
    data = []			#3层list:[[[]]]  sheet-row-cell
    for sheet in workbook.sheets():
	    row_count = sheet.nrows
	    col_count = sheet.ncols
	    sheet_data = []
	    for i in range(row_count):
	        row_values = sheet.row_values(i)
	        sheet_data.append(row_values)
	    data.append(sheet_data)
    return data, workbook.sheet_names()
    

def get_sheet_names(excelname):
	workbook = xlrd.open_workbook(excelname)
	return workbook.sheet_names()


	
#return needed taxdetail from a uploaded xls file, from row 2(row 1 is title)
#filename: uploaded xls file
#sheet_id: which sheet of this xls file
#other params: col ids of the sheet
def get_taxdetail_data( filename, sheet_id, taxdepartment_col_id, taxation_col_id, \
    taxpayer_code_col_id, taxpayer_name_col_id, taxcode_col_id, taxmoney_col_id, \
    tax_belong_start_date_col_id, tax_belong_end_date_col_id, record_datetime_col_id):
	print 'xls_fucker.get_taxdetail_data'

	workbook = xlrd.open_workbook(filename)
	sheet = workbook.sheet_by_index(sheet_id)
	row_count = sheet.nrows
	data = []
	for i in range(1, row_count):
		row_values = sheet.row_values(i)
		needed_row_values = [ row_values[taxdepartment_col_id], 
		row_values[taxation_col_id], 
		row_values[taxpayer_code_col_id],
		row_values[taxpayer_name_col_id], 
		row_values[taxcode_col_id], 
		row_values[taxmoney_col_id],
		row_values[tax_belong_start_date_col_id], 
		row_values[tax_belong_end_date_col_id], 
		row_values[record_datetime_col_id] ]
		data.append(needed_row_values)

		#taxdepartment = Taxdepartment(id, name)
		#taxdetail = Taxdetail(taxdepartment, taxation, taxcode, taxpayer, taxmoney, \ tax_belong_start_date, tax_belong_end_date, record_datetime, \ which_year, which_month, upload_user, upload_date)

	return data	