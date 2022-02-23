begin
execute immediate 'drop table UNI_SUB cascade constraints';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;
/
begin
execute immediate 'drop table UNIVERSITY cascade constraints';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;
/
begin
execute immediate 'drop table SUBJECT cascade constraints';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;   
/
begin
execute immediate 'drop table EXAM_CENTER cascade constraints';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;     
/
BEGIN
EXECUTE IMMEDIATE 'DROP SEQUENCE new_sequence';
EXCEPTION
WHEN OTHERS THEN
	IF SQLCODE != -2289 THEN
	RAISE;
	END IF;
END;   
/
begin
execute immediate 'drop table EXAMINEE cascade constraints';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;
/
begin
execute immediate 'drop view EXAMINEE_PERSONAL';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;
/

begin
execute immediate 'drop table GLOBAL_DATA';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;
/

begin
execute immediate 'drop table MERIT_LIST cascade constraints';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;     
/

begin
execute immediate 'drop table CHOICE_LIST cascade constraints';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;     
/
begin
execute immediate 'drop table QUOTA_LIST cascade constraints';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;     
/

begin
execute immediate 'drop table QUOTA_CHOICE_LIST cascade constraints';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;     
/

begin
execute immediate 'drop table ADMIN_LOGIN';
exception when others then
	if sqlcode <> -942 then
	raise;
	end if;
end;     
/
-- create tables

CREATE TABLE UNIVERSITY(
	UNI_ID VARCHAR2(4) NOT NULL PRIMARY KEY,
	NAME VARCHAR2(60) NOT NULL,
	LOCATION VARCHAR(255) NOT NULL);
		
CREATE TABLE SUBJECT(SUB_ID VARCHAR2(4) NOT NULL PRIMARY KEY,NAME VARCHAR2(60) NOT NULL);

CREATE TABLE UNI_SUB(
	UNI_SUB_ID INTEGER PRIMARY KEY NOT NULL,
	UNI_ID VARCHAR2(4) REFERENCES UNIVERSITY(UNI_ID),
	SUB_ID VARCHAR2(4) REFERENCES SUBJECT(SUB_ID),
	CAPASITY INT,
	QUOTA_CAPASITY INT,
	FILLED INT DEFAULT 0,
	QUOTA_FILLED INT DEFAULT 0
); 

CREATE TABLE EXAM_CENTER(
	CENTER_ID VARCHAR2(4) NOT NULL PRIMARY KEY,
	NAME VARCHAR2(60) NOT NULL,
	LOCATION VARCHAR2(255) NOT NULL,
	CAPASITY INT NOT NULL,
	FILLED INT DEFAULT 0
);

CREATE SEQUENCE new_sequence
	MINVALUE 111111
	START WITH 111111
	INCREMENT BY 1
	CACHE 10;

CREATE TABLE EXAMINEE(
	EXAMINEE_ID INTEGER NOT NULL PRIMARY KEY,
	HSC_ROLL INTEGER NOT NULL,
	HSC_REG INTEGER NOT NULL,
	NAME VARCHAR2(100) NOT NULL,
	BIRTHDATE DATE NOT NULL,
	QUOTA_STATUS VARCHAR(1),
	CENTER_ID VARCHAR2(4) REFERENCES EXAM_CENTER(CENTER_ID),
	PHY_MARK INTEGER DEFAULT NULL,
	CHM_MARK INTEGER DEFAULT NULL,
	MATH_MARK INTEGER DEFAULT NULL,
	MERIT_POS INTEGER DEFAULT NULL,
	QUOTA_POS INTEGER DEFAULT NULL,
	PASSWORD VARCHAR(64) DEFAULT '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',
	IMAGE_URL VARCHAR(10) DEFAULT NULL
);

CREATE VIEW EXAMINEE_PERSONAL AS SELECT EXAMINEE_ID,HSC_ROLL,HSC_REG,NAME,BIRTHDATE,QUOTA_STATUS,CENTER_ID,PASSWORD,IMAGE_URL FROM EXAMINEE;

CREATE TABLE GLOBAL_DATA(
	ENTRY_NO INTEGER NOT NULL,
	SYSTEM_STATE INTEGER DEFAULT 0,
	APPLY_FIRST_DATE DATE DEFAULT SYSDATE,
	APPLY_LAST_DATE DATE DEFAULT to_date('5-4-2022','dd-mm-yyyy'),
	EXAM_DATE DATE DEFAULT to_date('14-05-2022','dd-mm-yyyy'),
	RESULT_DATE DATE DEFAULT to_date('1-06-2022','dd-mm-yyyy'),
	MIGRATION_DATE DATE DEFAULT to_date('15-06-2022','dd-mm-yyyy'),
	ADMIN_MESSAGE VARCHAR2(4000)
);

CREATE TABLE MERIT_LIST(
	MERIT_POS INTEGER NOT NULL PRIMARY KEY,
	EXAMINEE_ID INTEGER NOT NULL,
	ADMISSION_STATUS VARCHAR(1) DEFAULT 'N' CHECK (ADMISSION_STATUS in ('Y','N')), 
	ALLOCATED_TO NUMBER REFERENCES UNI_SUB(UNI_SUB_ID)
);

CREATE TABLE CHOICE_LIST(
	MERIT_POS INTEGER REFERENCES MERIT_LIST(MERIT_POS),
	PRIORITY_NO INTEGER CHECK (PRIORITY_NO >= 1 AND PRIORITY_NO <= 10),
	UNI_SUB_ID INTEGER REFERENCES UNI_SUB(UNI_SUB_ID)
);


