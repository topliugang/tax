# -*- coding:utf-8 -*-  
"""
测试excel导入mysql
"""


import xlrd
import MySQLdb
import sys
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

def get_role_by_id(id):
    print 'get_role_by_id'
    print id, '  ', type(id)
    try:
        cur, conn = init_db()
        cur.execute('select id, name from role where id = %s', id)
        result = cur.fetchone()
        role = Role(result[0], result[1])
        print role
        return result
    except MySQLdb.Error, e:
        print 'mysql error %d: %s'%(e.args[0], e.args[1])
    finally:
        close_db(cur, conn)    


	

if __name__ == "__main__":
    get_role_by_id(1)
    
