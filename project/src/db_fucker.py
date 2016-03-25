#!/usr/bin/env python
# -*- coding:utf-8 -*-  
import MySQLdb
from objects import *

def init_db():
    #最后一个参数需要带 
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='liugang', \
        db='tax', port=3306, charset='utf8')
    cur = conn.cursor()
    return cur, conn

def close_db(cur, conn):
    cur.close()
    conn.close()

####Role###############################################################
def get_role_by_id(id):
    print 'get_role_by_id'
    try:
        cur, conn = init_db()
        cur.execute('select id, name from role where id = %s', id)
        result = cur.fetchone()
        role = Role(result[0], result[1])
        return role
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])
    finally:
        close_db(cur, conn)


####User##############################################################################################################################
def get_user_by_id(id):
    print 'get_user_by_id'
    try:
        cur, conn = init_db()
        cur.execute('select id, name, username, password, role_id from user where id = %s', id)
        result = cur.fetchone()
        role = get_role_by_id(result[4])
        user = User(result[0], result[1], result[2], result[3], role )
        return user
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])

    finally:
        close_db(cur, conn)    

def get_user_by_username_and_password(username, password):
    print 'get_user'
    try:
        cur, conn = init_db()
        cur.execute('select id, name, username, password, role_id from user where username = %s and password = %s',\
         (username, password))
        result = cur.fetchone()
        role = get_role_by_id(result[4])
        user = User(result[0], result[1], result[2], result[3], role )
        return user
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])

    finally:
        close_db(cur, conn)    

####Taxdepartment###############################################################
def get_taxdepartment_by_id(id):
    print 'get_taxdepartment_by_id'
    try:
        cur, conn = init_db()
        cur.execute('select id, name from taxdepartment where id = %s', id)
        result = cur.fetchone()
        taxdepartment = Taxdepartment(result[0], result[1])
        return taxdepartment
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])
    finally:
        close_db(cur, conn)    

####Taxation###############################################################
def get_taxation_by_id(id):
    print 'get_taxation_by_id'
    try:
        cur, conn = init_db()
        cur.execute('select id, name from taxation where id = %s', id)
        result = cur.fetchone()
        taxation = Taxation(result[0], result[1])
        return taxation
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])
    finally:
        close_db(cur, conn)        

####Taxpayer_class###############################################################
def get_taxpayer_class_by_id(id):
    print 'get_taxpayer_class_by_id'
    try:
        cur, conn = init_db()
        cur.execute('select id, name from taxpayer_class where id = %s', id)
        result = cur.fetchone()
        taxpayer_class = Taxpayer_class(result[0], result[1])
        return taxpayer_class
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])
    finally:
        close_db(cur, conn) 

####Taxpayer###############################################################
def get_taxpayer_by_id(id):
    print 'get_taxpayer_by_id'
    try:
        cur, conn = init_db()
        cur.execute('select id, code, name, taxpayer_class_id, taxdepartment_id from taxpayer where id = %s', id)
        result = cur.fetchone()
        taxpayer_class = get_taxpayer_class_by_id(result[3])
        taxdepartment = get_taxdepartment_by_id(result[4])
        taxpayer = Taxpayer(result[0], result[1], result[2], taxpayer_class, taxdepartment)
        return taxpayer
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])
    finally:
        close_db(cur, conn)   

####Taxdetail###############################################################        
def get_taxdetail_by_id(id):
    print 'get_taxdetail_by_id'
    try:
        cur, conn = init_db()
        sql = """
            select id, taxdepartment_id, taxation_id, taxcode, taxpayer_id, taxmoney, 
            tax_belong_start_date, tax_belong_end_date, record_datetime, which_year, 
            which_month, upload_user_id, upload_date from taxdetail
            where id = %s
        """
        cur.execute(sql, id)
        result = cur.fetchone()
        taxdepartment = get_taxdepartment_by_id(result[1])
        taxation = get_taxation_by_id(result[2])
        taxpayer = get_taxpayer_by_id(result[4])
        user = get_user_by_id(result[11])
        taxdetail = Taxdetail(result[0], 
            taxdepartment,
            taxation, 
            result[3], 
            taxpayer, 
            result[5],
            result[6], 
            result[7], 
            result[8], 
            result[9], 
            result[10], 
            user, 
            result[12])
        return taxdetail
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])
    finally:
        close_db(cur, conn) 

def get_taxdetails_by_year_and_month(which_year, which_month):     
    print 'get_taxdetail_data_by_year_and_month'
    try:
        cur, conn = init_db()
        sql = """
            select id, taxdepartment_id, taxation_id, taxcode, taxpayer_id, taxmoney, 
            tax_belong_start_date, tax_belong_end_date, record_datetime, which_year, 
            which_month, upload_user_id, upload_date from taxdetail
            where which_year = %s and which_month = %s
        """
        cur.execute(sql, (which_year, which_month))
        result = cur.fetchall()
        taxdetails = []
        for row in result:
            taxdepartment = get_taxdepartment_by_id(row[1])
            taxation = get_taxation_by_id(row[2])
            taxpayer = get_taxpayer_by_id(row[4])
            user = get_user_by_id(row[11])
            taxdetail = Taxdetail(row[0], 
                taxdepartment,
                taxation, 
                row[3], 
                taxpayer, 
                row[5],
                row[6], 
                row[7], 
                row[8], 
                row[9], 
                row[10], 
                user, 
                row[12])
            taxdetails.append(taxdetail)
        return taxdetails
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])
    finally:
        close_db(cur, conn) 


def insert_tax_detail(data, which_year, which_month, user_id):
    print 'insert_tax_detail'
    try:
        cur, conn = init_db()    
        for row in data:
            row.append(which_year)
            row.append(which_month)
            row.append(user_id)
            cur.callproc('insert_data', row)
            conn.commit()
            print 'insert sucess'
        
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])

    finally:
        close_db(cur, conn)
        

def get_tax_class_data(which_year, which_month):
    print 'get_tax_class_data'
    try:
        cur, conn = init_db()
        sql = """
            select taxdepartment_id, sum(taxmoney) from taxdetail 
            where which_year = %s and which_month = %s
            group by taxdepartment_id order by taxdepartment_id asc;
        """
        cur.execute(sql, (which_year, which_month))
        result = cur.fetchall()
        data = []
        for row in result:
            rowdata = []
            taxdepartment = get_taxdepartment_by_id(row[0])
            rowdata.append(taxdepartment)
            rowdata.append('%.2f'%(row[1]/10000))
            rowdata.append('%.2f'%(row[1]/10000))
            rowdata.append('%.2f'%(row[1]/10000))
            rowdata.append('%.2f'%(row[1]/10000))
            rowdata.append('%.2f'%(row[1]/10000))
            rowdata.append('%.2f'%(row[1]/10000))
            rowdata.append('%.2f'%(row[1]/10000))
            rowdata.append('%.2f'%(row[1]/10000))
            
            data.append(rowdata)
        
        return data
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])
    finally:
        close_db(cur, conn) 


    
    
