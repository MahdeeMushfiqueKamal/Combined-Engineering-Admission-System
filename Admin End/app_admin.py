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

    pool = cx_Oracle.SessionPool(user="C##CEAS_ADMIN",password=os.environ.get('PYTHON_DB_PASSWORD'),dsn=os.environ.get('PYTHON_CONNECTSTRING'), min=pool_min,max=pool_max,increment=pool_inc,threaded=True,getmode=pool_gmd,sessionCallback=init_session)
    return pool

################################################################################


app = Flask(__name__)
app.secret_key  = '36610328caf5968c435a13abc5d70b4d'

# Display a welcome message on the 'home' page
@app.route('/')
def index():
    flash_msg = get_flashed_messages()
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute('''SELECT ADMIN_MESSAGE,TO_CHAR(APPLY_FIRST_DATE,'Month DD, YYYY'),TO_CHAR(APPLY_LAST_DATE,'Month DD, YYYY'),
    TO_CHAR(EXAM_DATE,'Month DD, YYYY'),TO_CHAR(RESULT_DATE,'Month DD, YYYY'),TO_CHAR(MIGRATION_DATE,'Month DD, YYYY') 
    FROM C##CEAS_ADMIN.GLOBAL_DATA ORDER BY ENTRY_NO''')
    GLOBAL_DATA = cursor.fetchall()

    return render_template('index.html',flash_msg=flash_msg, GLOBAL_DATA=GLOBAL_DATA)

@app.route('/dashboard/<examinee_id>')
def dashboard(examinee_id):
    flash_msg = get_flashed_messages()
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute('SELECT * from EXAMINEE WHERE EXAMINEE_ID = :id',[examinee_id])
    examinee_details = cursor.fetchone()
    print(examinee_details)
    if examinee_details == None:
        abort(404)
    cursor.execute('SELECT NAME,LOCATION FROM EXAM_CENTER WHERE CENTER_ID = (SELECT CENTER_ID FROM EXAMINEE WHERE EXAMINEE_ID = :id)',[examinee_id])
    center_details = cursor.fetchone()
    print(center_details)
    return render_template('dashboard.html',examinee_details=examinee_details, center_details=center_details,flash_msg=flash_msg)

@app.route('/process_update',methods=['POST'])
def process_update():
    print("Process Update called")
    print(request.form)
    connection = pool.acquire()
    cursor = connection.cursor()

    start_date = request.form['app-start-date'] 
    end_date = request.form['app-end-date'] 
    exam_date = request.form['exam-date'] 
    result_date = request.form['result-date']
    mig_date = request.form['mig-date']
    state = request.form['state']
    msg = request.form['admin-msg']

    print(start_date, end_date, exam_date, result_date, mig_date, state, msg)

    
    if start_date != "":
        query_str = "UPDATE C##CEAS_ADMIN.GLOBAL_DATA SET APPLY_FIRST_DATE = TO_DATE('" + str(start_date) + "','YYYY-MM-DD')"
        print(query_str)
        cursor.execute(query_str)

    if end_date != "":
        query_str = "UPDATE C##CEAS_ADMIN.GLOBAL_DATA SET APPLY_LAST_DATE = TO_DATE('" + str(end_date) + "','YYYY-MM-DD')"
        print(query_str)
        cursor.execute(query_str)
    if exam_date != "":
        query_str = "UPDATE C##CEAS_ADMIN.GLOBAL_DATA SET EXAM_DATE = TO_DATE('" + str(exam_date) + "','YYYY-MM-DD')"
        print(query_str)
        cursor.execute(query_str)
    if result_date != "":
        query_str = "UPDATE C##CEAS_ADMIN.GLOBAL_DATA SET RESULT_DATE = TO_DATE('" + str(result_date) + "','YYYY-MM-DD')"
        print(query_str)
        cursor.execute(query_str)
    if mig_date != "":
        query_str = "UPDATE C##CEAS_ADMIN.GLOBAL_DATA SET MIGRATION_DATE = TO_DATE('" + str(mig_date) + "','YYYY-MM-DD')"
        print(query_str)
        cursor.execute(query_str)
    if state != "":
        query_str = "UPDATE C##CEAS_ADMIN.GLOBAL_DATA SET SYSTEM_STATE = " + state
        print(query_str)
        cursor.execute(query_str)
    if msg != "":
        query_str = "UPDATE C##CEAS_ADMIN.GLOBAL_DATA SET ADMIN_MESSAGE = '" + str(msg) + "'"
        print(query_str)
        cursor.execute(query_str)
    

    flash_msg = 'Successfully Updated Global Data'
    flash(flash_msg)
    return redirect(url_for('index'))

    # ENTRY_NO INTEGER NOT NULL,
	# SYSTEM_STATE INTEGER DEFAULT 1,
	# APPLY_FIRST_DATE DATE DEFAULT SYSDATE,
	# APPLY_LAST_DATE DATE DEFAULT to_date('5-4-2022','dd-mm-yyyy'),
	# EXAM_DATE DATE DEFAULT to_date('14-05-2022','dd-mm-yyyy'),
	# RESULT_DATE DATE DEFAULT to_date('1-06-2022','dd-mm-yyyy'),
	# MIGRATION_DATE DATE DEFAULT to_date('15-06-2022','dd-mm-yyyy'),
	# ADMIN_MESSAGE VARCHAR2(4000)





@app.route('/merit_list/<int:page>')
def merit_list(page):
    if page > 50 or page <1:
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

    app.run(port=int(1530), debug = True)