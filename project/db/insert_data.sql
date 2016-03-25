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


