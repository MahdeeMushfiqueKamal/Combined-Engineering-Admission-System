import os,sys,hashlib,cx_Oracle
from sqlite3 import Cursor
from django.db import connection
from flask import *
from matplotlib.pyplot import connect

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
    FROM C##CEAS_ADMIN.GLOBAL_DATA WHERE ENTRY_NO = 1''')
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
        query_str = "UPDATE GLOBAL_DATA SET APPLY_FIRST_DATE = TO_DATE('" + str(start_date) + "','YYYY-MM-DD') WHERE ENTRY_NO = 1"
        print(query_str)
        cursor.execute(query_str)

    if end_date != "":
        query_str = "UPDATE GLOBAL_DATA SET APPLY_LAST_DATE = TO_DATE('" + str(end_date) + "','YYYY-MM-DD') WHERE ENTRY_NO = 1"
        print(query_str)
        cursor.execute(query_str)
    if exam_date != "":
        query_str = "UPDATE GLOBAL_DATA SET EXAM_DATE = TO_DATE('" + str(exam_date) + "','YYYY-MM-DD') WHERE ENTRY_NO = 1"
        print(query_str)
        cursor.execute(query_str)
    if result_date != "":
        query_str = "UPDATE GLOBAL_DATA SET RESULT_DATE = TO_DATE('" + str(result_date) + "','YYYY-MM-DD') WHERE ENTRY_NO = 1"
        print(query_str)
        cursor.execute(query_str)
    if mig_date != "":
        query_str = "UPDATE GLOBAL_DATA SET MIGRATION_DATE = TO_DATE('" + str(mig_date) + "','YYYY-MM-DD') WHERE ENTRY_NO = 1"
        print(query_str)
        cursor.execute(query_str)
    if state != '0':
        query_str = "UPDATE GLOBAL_DATA SET SYSTEM_STATE = " + state + ' WHERE ENTRY_NO = 1'
        print(query_str)
        cursor.execute(query_str)
    if msg != "":
        query_str = "UPDATE GLOBAL_DATA SET ADMIN_MESSAGE = '" + str(msg) + "' WHERE ENTRY_NO = 1"
        print(query_str)
        cursor.execute(query_str)
    
    connection.commit()

    flash_msg = 'Successfully Updated Global Data'
    flash(flash_msg)
    return redirect(url_for('index'))

