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

-- create tables

CREATE TABLE UNIVERSITY(
	UNI_ID VARCHAR2(4) NOT NULL PRIMARY KEY,
	NAME VARCHAR2(60) NOT NULL,
	LOCATION VARCHAR(255) NOT NULL);
		
CREATE TABLE SUBJECT(SUB_ID VARCHAR2(4) NOT NULL PRIMARY KEY,NAME VARCHAR2(60) NOT NULL);

CREATE TABLE UNI_SUB(
	UNI_ID VARCHAR2(4) REFERENCES UNIVERSITY(UNI_ID),
	SUB_ID VARCHAR2(4) REFERENCES SUBJECT(SUB_ID),
	CAPASITY INT,
	QUOTA_CAPASITY INT
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
	PHY_MARK INTEGER DEFAULT 0,
	CHM_MARK INTEGER DEFAULT 0,
	MATH_MARK INTEGER DEFAULT 0,
	MERIT_POS INTEGER DEFAULT NULL,
	QUOTA_POS INTEGER DEFAULT NULL,
	PASSWORD VARCHAR(64) DEFAULT '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',
	IMAGE_URL VARCHAR(10) DEFAULT NULL
);

CREATE VIEW EXAMINEE_PERSONAL AS SELECT EXAMINEE_ID,HSC_ROLL,HSC_REG,NAME,BIRTHDATE,QUOTA_STATUS,CENTER_ID,PASSWORD,IMAGE_URL FROM EXAMINEE;

CREATE TABLE GLOBAL_DATA(
	ENTRY_NO INTEGER NOT NULL,
	SYSTEM_STATE INTEGER DEFAULT 1,
	APPLY_FIRST_DATE DATE DEFAULT SYSDATE,
	APPLY_LAST_DATE DATE DEFAULT to_date('5-4-2022','dd-mm-yyyy'),
	EXAM_DATE DATE DEFAULT to_date('14-05-2022','dd-mm-yyyy'),
	RESULT_DATE DATE DEFAULT to_date('1-06-2022','dd-mm-yyyy'),
	MIGRATION_DATE DATE DEFAULT to_date('15-06-2022','dd-mm-yyyy'),
	ADMIN_MESSAGE VARCHAR2(4000)
);


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
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','ARCH',55,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','BME',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','CE',195,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','CHE',60,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','CSE',120,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','EEE',195,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','IPE',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','NAME',55,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','ME',180,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','MME',50,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','URP',30,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('BUET','WRE',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','ARCH',30,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','BME',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','CE',130,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','CSE',130,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','EEE',180,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','ETE',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','MSE',30,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','ME',180,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','MIE',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','PME',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','URP',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('CUET','WRE',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','ARCH',40,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','BECM',60,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','BME',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','CHE',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','CE',120,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','CSE',120,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','EEE',120,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','ECE',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','ESE',30,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','IEM',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','LE',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','MSE',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','ME',120,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','MTE',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','TE',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('KUET','URP',60,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','ARCH',30,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','BECM',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','CFPE',30,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','CE',180,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','CSE',180,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','EEE',180,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','ECE',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','ETE',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','GCE',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','IPE',60,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','ME',180,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','MSE',60,0);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','MTE',60,1);
INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES('RUET','URP',60,1);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('BUET','Bangladesh University of Engineering and Technology', 'Dhaka-1000',8000);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('CUET','Chittagong University of Engineering and Technology', 'Pahartoli, Raozan-4349, Chittagong',7000);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('KUET','Khulna University of Engineering and Technology', 'Fulbarigate,Khulna',7000);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('RUET','Rajshahi University of Engineering and Technology', 'Kazla, Rajshahi-6204',7000);
INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES('SUST','Sylhet University of Science and Technology', 'University Ave, Sylhet 3114',7000);