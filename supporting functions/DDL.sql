begin
    begin
    execute immediate 'drop table UNI_SUB cascade constraints';
    exception when others then
        if sqlcode <> -942 then
        raise;
        end if;
    end;

    begin
    execute immediate 'drop table UNIVERSITY cascade constraints';
    exception when others then
        if sqlcode <> -942 then
        raise;
        end if;
    end;
    
    begin
    execute immediate 'drop table SUBJECT cascade constraints';
    exception when others then
        if sqlcode <> -942 then
        raise;
        end if;
    end;   

    begin
    execute immediate 'drop table EXAM_CENTER cascade constraints';
    exception when others then
        if sqlcode <> -942 then
        raise;
        end if;
    end;     

    BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE new_sequence';
    EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -2289 THEN
        RAISE;
        END IF;
    END;   

    begin
    execute immediate 'drop table EXAMINEE cascade constraints';
    exception when others then
        if sqlcode <> -942 then
        raise;
        end if;
    end;  
            
    -- Table Creation
    
    execute immediate 'CREATE TABLE UNIVERSITY(
        UNI_ID VARCHAR2(4) NOT NULL PRIMARY KEY,
        NAME VARCHAR2(60) NOT NULL,
        LOCATION VARCHAR(255) NOT NULL)';

    execute immediate 'CREATE TABLE SUBJECT(SUB_ID VARCHAR2(4) NOT NULL PRIMARY KEY,NAME VARCHAR2(60) NOT NULL)';
    execute immediate 'CREATE TABLE UNI_SUB(
        UNI_ID VARCHAR2(4) REFERENCES UNIVERSITY(UNI_ID),
        SUB_ID VARCHAR2(4) REFERENCES SUBJECT(SUB_ID),
        CAPASITY INT,
        QUOTA_CAPASITY INT
    )'; 
    execute immediate 'CREATE TABLE EXAM_CENTER(
        CENTER_ID VARCHAR2(4) NOT NULL PRIMARY KEY,
        NAME VARCHAR2(60) NOT NULL,
        LOCATION VARCHAR2(255) NOT NULL,
        CAPASITY INT NOT NULL,
        FILLED INT DEFAULT 0)';

    execute immediate 'CREATE SEQUENCE new_sequence
        MINVALUE 111111
        START WITH 111111
        INCREMENT BY 1
        CACHE 10';

    execute immediate 'CREATE TABLE EXAMINEE(
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
        QUOTA_POS INTEGER DEFAULT NULL 
    )';
    commit;
end;