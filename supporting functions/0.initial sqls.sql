-- Log into SYSTEM/ SYS as SYSDBA and write this stuff. 

CREATE USER C##CEAS_ADMIN IDENTIFIED BY 1234;
grant create session to C##CEAS_ADMIN;
grant create table to c##CEAS_ADMIN;
grant create view, create procedure, create sequence to c##CEAS_ADMIN;
GRANT UNLIMITED TABLESPACE TO C##CEAS_ADMIN;


CREATE USER C##CEAS_USER IDENTIFIED BY 1234;
grant create session to C##CEAS_USER;

-- Log into C##CEAS_ADMIN using Navicat/Datagrip and 1.Execute DDL.sql and 2.populate_examinee.sql

-- Write the following thing in SYSTEM after creating tables.

grant select on C##CEAS_ADMIN.UNIVERSITY to C##CEAS_USER;
grant select on C##CEAS_ADMIN.SUBJECT to C##CEAS_USER;
grant select on C##CEAS_ADMIN.UNI_SUB to C##CEAS_USER;
grant select,update on C##CEAS_ADMIN.EXAM_CENTER to C##CEAS_USER;
grant select on C##CEAS_ADMIN.EXAMINEE to C##CEAS_USER;
grant select on C##CEAS_ADMIN.new_sequence to C##CEAS_USER;
grant select,insert,update on C##CEAS_ADMIN.EXAMINEE_PERSONAL to C##CEAS_USER;
grant select on C##CEAS_ADMIN.GLOBAL_DATA to C##CEAS_USER;
grant select on C##CEAS_ADMIN.MERIT_LIST to C##CEAS_USER;
grant select,insert,delete on C##CEAS_ADMIN.CHOICE_LIST to C##CEAS_USER;
grant select on C##CEAS_ADMIN.QUOTA_LIST to C##CEAS_USER;
grant select,insert,delete on C##CEAS_ADMIN.QUOTA_CHOICE_LIST to C##CEAS_USER;