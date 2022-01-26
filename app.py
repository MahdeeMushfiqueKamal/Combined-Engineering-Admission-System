import os
import sys
import cx_Oracle
from flask import Flask,render_template, url_for
from markupsafe import escape

if sys.platform.startswith("darwin"):
    cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/instantclient_19_3")
elif sys.platform.startswith("win32"):
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_3")

def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("""
        ALTER SESSION SET
          TIME_ZONE = 'UTC'
          NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI'""")

# start_pool(): starts the connection pool
def start_pool():
    pool_min = 4
    pool_max = 4
    pool_inc = 0
    pool_gmd = cx_Oracle.SPOOL_ATTRVAL_WAIT

    print("Connecting to localhost...................")

    pool = cx_Oracle.SessionPool(user="SYSTEM",password="1234",dsn="127.0.0.1/orcl", min=pool_min,max=pool_max,increment=pool_inc,threaded=True,getmode=pool_gmd,sessionCallback=init_session)
    return pool

################################################################################
# create_schema(): drop and create the demo table, and add a row
def create_schema():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("""
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
            execute immediate 'drop table STUDENT cascade constraints';
            exception when others then
                if sqlcode <> -942 then
                raise;
                end if;
            end;  
                   
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

            execute immediate 'CREATE TABLE STUDENT(
                STUDENT_ID INTEGER NOT NULL PRIMARY KEY,
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
        end;""")
    
    fhand = open('supporting functions/populate_table.sql')
    for line in fhand.readlines():
        line = line.replace(';','').strip()
        print(line)
        cursor.execute(line)
    connection.commit()
    fhand.close()

    cursor.execute('''INSERT INTO STUDENT(STUDENT_ID,HSC_ROLL,HSC_REG,NAME,BIRTHDATE,QUOTA_STATUS,CENTER_ID) VALUES(new_sequence.NEXTVAL,9961474,191365123,'Garth Mollah','3/5/2001','N','KUET')''')
    cursor.execute('''UPDATE EXAM_CENTER SET FILLED = (SELECT FILLED FROM EXAM_CENTER WHERE CENTER_ID='KUET' ) + 1 WHERE CENTER_ID='KUET' ''')
    connection.commit()
    

################################################################################

app = Flask(__name__)

# Display a welcome message on the 'home' page
@app.route('/')
def index():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute('''SELECT S.NAME, US.CAPASITY, US.QUOTA_CAPASITY FROM UNI_SUB US 
    JOIN SUBJECT S ON US.SUB_ID = S.SUB_ID WHERE US.UNI_ID = 'BUET'
    ''')
    BUET_SEATS = cursor.fetchall()

    cursor.execute('''SELECT S.NAME, US.CAPASITY, US.QUOTA_CAPASITY FROM UNI_SUB US 
    JOIN SUBJECT S ON US.SUB_ID = S.SUB_ID WHERE US.UNI_ID = 'CUET'
    ''')
    CUET_SEATS = cursor.fetchall()

    cursor.execute('''SELECT S.NAME, US.CAPASITY, US.QUOTA_CAPASITY FROM UNI_SUB US 
    JOIN SUBJECT S ON US.SUB_ID = S.SUB_ID WHERE US.UNI_ID = 'KUET'
    ''')
    KUET_SEATS = cursor.fetchall()

    cursor.execute('''SELECT S.NAME, US.CAPASITY, US.QUOTA_CAPASITY FROM UNI_SUB US 
    JOIN SUBJECT S ON US.SUB_ID = S.SUB_ID WHERE US.UNI_ID = 'RUET'
    ''')
    RUET_SEATS = cursor.fetchall()

    return render_template('index.html',BUET_SEATS=BUET_SEATS, CUET_SEATS = CUET_SEATS, KUET_SEATS= KUET_SEATS, RUET_SEATS = RUET_SEATS)

@app.route('/dashboard/<student_id>')
def dashboard(student_id):
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute('SELECT * from STUDENT WHERE STUDENT_ID = :id',[student_id])
    strudent_details = cursor.fetchone()
    print(strudent_details)
    return str("Hello "+student_id)




################################################################################
#
# Initialization is done once at startup time
#
if __name__ == '__main__':

    # Start a pool of connections
    pool = start_pool()

    # Create a demo table
    create_schema()

    # Start a webserver
    app.run(port=int(8080))