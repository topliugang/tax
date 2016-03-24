#!/usr/bin/env python
# -*- coding:utf-8 -*-  
#
# Copyright 2009 Facebook
#

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.template
import os.path

from tornado.options import define, options

import xls_fucker
import db_fucker


import time

define("port", default=8888, help="run on the given port", type=int)
define("upload_dir", default=os.path.join(os.path.dirname(__file__),'../upload/'), help='upload files dir')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", LoginHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/main', MainHandler),
            (r'/import', ImportHandler),
            (r'/upload_file', UploadFileHandler),
            (r'/query_detail',QueryDetailHandler),
        ]
        settings = dict(
            fucktitle = u"税务统计系统",
            template_path=os.path.join(os.path.dirname(__file__),'../web/template'),
            static_path=os.path.join(os.path.dirname(__file__),'../web/static'),
            upload_file=os.path.join(os.path.dirname(__file__),'../upload'),
        )

        super(Application, self).__init__(handlers, **settings)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_cookie('user_id')
        if(user_id):
            self.redirect('/main')
        else:
            self.render('login.html') 

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user = db_fucker.get_user_by_username_and_password(username, password)
        if ( user ):
            #cookie
            self.set_cookie('user_id', str(user.id))
            self.set_cookie('user_name', user.name)
            self.set_cookie('user_username', user.username)
            self.set_cookie('role_id', str(user.role.id))
            self.redirect('/main')
        else:
            self.redirect('/login')

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_cookie('user_id')
        if(not user_id):
            self.redirect('/login')
        name = self.get_cookie('user_name')
        username = self.get_cookie('user_username')
        
        self.render('main.html', name = name, username = username)
        #t = tornado.template.Template('fuck.html')
        #print t.generate(title="FUCKKKK")


#导入excel表格到数据库
class ImportHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('import.html', filename = None, sheet_names = None, data = None)

    def post(self):
        taxdepartment_col_id = int(self.get_argument('taxdepartment'))
        taxation_col_id = int(self.get_argument('taxation'))
        taxpayer_code_col_id = int(self.get_argument('taxpayer_code'))
        taxpayer_name_col_id = int(self.get_argument('taxpayer_name'))
        taxcode_col_id = int(self.get_argument('taxcode'))
        taxmoney_col_id = int(self.get_argument('taxmoney'))

        tax_belong_start_date_col_id = int(self.get_argument('tax_belong_start_date'))
        tax_belong_end_date_col_id = int(self.get_argument('tax_belong_end_date'))
        record_datetime_col_id = int(self.get_argument('record_datetime'))

        filename = self.get_argument('filename')
        sheet_id = int(self.get_argument('sheet_id'))

        which_year = self.get_argument('which_year')
        which_month = self.get_argument('which_month')

        filepathname = os.path.join(options.upload_dir, filename)

        #data[ str, str, str, str, str, float, str, str, str ] len = 9
        data = xls_fucker.get_taxdetail_data(filepathname, sheet_id, 
            taxdepartment_col_id,
            taxation_col_id, 
            taxpayer_code_col_id, 
            taxpayer_name_col_id, 
            taxcode_col_id, 
            taxmoney_col_id,
            tax_belong_start_date_col_id, 
            tax_belong_end_date_col_id, 
            record_datetime_col_id)

        user_id = self.get_cookie('user_id')
        db_fucker.insert_tax_detail(data, which_year, which_month, user_id)
        self.render('success.html')

#上传文件
class UploadFileHandler(tornado.web.RequestHandler):
    def post(self):
        if self.request.files:
            file_meta = self.request.files['myfile']
            myfile = file_meta[0]
            #filename = myfile['filename']
            filename = str(int(time.time()*1000))+'.dat'
            filepathname = os.path.join(options.upload_dir, filename)
            with open(filepathname, 'wb') as fin:
                fin.write(myfile['body'])
            data, sheet_names = xls_fucker.get_total_data(filepathname) #data:sheet-row-cell
            #sheet_names = xls_fucker.get_sheet_names(filepathname)
            self.render('import.html', filename = filename, sheet_names = sheet_names, data = data)


#查询详细信息
class QueryDetailHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('queryDetail.html', taxdetails = None)

    def post(self):
        which_year = int(self.get_argument('which_year'))
        which_month = int(self.get_argument('which_month'))
        taxdetails = db_fucker.get_taxdetails_by_year_and_month(which_year, which_month)
        self.render('queryDetail.html', taxdetails = taxdetails)


def main():
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    


if __name__ == "__main__":
    main()
