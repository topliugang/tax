/*
	建表
*/

drop table if exists user;
drop table if exists role;
drop table if exists taxdepartment;
drop table if exists taxation;
drop table if exists taxpayer_class;
drop table if exists taxpayer;
drop table if exists taxdetail;


create table role(
	id int not null auto_increment,
	name varchar(200),
	primary key (id)
)default charset=utf8;


create table user(
	id int not null auto_increment, 
	name varchar(200), 
	username varchar(200), 
	password varchar(200),
	role_id int,
	primary key (id)
)default charset=utf8;



create table taxdepartment( -- 税务机构(税务局)
	id int not null auto_increment,
	name varchar(200),
	primary key (id),
	unique(name)
)default charset=utf8;

create table taxation( -- 税务所
	id int not null auto_increment,
	name varchar(200),
	primary key (id),
	unique(name)
)default charset=utf8;

create table taxpayer_class( -- 纳税人分类
	id int not null auto_increment,
	name varchar(200),
	primary key (id)
)default charset=utf8;

create table taxpayer( -- 纳税人(企业)
	id int not null auto_increment,
	code varchar(200),
	name varchar(200),
	taxpayer_class_id int,
	taxdepartment_id int,
	primary key (id),
	unique(code)
)default charset=utf8;

create table taxdetail( -- 纳税明细
	id int not null auto_increment,
	taxdepartment_id int, -- 税务局id
	taxation_id int, -- 税务所id
	taxcode varchar(200), -- 电子税票号
	taxpayer_id int, -- 纳税人id
	taxmoney float, -- 金额
	tax_belong_start_date datetime, -- 税款所属期起
	tax_belong_end_date datetime, -- 税款所属期止
	record_datetime datetime, -- 录入日期
	which_year int, 
	which_month int,
	upload_user_id int, 
	upload_date datetime,
	primary key (id)
)default charset=utf8;







/*
	创建存储过程
*/

DELIMITER @@
drop procedure if exists insert_data;
create procedure insert_data( in taxdepartment_name varchar(200), 
	in taxation_name varchar(200), 
	in taxpayer_code varchar(200), 
	in taxpayer_name varchar(200), 
	in taxcode varchar(200), 
	in taxmoney float,
	in tax_belong_start_date varchar(200), 
	in tax_belong_end_date varchar(200),
	in record_datetime varchar(200), 
	in which_year int, 
	in which_month int, 
	in user_id int )

begin

declare taxdepartment_id int;
declare taxation_id int;
declare taxpayer_id int;
-- temp set by 1, will change
declare taxpayer_class_id int;
set taxpayer_class_id = 1;

insert into taxdepartment(name) 
select taxdepartment_name from dual where not exists 
(select * from taxdepartment where name = taxdepartment_name);

select id into taxdepartment_id from taxdepartment where name = taxdepartment_name;

insert into taxation(name) 
select taxation_name from dual where not exists 
(select * from taxation where name = taxation_name);

select id into taxation_id from taxation where name = taxation_name;

insert into taxpayer(code, name, taxdepartment_id, taxpayer_class_id) 
select taxpayer_code, taxpayer_name, taxdepartment_id, taxpayer_class_id from dual where not exists 
(select * from taxpayer where code = taxpayer_code);

select id into taxpayer_id from taxpayer where code = taxpayer_code;

insert into taxdetail(taxdepartment_id, taxation_id, taxcode, taxpayer_id, taxmoney, 
	tax_belong_start_date, tax_belong_end_date, record_datetime, which_year, which_month, 
	upload_user_id, upload_date)
	values
	(taxdepartment_id, taxation_id, taxcode, taxpayer_id, taxmoney,
		tax_belong_start_date, tax_belong_end_date, record_datetime, which_year, which_month,
	 	user_id, now());

end 

@@ 
DELIMITER ; 

-- call insertdata('枣庄市地方税务局市中分局', '枣庄市地方税务局市中分局中心街中心税务所', '370402164451975', '枣庄市海星机电物资有限公司', '320160127000275387', 60)





-- test data
insert into role(name) values('role1');
insert into user(name, username, password, role_id) values('管理员', 'admin', 'admin', 1);
insert into taxpayer_class(name) values('class1');


/*

税款所属税务机构	主管税务所（科、分局）	电子税票号码	纳税人识别号	纳税人名称	税款所属期起	税款所属期止	实缴金额	录入日期
枣庄市地方税务局市中分局	枣庄市地方税务局市中分局中心街中心税务所	320160127000275387	370402164451975	枣庄市海星机电物资有限公司	2015-12-01 00:00:00.0	2015-12-31 00:00:00.0	60	2016-01-27 14:00:56.0
枣庄市地方税务局峄城分局	枣庄市地方税务局峄城分局峨山中心税务所	320160107000481670	37040475828481X	枣庄顺和玩具有限公司	2015-12-01 00:00:00.0	2015-12-31 00:00:00.0	1000	2016-01-07 10:45:46.0
枣庄市地方税务局峄城分局	枣庄市地方税务局峄城分局古邵中心税务所	320160112000997250	370404699678164	枣庄鑫源纸业有限公司	2015-12-01 00:00:00.0	2015-12-31 00:00:00.0	2000	2016-01-12 15:29:12.0
枣庄市地方税务局山亭分局	枣庄市地方税务局山亭分局冯卯中心税务所	320160113001306327	370406674533241	枣庄市顺滕纸箱有限公司	2016-01-13 00:00:00.0	2016-01-13 00:00:00.0	1990	2016-01-13 15:38:23.0
枣庄市地方税务局山亭分局	枣庄市地方税务局山亭分局冯卯中心税务所	320160122000293476	370406550925462	枣庄市祥泰果蔬有限公司	2016-01-22 00:00:00.0	2016-01-22 00:00:00.0	1150	2016-01-22 12:28:38.0
枣庄市地方税务局山亭分局	枣庄市地方税务局山亭分局冯卯中心税务所	320160122000291971	370406673174531	枣庄市山亭区宏祥农副产品有限公司	2016-01-22 00:00:00.0	2016-01-22 00:00:00.0	3000	2016-01-22 12:29:42.0
枣庄市地方税务局山亭分局	枣庄市地方税务局山亭分局冯卯中心税务所	320160122000293472	370406688298748	枣庄市恒军包装制品有限公司	2016-01-22 00:00:00.0	2016-01-22 00:00:00.0	2000	2016-01-22 12:27:40.0
滕州市地方税务局	滕州市地方税务局北辛中心税务所	320160113001131495	370481073023836	滕州德和企业管理咨询有限公司	2015-12-01 00:00:00.0	2015-12-31 00:00:00.0	48	2016-01-13 14:16:29.0
滕州市地方税务局	滕州市地方税务局北辛中心税务所	320160111000470788	370481169894935	滕州市第四建筑安装工程公司一分公司	2015-01-01 00:00:00.0	2015-12-31 00:00:00.0	2455.64	2016-01-11 12:01:30.0


insert into taxdepartment(name) 
select '枣庄市地方税务局市中分局' from dual where not exists 
(select * from taxdepartment where name = '枣庄市地方税务局市中分局' );


*/











