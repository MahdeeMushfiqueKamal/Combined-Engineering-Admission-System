-- Trigger for saving the deleted students' information

CREATE TABLE DELETED_EXAMINEE(
	EXAMINEE_ID INTEGER NOT NULL PRIMARY KEY,
	HSC_ROLL INTEGER NOT NULL,
	HSC_REG INTEGER NOT NULL,
	NAME VARCHAR2(100) NOT NULL,
	BIRTHDATE DATE NOT NULL,
	QUOTA_STATUS VARCHAR(1),
	PASSWORD VARCHAR(64) DEFAULT '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',
	IMAGE_URL VARCHAR(10) DEFAULT NULL
);

CREATE OR REPLACE TRIGGER BACKUP_DELETED_STUDENTS
BEFORE DELETE
ON EXAMINEE
FOR EACH ROW
DECLARE
V_EXAMINEE_ID INTEGER;
V_HSC_ROLL INTEGER;
V_HSC_REG INTEGER;
V_NAME VARCHAR2(100);
V_BIRTHDATE DATE;
V_QUOTA_STATUS VARCHAR(1);
V_CENTER_ID VARCHAR2(4);
V_PASSWORD VARCHAR(64);
V_IMAGE_URL VARCHAR(10);
BEGIN
V_EXAMINEE_ID = OLD.EXAMINEE_ID;
V_HSC_ROLL = OLD.HSC_ROLL;
V_HSC_REG = OLD.HSC_REG;
V_NAME = OLD.NAME;
V_BIRTHDATE = OLD.BIRTHDATE;
V_QUOTA_STATUS = OLD.QUOTA_STATUS;
V_CENTER_ID = OLD.CENTER_ID;
V_PASSWORD = OLD.PASSWORD;
V_IMAGE_URL = OLD.IMAGE_URL;
INSERT INTO DELETED_EXAMINEE VALUES (V_EXAMINEE_ID, V_HSC_ROLL, V_HSC_REG, V_NAME, V_BIRTHDATE, V_QUOTA_STATUS, V_CENTER_ID, V_PASSWORD, V_IMAGE_URL);
END ;
/

-- Trigger for updating Admin MSG when System State is changed

CREATE OR REPLACE TRIGGER ADMIN_MSG_UPDATE
AFTER UPDATE
OF MERIT_POS
ON EXAMINEE
DECLARE
OLD_ADMIN_MESSAGE VARCHAR2(4000);
V_ADMIN_MESSAGE VARCHAR2(4000);
BEGIN
SELECT ADMIN_MESSAGE INTO OLD_ADMIN_MESSAGE FROM GLOBAL_DATA WHERE ENTRY_NO = 1;
V_ADMIN_MESSAGE = OLD_ADMIN_MESSAGE || ' ;Results have been published!;';

UPDATE GLOBAL_DATA SET ADMIN_MESSAGE = V_ADMIN_MESSAGE WHERE ENTRY_NO = 1;
END ;
/


-- Trigger for keeping the list of admission status changes 

CREATE TABLE LOG_TABLE_ADMISSION_STATUS_UPDATE
(
USERNAME VARCHAR2(25),
DATETIME DATE
) ;

CREATE OR REPLACE TRIGGER ADMISSION_STATUS_CHANGES
AFTER UPDATE
OF ADMISSION_STATUS
ON C##CEAS_ADMIN.MERIT_LIST
DECLARE
USERNAME VARCHAR2(25);
BEGIN
USERNAME := USER;
INSERT INTO LOG_TABLE_ADMISSION_STATUS_UPDATE VALUES (USERNAME, SYSDATE);
END ;
/