CREATE TABLE QUOTA_LIST(
	QUOTA_POS INTEGER NOT NULL PRIMARY KEY,
	EXAMINEE_ID INTEGER NOT NULL,
	ADMISSION_STATUS VARCHAR(1) DEFAULT 'N' CHECK (ADMISSION_STATUS in ('Y','N')), 
	ALLOCATED_TO NUMBER REFERENCES UNI_SUB(UNI_SUB_ID)
);

CREATE TABLE QUOTA_CHOICE_LIST(
	QUOTA_POS INTEGER REFERENCES QUOTA_LIST(QUOTA_POS),
	PRIORITY_NO INTEGER CHECK (PRIORITY_NO >= 1 AND PRIORITY_NO <= 10),
	UNI_SUB_ID INTEGER REFERENCES UNI_SUB(UNI_SUB_ID)
);

CREATE TABLE ADMIN_LOGIN(
	ADMIN_ID VARCHAR2(5),
	PASSWORD VARCHAR(64)
);

INSERT INTO ADMIN_LOGIN(ADMIN_ID,PASSWORD) VALUES('admin','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');
-- populate with necessary data

INSERT INTO GLOBAL_DATA(ENTRY_NO,ADMIN_MESSAGE) VALUES(1,'Firstly, an applicant shall have to submit a properly filled online application form via the online submission system available through the website within the stipuleted time period.;;Follow Covid Policy in Exam Hall and Bring Admit Card;;Provide Subject Choice List within date');
		
INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES('BUET','Bangladesh University of Engineering and Technology', 'Dhaka-1000');
INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES('CUET','Chittagong University of Engineering and Technology', 'Kaptai, Highway, Chattogram 4349');
INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES('KUET','Khulna University of Engineering and Technology', 'Fulbarigate,Khulna');
INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES('RUET','Rajshahi University of Engineering and Technology', 'Kazla, Rajshahi-6204');

INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('ARCH','Architecture');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('BECM','Building Engineering and Construction Management');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('BME','Biomedical Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('CE','Civil Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('CFPE','Chemical and Food Process Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('CHE','Chemical Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('CSE','Computer Science and Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('ECE','Electrical and Computer Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('EEE','Electrical and Electronics Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('ESE','Energy Science and Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('ETE','Electronics and Telecommunication Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('GCE','Glass and Ceramic Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('IEM','Industrial Engineering and Management');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('IPE','Industrial and Production Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('LE','Lather Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('MSE','Material Science and Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('ME','Mechanical Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('MIE','Mechatronics and Industrial Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('MME','Materials and Metallurgical Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('MTE','Mechatronics Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('NAME','Naval Architecture and Marine Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('TE','Textile Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('PME','Petrolium and Mining Engineering');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('URP','Urbal and Regional Planning');
INSERT INTO SUBJECT(SUB_ID,NAME) VALUES('WRE','Water Resources Engineering');
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 1,'BUET','ARCH',55,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 2,'BUET','BME',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 3,'BUET','CE',195,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 4,'BUET','CHE',60,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 5,'BUET','CSE',120,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 6,'BUET','EEE',195,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 7,'BUET','IPE',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 8,'BUET','NAME',55,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 9,'BUET','ME',180,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 10,'BUET','MME',50,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 11,'BUET','URP',30,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 12,'BUET','WRE',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 13,'CUET','ARCH',30,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 14,'CUET','BME',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 15,'CUET','CE',130,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 16,'CUET','CSE',130,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 17,'CUET','EEE',180,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 18,'CUET','ETE',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 19,'CUET','MSE',30,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 20,'CUET','ME',180,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 21,'CUET','MIE',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 22,'CUET','PME',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 23,'CUET','URP',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 24,'CUET','WRE',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 25,'KUET','ARCH',40,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 26,'KUET','BECM',60,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 27,'KUET','BME',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 28,'KUET','CHE',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 29,'KUET','CE',120,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 30,'KUET','CSE',120,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 31,'KUET','EEE',120,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 32,'KUET','ECE',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 33,'KUET','ESE',30,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 34,'KUET','IEM',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 35,'KUET','LE',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 36,'KUET','MSE',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 37,'KUET','ME',120,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 38,'KUET','MTE',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 39,'KUET','TE',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 40,'KUET','URP',60,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 41,'RUET','ARCH',30,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 42,'RUET','BECM',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 43,'RUET','CFPE',30,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 44,'RUET','CE',180,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 45,'RUET','CSE',180,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 46,'RUET','EEE',180,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 47,'RUET','ECE',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 48,'RUET','ETE',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 49,'RUET','GCE',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 50,'RUET','IPE',60,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 51,'RUET','ME',180,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 52,'RUET','MSE',60,0);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 53,'RUET','MTE',60,1);
INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( 54,'RUET','URP',60,1);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('BUET','Bangladesh University of Engineering and Technology', 'Dhaka-1000',8000);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('CUET','Chittagong University of Engineering and Technology', 'Pahartoli, Raozan-4349, Chittagong',7000);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('KUET','Khulna University of Engineering and Technology', 'Fulbarigate,Khulna',7000);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('RUET','Rajshahi University of Engineering and Technology', 'Kazla, Rajshahi-6204',7000);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('SUST','Sylhet University of Science and Technology', 'University Ave, Sylhet 3114',7000);