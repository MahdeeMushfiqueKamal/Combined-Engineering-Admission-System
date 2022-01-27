import os
from sqlite3 import Cursor
import sys
import cx_Oracle
from flask import Flask,render_template, url_for, redirect, abort
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
    print('Creating Schema...')
    connection = pool.acquire()
    cursor = connection.cursor()
    fhand = open('supporting functions/DDL.sql')
    cursor.execute(fhand.read())
    fhand.close()
    
    print("Populating Tables...")
    fhand = open('supporting functions/populate_table.sql')
    for line in fhand.readlines():
        line = line.replace(';','').strip()
        #print(line)
        cursor.execute(line)
    connection.commit()
    fhand.close()

    print('Populating Examinee table...')
    fhand = open('supporting functions/populate_examinee_small.sql')
    for line in fhand.readlines():
        line = line.replace(';','').strip()
        #print(line)
        cursor.execute(line)
    connection.commit()
    fhand.close()


    cursor.execute('SELECT CENTER_ID,FILLED FROM EXAM_CENTER')
    for line in cursor.fetchall():
        for item in line:
            print(item, end=' \t')
        print('')

    print('Updating Examinee marks...')
    fhand = open('supporting functions/update_marks_small.sql')
    for line in fhand.readlines():
        line = line.replace(';','').strip()
        #print(line)
        cursor.execute(line)
    connection.commit()
    fhand.close()
    

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

    return render_template('index.html',BUET_SEATS=BUET_SEATS, CUET_SEATS = CUET_SEATS, KUET_SEATS= KUET_SEATS, 
    RUET_SEATS = RUET_SEATS)

@app.route('/dashboard/<examinee_id>')
def dashboard(examinee_id):
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute('SELECT * from EXAMINEE WHERE EXAMINEE_ID = :id',[examinee_id])
    examinee_details = cursor.fetchone()
    print(examinee_details)
    cursor.execute('SELECT NAME,LOCATION FROM EXAM_CENTER WHERE CENTER_ID = (SELECT CENTER_ID FROM EXAMINEE WHERE EXAMINEE_ID = :id)',[examinee_id])
    center_details = cursor.fetchone()
    print(center_details)
    return render_template('dashboard.html',examinee_details=examinee_details, center_details=center_details)

@app.route('/merit_list/<int:page>')
def merit_list(page):
    if page >= 50 or page <1:
        abort(404)
    
    connection = pool.acquire()
    cursor = connection.cursor()
    query_str = 'SELECT MERIT_POS, EXAMINEE_ID, NAME, PHY_MARK, CHM_MARK, MATH_MARK FROM EXAMINEE WHERE MERIT_POS IS NOT NULL ORDER BY MERIT_POS'
    cursor.execute(query_str)
    merit_rows = cursor.fetchall()    
    
    return render_template('merit_list.html',merit_rows=merit_rows,page=page)


@app.route('/quota_merit_list')
def quota_merit_list():
    connection = pool.acquire()
    cursor = connection.cursor()
    query_str = 'SELECT QUOTA_POS, EXAMINEE_ID, NAME, PHY_MARK, CHM_MARK, MATH_MARK FROM EXAMINEE WHERE QUOTA_POS IS NOT NULL ORDER BY QUOTA_POS'
    cursor.execute(query_str)
    quota_rows = cursor.fetchall()
    return render_template('quota_merit_list.html',quota_rows=quota_rows)

@app.route('/admin/generate_merit_list')
def generate_merit_list():
    connection = pool.acquire()
    cursor = connection.cursor()
    #for merit list
    query_str = '''SELECT RANK() OVER( ORDER BY MATH_MARK+PHY_MARK+CHM_MARK DESC, MATH_MARK DESC, PHY_MARK DESC, 
    CHM_MARK DESC, BIRTHDATE DESC, NAME ASC ) table_rank,EXAMINEE_ID 
    FROM EXAMINEE OFFSET 0 ROWS FETCH NEXT 5000 ROWS ONLY'''

    cursor.execute(query_str)
    rows = cursor.fetchall()
    for row in rows: 
        query_str = 'UPDATE EXAMINEE SET MERIT_POS = '+str(row[0])+' WHERE EXAMINEE_ID = '+str(row[1])
        cursor.execute(query_str)
    
    #for quota list
    query_str = '''SELECT RANK() OVER( ORDER BY MATH_MARK+PHY_MARK+CHM_MARK DESC, MATH_MARK DESC, PHY_MARK DESC, 
    CHM_MARK DESC, BIRTHDATE DESC, NAME ASC ) table_rank,EXAMINEE_ID 
    FROM EXAMINEE WHERE QUOTA_STATUS=\'Y\' OFFSET 0 ROWS FETCH NEXT 100 ROWS ONLY'''

    cursor.execute(query_str)
    rows = cursor.fetchall()
    for row in rows: 
        query_str = 'UPDATE EXAMINEE SET QUOTA_POS = '+str(row[0])+' WHERE EXAMINEE_ID = '+str(row[1])
        cursor.execute(query_str)

    connection.commit()
    return redirect(url_for('merit_list',page=1))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

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