@app.route('/update_marks',methods=['POST'])
def update_marks():
    print("Mark Update called")
    print(request.form)
    connection = pool.acquire()
    cursor = connection.cursor()

    examinee_id = request.form['EXAMINEE_ID']
    math_mark = request.form['MATH_MARK'] 
    phy_mark = request.form['PHY_MARK'] 
    chm_mark = request.form['CHM_MARK'] 

    query_str = 'SELECT * FROM EXAMINEE WHERE EXAMINEE_ID = '+examinee_id
    cursor.execute(query_str)
    if cursor.fetchone() == None:
        flash_msg = 'Examinee Does not exists! '
        flash(flash_msg)
        return redirect(url_for('index'))

    if math_mark == "" or phy_mark == "" or chm_mark=='':
        flash_msg = 'Marks can not be empty!'
        flash(flash_msg)
        return redirect(url_for('index'))
    elif not math_mark.isdigit() or not phy_mark.isdigit() or not chm_mark.isdigit():
        flash_msg = 'Marks must be numbers!'
        flash(flash_msg)
        return redirect(url_for('index'))
    elif not (int(math_mark) >= 0 and int(math_mark)<=200 and int(phy_mark) >= 0 and int(phy_mark)<=200 and int(chm_mark) >= 0 and int(chm_mark)<=200):
        flash_msg = 'Marks must be between 0 to 200!'
        flash(flash_msg)
        return redirect(url_for('index'))    
    else:    
        query_str = "UPDATE EXAMINEE SET MATH_MARK = " + str(math_mark) + ' ,PHY_MARK = ' + str(phy_mark) + " ,CHM_MARK = " + str(chm_mark) + " WHERE EXAMINEE_ID = " + examinee_id
        print(query_str)
        cursor.execute(query_str)
        connection.commit()
        flash_msg = 'Successfully Updated The Marks for Examinee ID ' + examinee_id
        flash(flash_msg)
        return redirect(url_for('index'))


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
    cursor.execute('DELETE FROM CHOICE_LIST')
    cursor.execute('DELETE FROM MERIT_LIST')
    #for merit list
    query_str = '''
    DECLARE
		rnk NUMBER;
		ex_id NUMBER;
    BEGIN
        for r in (SELECT RANK() OVER( ORDER BY MATH_MARK+PHY_MARK+CHM_MARK DESC, MATH_MARK DESC, PHY_MARK DESC, CHM_MARK DESC, BIRTHDATE DESC, NAME ASC ) table_rank,EXAMINEE_ID FROM EXAMINEE OFFSET 0 ROWS FETCH NEXT 5000 ROWS ONLY)
        LOOP 
            rnk := r.TABLE_RANK;
            ex_id := r.EXAMINEE_ID;
            UPDATE EXAMINEE SET MERIT_POS = rnk WHERE EXAMINEE_ID = ex_id;
            INSERT INTO MERIT_LIST(MERIT_POS,EXAMINEE_ID) VALUES(rnk,ex_id); 
        END LOOP;
    END;
    '''
    cursor.execute(query_str)
    
    #for quota list
    query_str = '''
    DECLARE
        q_rnk NUMBER;
        ex_id NUMBER;
	BEGIN
		for r in (SELECT RANK() OVER( ORDER BY MATH_MARK+PHY_MARK+CHM_MARK DESC, MATH_MARK DESC, PHY_MARK DESC, 
        CHM_MARK DESC, BIRTHDATE DESC, NAME ASC ) table_rank,EXAMINEE_ID 
        FROM EXAMINEE WHERE QUOTA_STATUS='Y' OFFSET 0 ROWS FETCH NEXT 100 ROWS ONLY)
        LOOP 
                q_rnk := r.TABLE_RANK;
                ex_id := r.EXAMINEE_ID;
                UPDATE EXAMINEE SET QUOTA_POS = q_rnk WHERE EXAMINEE_ID = ex_id;
        END LOOP;
    END;
    '''
    cursor.execute(query_str)
    connection.commit()
    flash('Merit List has been generated')
    return redirect(url_for('index'))

@app.route('/admin/mark_from_csv',methods=['POST'])
def mark_from_csv():
    connection = pool.acquire()
    cursor = connection.cursor()
    csv_file = request.files.get('CSV_file')
    for line in csv_file.readlines():
        line = line.decode('ascii').strip()
        print(line)
        line = line.split(',')
        if len(line) != 4:
            flash('Invalid input in csv file')
            return redirect(url_for('index'))
        examinee_id = line[0]
        math_mark = line[1]
        phy_mark = line[2]
        chm_mark = line[3]
        print('One line update from CSV: ',examinee_id,math_mark,phy_mark,chm_mark)
        
        query_str = 'SELECT * FROM EXAMINEE WHERE EXAMINEE_ID = '+examinee_id
        cursor.execute(query_str)
        if cursor.fetchone() == None:
            flash_msg = 'Examinee Does not exists! '
            flash(flash_msg)
            return redirect(url_for('index'))
        if not (int(math_mark) >= 0 and int(math_mark)<=200 and int(phy_mark) >= 0 and int(phy_mark)<=200 and int(chm_mark) >= 0 and int(chm_mark)<=200):
            flash_msg = 'Marks must be between 0 to 200! Invalid input in csv file'
            flash(flash_msg)
            return redirect(url_for('index'))    
        else:    
            query_str = "UPDATE EXAMINEE SET MATH_MARK = " + str(math_mark) + ' ,PHY_MARK = ' + str(phy_mark) + " ,CHM_MARK = " + str(chm_mark) + " WHERE EXAMINEE_ID = " + examinee_id
            print(query_str)
            cursor.execute(query_str)
    connection.commit()
    flash('Marks are updated from CSV File')
    return redirect(url_for('index'))

