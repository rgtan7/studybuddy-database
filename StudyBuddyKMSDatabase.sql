CREATE TABLE aoe_level (
	aoe_level_id serial primary key not null, 
	aoe_level varchar(64),	
	aoe_level_ind bool default false
);

CREATE TABLE aoe (
	aoe_id serial primary key not null, 
	aoe_name varchar(64),
	aoe_level_id int references aoe_level(aoe_level_id), 
	aoe_employeereq int, 
	aoe_employeecount int,
	aoe_employeeneed int, 
	aoe_delete_ind bool default false 
);

CREATE TABLE skill(
	skill_id serial primary key not null,
	skill_name varchar(128),
	aoe_id int references aoe(aoe_id),
	-- aoe_level int references aoe_level(aoe_level_id), 
	skill_modified_on timestamp without time zone default now(),
	skill_delete_ind bool default false,
	aoe_level_id int references aoe_level(aoe_level_id)
);

CREATE TABLE emp(
	emp_id serial primary key not null,
	emp_name_first varchar(256),
	emp_name_middle varchar(64),
	emp_name_last varchar(64),
	emp_sex varchar(64),
	emp_bday date,
	emp_degree varchar(256),
	emp_civil varchar(64),
	emp_phone varchar(13),
	emp_email varchar(64),
	emp_address1 varchar(64),
	emp_address2 varchar(64),
	emp_address3 varchar(64),
	emp_address4 varchar(64),
	emp_postal int,
	aoe_id int references aoe(aoe_id), 
	skill_id_1 int references skill(skill_id) ,
	skill_id_2 int references skill(skill_id) ,
	skill_id_3 int references skill(skill_id) ,
	emp_hiredate date,
	emp_sched varchar(64), 
	emp_bank varchar(128),
	emp_bank_name varchar(128),
	emp_bank_num varchar(64),
	emp_modified_on timestamp without time zone default now(),
	emp_delete_ind bool default false);

CREATE TABLE equipment(
	equipment_id serial primary key not null,
	equipment_name varchar(128),
	equipment_type varchar(64),
	emp_id int references emp(emp_id), 
	equipment_modified_on timestamp without time zone default now(),
	equipment_delete_ind bool default false);

create table users(
    user_id serial primary key not null,
    user_name varchar(32) unique, 
    user_password varchar(64) not null,
    user_modified_on timestamp without time zone default now(),
    user_delete_ind boolean default false
)

INSERT INTO aoe_level (aoe_level): 
VALUES ('College'); 

INSERT INTO aoe_level (aoe_level) 
VALUES ('Highschool');

INSERT INTO aoe_level (aoe_level) 
VALUES ('Elementary');

INSERT INTO aoe_level (aoe_level) 
VALUES ('Preschool'); 