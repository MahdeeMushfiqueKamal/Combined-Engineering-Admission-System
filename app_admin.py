import os,sys,hashlib,cx_Oracle
from flask import *

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

    pool = cx_Oracle.SessionPool(user="C##CEAS_ADMIN",password="1234",dsn="127.0.0.1/rainbow", min=pool_min,max=pool_max,increment=pool_inc,threaded=True,getmode=pool_gmd,sessionCallback=init_session)
    return pool

################################################################################


app = Flask(__name__)
app.secret_key  = '36610328caf5968c435a13abc5d70b4d'

# Display a welcome message on the 'home' page
@app.route('/')
def index():
    flash_msg = get_flashed_messages()
    return render_template('admin_index.html',flash_msg=flash_msg)
    #return "admin Page"

# @app.route('/dashboard/<examinee_id>')
# def dashboard(examinee_id):
#     flash_msg = get_flashed_messages()
#     connection = pool.acquire()
#     cursor = connection.cursor()
#     cursor.execute('SELECT * from EXAMINEE WHERE EXAMINEE_ID = :id',[examinee_id])
#     examinee_details = cursor.fetchone()
#     print(examinee_details)
#     if examinee_details == None:
#         abort(404)
#     cursor.execute('SELECT NAME,LOCATION FROM EXAM_CENTER WHERE CENTER_ID = (SELECT CENTER_ID FROM EXAMINEE WHERE EXAMINEE_ID = :id)',[examinee_id])
#     center_details = cursor.fetchone()
#     print(center_details)
#     return render_template('dashboard.html',examinee_details=examinee_details, center_details=center_details,flash_msg=flash_msg)

# @app.route('/merit_list/<int:page>')
# def merit_list(page):
#     if page > 50 or page <1:
#         abort(404)
    
#     connection = pool.acquire()
#     cursor = connection.cursor()
#     query_str = 'SELECT MERIT_POS, EXAMINEE_ID, NAME, PHY_MARK, CHM_MARK, MATH_MARK FROM EXAMINEE WHERE MERIT_POS IS NOT NULL ORDER BY MERIT_POS'
#     cursor.execute(query_str)
#     merit_rows = cursor.fetchall()    
    
#     return render_template('merit_list.html',merit_rows=merit_rows,page=page)


# @app.route('/quota_merit_list')
# def quota_merit_list():
#     connection = pool.acquire()
#     cursor = connection.cursor()
#     query_str = 'SELECT QUOTA_POS, EXAMINEE_ID, NAME, PHY_MARK, CHM_MARK, MATH_MARK FROM EXAMINEE WHERE QUOTA_POS IS NOT NULL ORDER BY QUOTA_POS'
#     cursor.execute(query_str)
#     quota_rows = cursor.fetchall()
#     return render_template('quota_merit_list.html',quota_rows=quota_rows)

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
    flash('Merit List has been generated')
    return redirect(url_for('index'))


@app.route('/admin/generate_mark_list')
def generate_mark_list():
    connection = pool.acquire()
    cursor = connection.cursor()

    flash('Boo')
    return redirect(url_for('index'))



@app.route('/admin/update_application_date')
def update_application_date():
    connection = pool.acquire()
    cursor = connection.cursor()
    flash('Boo')

    return redirect(url_for('index'))

@app.route('/admin/update_exam_date')
def update_exam_date():
    connection = pool.acquire()
    cursor = connection.cursor()
    flash('Boo')

    return redirect(url_for('index'))



@app.route('/admin/update_msg')
def update_msg():
    connection = pool.acquire()
    cursor = connection.cursor()
    flash('Boo')

    return redirect(url_for('index'))




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

    # Start a webserver
    app.run(port=int(1530))