@app.route('/admin/1st_generate_subject_allocation')
def generate_subject_allocation():
    connection = pool.acquire()
    cursor = connection.cursor()
    query_str = '''
    DECLARE
        Available_seat NUMBER;
        us_id NUMBER;
        allotted_sub NUMBER;

    BEGIN
        FOR m_pos IN 1..5000
        LOOP
            --DBMS_OUTPUT.PUT_LINE(M_POS);
            FOR INNER_R IN (SELECT PRIORITY_NO, UNI_SUB_ID FROM CHOICE_LIST WHERE MERIT_POS = m_pos ORDER BY PRIORITY_NO)
            LOOP
                -- FOR each priority-no got a uni sub id
                us_id := INNER_R.UNI_SUB_ID;
                SELECT CAPASITY- FILLED into Available_seat FROM UNI_SUB WHERE UNI_SUB_ID = us_id;
                SELECT ALLOCATED_TO into allotted_sub FROM MERIT_LIST WHERE MERIT_POS = m_pos;
                IF m_pos <10 THEN
                DBMS_OUTPUT.PUT_LINE(m_pos);
                DBMS_OUTPUT.PUT_LINE(us_id);
                DBMS_OUTPUT.PUT_LINE(Available_seat);
                DBMS_OUTPUT.PUT_LINE(allotted_sub);
                END IF;
                IF Available_seat > 0 AND allotted_sub IS NULL THEN
                    UPDATE UNI_SUB SET FILLED = (SELECT FILLED FROM UNI_SUB WHERE UNI_SUB_ID = us_id) + 1 WHERE UNI_SUB_ID = us_id;
                    UPDATE MERIT_LIST SET ALLOCATED_TO = us_id WHERE MERIT_POS = m_pos;
                END IF;
            END LOOP;
        END LOOP;
    END ;
    '''
    cursor.execute(query_str)
    connection.commit()
    flash('Subject Allocation for 1st Run is done')
    return redirect(url_for('index'))


@app.route('/admin/run_migration')
def run_migration():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute('UPDATE UNI_SUB SET FILLED = 0')
    cursor.execute('UPDATE MERIT_LIST SET ALLOCATED_TO = NULL')
    query_str = '''
    DECLARE
		m_pos NUMBER;
		Available_seat NUMBER;
		us_id NUMBER;
		allotted_sub NUMBER;

    BEGIN
        FOR R IN (SELECT MERIT_POS, ADMISSION_STATUS FROM MERIT_LIST ORDER BY MERIT_POS)
        LOOP
            IF R.ADMISSION_STATUS = 'Y' THEN
            m_pos := R.MERIT_POS;
            --DBMS_OUTPUT.PUT_LINE(M_POS);
            FOR INNER_R IN (SELECT PRIORITY_NO, UNI_SUB_ID FROM CHOICE_LIST WHERE MERIT_POS = m_pos ORDER BY PRIORITY_NO)
            LOOP
                -- FOR each priority-no got a uni sub id
                us_id := INNER_R.UNI_SUB_ID;
                SELECT CAPASITY- FILLED into Available_seat FROM UNI_SUB WHERE UNI_SUB_ID = us_id;
                SELECT ALLOCATED_TO into allotted_sub FROM MERIT_LIST WHERE MERIT_POS = m_pos;
                IF Available_seat > 0 AND allotted_sub IS NULL THEN
                        UPDATE UNI_SUB SET FILLED = (SELECT FILLED FROM UNI_SUB WHERE UNI_SUB_ID = us_id) + 1 WHERE UNI_SUB_ID = us_id;
                        UPDATE MERIT_LIST SET ALLOCATED_TO = us_id WHERE MERIT_POS = m_pos;
                END IF;
                END LOOP;
            END IF;
        END LOOP;
    END ;
    '''
    cursor.execute(query_str)
    connection.commit()
    flash('Migration Run is done')
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