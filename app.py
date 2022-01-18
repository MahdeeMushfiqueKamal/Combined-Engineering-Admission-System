import os
import sys
import cx_Oracle
from flask import Flask,render_template, url_for

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

    print("Connecting to localhost")

    pool = cx_Oracle.SessionPool(user="SYSTEM",
                                 password="1234",
                                 dsn="127.0.0.1/orcl",
                                 min=pool_min,
                                 max=pool_max,
                                 increment=pool_inc,
                                 threaded=True,
                                 getmode=pool_gmd,
                                 sessionCallback=init_session)

    return pool

################################################################################
#
# create_schema(): drop and create the demo table, and add a row
#
def create_schema():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("""
        begin

            begin
            execute immediate 'drop table UNI_SUB';
            exception when others then
                if sqlcode <> -942 then
                raise;
                end if;
            end;

            begin
            execute immediate 'drop table UNIVERSITY';
            exception when others then
              if sqlcode <> -942 then
                raise;
              end if;
            end;

            begin
            execute immediate 'drop table SUBJECT';
            exception when others then
                if sqlcode <> -942 then
                raise;
                end if;
            end;            

            
            
            execute immediate 'CREATE TABLE UNIVERSITY(UNI_ID VARCHAR2(4) NOT NULL PRIMARY KEY,NAME VARCHAR2(60) NOT NULL,LOCATION VARCHAR(255) NOT NULL)';
            execute immediate 'CREATE TABLE SUBJECT(SUB_ID VARCHAR2(4) NOT NULL PRIMARY KEY,NAME VARCHAR2(60) NOT NULL)';
            execute immediate 'CREATE TABLE UNI_SUB(
                UNI_ID VARCHAR2(4) REFERENCES UNIVERSITY(UNI_ID),
                SUB_ID VARCHAR2(4) REFERENCES SUBJECT(SUB_ID),
                CAPASITY INT,
                QUOTA_CAPASITY INT
            )'; 


            -- populate UNIVERSITY

            execute immediate 'INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES(''BUET'',''Bangladesh University of Engineering and Technology'', ''Dhaka-1000'')';
            execute immediate 'INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES(''KUET'',''Khulna University of Engineering and Technology'', ''Fulbarigate,Khulna'')';
            execute immediate 'INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES(''RUET'',''Rajshahi University of Engineering and Technology'', ''Kazla, Rajshahi-6204'')';
           
            -- populate subject
            
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''ARCH'',''Architecture'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''BECM'',''Building Engineering and Construction Management'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''BME'',''Biomedical Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''CE'',''Civil Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''CFPE'',''Chemical and Food Process Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''CHE'',''Chemical Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''CSE'',''Computer Science and Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''ECE'',''Electrical and Computer Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''EEE'',''Electrical and Electronics Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''ESE'',''Energy Science and Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''ETE'',''Electronics and Telecommunication Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''GCE'',''Glass and Ceramic Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''IEM'',''Industrial Engineering and Management'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''IPE'',''Industrial and Production Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''LE'',''Lather Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''MSE'',''Material Science and Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''ME'',''Mechanical Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''MIE'',''Mechatronics and Industrial Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''MTE'',''Mechatronics Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''TE'',''Textile Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''PME'',''Petrolium and Mining Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''URP'',''Urbal and Regional Planning'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''WRE'',''Water Resources Engineering'')';
            commit;
        end;""")
    


################################################################################
#
# Specify some routes
#
# The default route will display a welcome message:
#   http://127.0.0.1:8080/
#
# To insert a new user 'fred' you can call:
#    http://127.0.0.1:8080/post/fred
#
# To find a username you can pass an id, for example 1:
#   http://127.0.0.1:8080/user/1
#

app = Flask(__name__)

# Display a welcome message on the 'home' page
@app.route('/')
def index():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SUBJECT")
    query_result = cursor.fetchall()
    return render_template('index.html',context=query_result)


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
    # app.run(port=int(os.environ.get('PORT', '8080')))
    app.run(port=int(1520))