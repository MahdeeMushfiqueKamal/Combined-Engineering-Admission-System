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
            execute immediate 'INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES(''CUET'',''Chittagong University of Engineering and Technology'', ''Chittagong'')';
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
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''MME'',''Materials and Metallurgical Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''MTE'',''Mechatronics Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''NAME'',''Naval Architecture and Marine Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''TE'',''Textile Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''PME'',''Petrolium and Mining Engineering'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''URP'',''Urbal and Regional Planning'')';
            execute immediate 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(''WRE'',''Water Resources Engineering'')';

            -- populate Uni-Sub

            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''ARCH'',55,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''BME'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''CE'',195,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''CHE'',60,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''CSE'',120,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''EEE'',195,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''IPE'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''NAME'',55,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''ME'',180,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''MME'',50,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''URP'',30,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''BUET'',''WRE'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''ARCH'',30,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''BME'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''CE'',130,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''CSE'',130,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''EEE'',180,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''ETE'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''MSE'',30,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''ME'',180,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''MIE'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''PME'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''URP'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''CUET'',''WRE'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''ARCH'',40,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''BECM'',60,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''BME'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''CHE'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''CE'',120,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''CSE'',120,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''EEE'',120,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''ECE'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''ESE'',30,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''IEM'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''LE'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''MSE'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''ME'',120,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''MTE'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''TE'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''KUET'',''URP'',60,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''ARCH'',30,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''BECM'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''CFPE'',30,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''CE'',180,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''CSE'',180,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''EEE'',180,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''ECE'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''ETE'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''GCE'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''IPE'',60,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''ME'',180,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''MSE'',60,0)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''MTE'',60,1)';
            execute immediate 'INSERT INTO UNI_SUB(UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES(''RUET'',''URP'',60,1)';

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