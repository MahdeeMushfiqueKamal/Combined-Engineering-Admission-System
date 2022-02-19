from fileinput import filename
import os,sys,hashlib,cx_Oracle
from pathlib import Path
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
    pool = cx_Oracle.SessionPool(user="C##CEAS_USER",password=os.environ.get('PYTHON_DB_PASSWORD'),dsn=os.environ.get('PYTHON_CONNECTSTRING'), min=pool_min,max=pool_max,increment=pool_inc,threaded=True,getmode=pool_gmd,sessionCallback=init_session)
    return pool

################################################################################

app = Flask(__name__)
app.secret_key  = '36610328caf5968c435a13abc5d70b4c'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.UPLOAD_PATH = str(Path(__file__).parent.absolute()) + '\\static\\profile_pic\\'


# Display a welcome message on the 'home' page
@app.route('/')
def index():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute('''SELECT S.NAME, US.CAPASITY, US.QUOTA_CAPASITY FROM C##CEAS_ADMIN.UNI_SUB US 
    JOIN C##CEAS_ADMIN.SUBJECT S ON US.SUB_ID = S.SUB_ID WHERE US.UNI_ID = 'BUET'
    ''')
    BUET_SEATS = cursor.fetchall()

    cursor.execute('''SELECT S.NAME, US.CAPASITY, US.QUOTA_CAPASITY FROM C##CEAS_ADMIN.UNI_SUB US 
    JOIN C##CEAS_ADMIN.SUBJECT S ON US.SUB_ID = S.SUB_ID WHERE US.UNI_ID = 'CUET'
    ''')
    CUET_SEATS = cursor.fetchall()

    cursor.execute('''SELECT S.NAME, US.CAPASITY, US.QUOTA_CAPASITY FROM C##CEAS_ADMIN.UNI_SUB US 
    JOIN C##CEAS_ADMIN.SUBJECT S ON US.SUB_ID = S.SUB_ID WHERE US.UNI_ID = 'KUET'
    ''')
    KUET_SEATS = cursor.fetchall()

    cursor.execute('''SELECT S.NAME, US.CAPASITY, US.QUOTA_CAPASITY FROM C##CEAS_ADMIN.UNI_SUB US 
    JOIN C##CEAS_ADMIN.SUBJECT S ON US.SUB_ID = S.SUB_ID WHERE US.UNI_ID = 'RUET'
    ''')
    RUET_SEATS = cursor.fetchall()

    cursor.execute('''SELECT ADMIN_MESSAGE,TO_CHAR(APPLY_FIRST_DATE,'Month DD, YYYY'),TO_CHAR(APPLY_LAST_DATE,'Month DD, YYYY'),
    TO_CHAR(EXAM_DATE,'Month DD, YYYY'),TO_CHAR(RESULT_DATE,'Month DD, YYYY'), TO_CHAR(MIGRATION_DATE,'Month DD, YYYY')
    FROM C##CEAS_ADMIN.GLOBAL_DATA ORDER BY ENTRY_NO''')
    GLOBAL_DATA = cursor.fetchall()
    print(GLOBAL_DATA)

    return render_template('index.html',BUET_SEATS=BUET_SEATS, CUET_SEATS = CUET_SEATS, KUET_SEATS= KUET_SEATS, 
    RUET_SEATS = RUET_SEATS,GLOBAL_DATA=GLOBAL_DATA)

@app.route('/apply')
def apply():
    flash_msg = get_flashed_messages()
    print(flash_msg)
    connection = pool.acquire()
    cursor = connection.cursor()
    seats = cursor.execute('SELECT CENTER_ID,CAPASITY-FILLED FROM C##CEAS_ADMIN.EXAM_CENTER').fetchall()
    print('printing seats',seats)
    return render_template('apply_form.html',flash_msg=flash_msg,seats=seats)

@app.route('/process_apply',methods=['POST'])
def process_apply():
    print(request.form)
    connection = pool.acquire()
    cursor = connection.cursor()

    hsc_roll = request.form['HSC_ROLL'] 
    hsc_reg = request.form['HSC_REG'] 
    name = request.form['NAME'] 
    password = request.form['PASS'] 
    re_password = request.form['REPASS']
    birth_date = request.form['DATE_OF_BIRTH']
    quota_status = 'Y' if request.form.get('QUOTA_STATUS') else 'N'
    center = request.form.get('CENTER')

    if len(hsc_roll)!= 7 or len(hsc_reg)!=9 or len(name)==0 or len(password) ==0 or len(birth_date)==0:
        flash('Enter your data properly')
        return redirect('apply')
    query_str = 'SELECT * FROM C##CEAS_ADMIN.EXAMINEE WHERE HSC_ROLL = '+hsc_roll+' OR HSC_REG = '+hsc_reg
    cursor.execute(query_str)
    if cursor.fetchone() != None:
        flash('HSC ROLL or HSC Registration already exists. Try again or Log into dashboard')
        return redirect('apply')
    
    if password != re_password:
        flash('Re Enter your password Properly')
        return redirect('apply')
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    if center == None:
        flash('Select your Exam Center')
        return redirect('apply')

    query_str = 'INSERT INTO C##CEAS_ADMIN.EXAMINEE_PERSONAL(EXAMINEE_ID,HSC_ROLL,HSC_REG,NAME,BIRTHDATE,QUOTA_STATUS,CENTER_ID,PASSWORD) VALUES(C##CEAS_ADMIN.new_sequence.NEXTVAL,'+hsc_roll+','+hsc_reg+',\''+name+'\',\''+birth_date+'\',\''+quota_status+'\',\''+center+'\',\''+password+'\')'
    cursor.execute(query_str)
    query_str = 'UPDATE C##CEAS_ADMIN.EXAM_CENTER SET FILLED = (SELECT FILLED FROM C##CEAS_ADMIN.EXAM_CENTER WHERE CENTER_ID=\'' + center +'\' ) + 1 WHERE CENTER_ID=\''+center+'\''
    cursor.execute(query_str)
    connection.commit()
    query_str = 'SELECT EXAMINEE_ID FROM C##CEAS_ADMIN.EXAMINEE WHERE HSC_ROLL = '+hsc_roll 
    cursor.execute(query_str)
    examinee_id = cursor.fetchone()[0]

    # uploading image 
    picture = request.files.get('PICTURE')
    print(picture)
    if picture.filename != '':
        file_name = app.UPLOAD_PATH + str(examinee_id) + '.png'
        print(file_name)
        picture.save(file_name)
        query_str = 'UPDATE C##CEAS_ADMIN.EXAMINEE_PERSONAL SET IMAGE_URL = \''+str(examinee_id)+'.png\' WHERE EXAMINEE_ID = '+str(examinee_id)
        print(query_str)
        cursor.execute(query_str)
        connection.commit()
    
    flash_msg = "Successfully Registered. Your Examinee Id is " + str(examinee_id) + ' Now Log in'
    flash(flash_msg)
    return redirect(url_for('login'))

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('examinee_id',None)
    flash('Successfully Logged Out')
    return redirect(url_for('login'))

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        flash_msg = get_flashed_messages()
        return render_template('login.html',flash_msg=flash_msg)
    elif request.method == 'POST':
        print(request.form)
        examinee_id = request.form['EXAMINEE_ID'] 
        password = request.form['PASS'] 
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        connection = pool.acquire()
        cursor = connection.cursor()
        query_str = 'SELECT * FROM C##CEAS_ADMIN.EXAMINEE WHERE EXAMINEE_ID = ' + examinee_id +' AND PASSWORD = \''+ password +'\''
        print(query_str)
        cursor.execute(query_str)
        if len(cursor.fetchall()) == 1:
            flash('Successfully Logged in')
            session['examinee_id'] = examinee_id
            return redirect(url_for('dashboard',examinee_id=examinee_id))
        else:
            flash('Incorrect Examinee Id or Password, Try again')
            return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard_redirect():
    if 'examinee_id' not in session:
        flash('You need to login before entering Dashboard')
        return redirect(url_for('login'))
    examinee_id = session['examinee_id']
    return redirect(url_for('dashboard',examinee_id=examinee_id))

@app.route('/dashboard/<examinee_id>')
def dashboard(examinee_id):
    flash_msg = get_flashed_messages()
    if 'examinee_id' not in session:
        flash('You need to login before entering Dashboard')
        return redirect(url_for('login'))
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute('SELECT * from C##CEAS_ADMIN.EXAMINEE WHERE EXAMINEE_ID = :id',[examinee_id])
    examinee_details = cursor.fetchone()
    print(examinee_details)
    if examinee_details == None:
        abort(404)
    cursor.execute('SELECT NAME,LOCATION FROM C##CEAS_ADMIN.EXAM_CENTER WHERE CENTER_ID = (SELECT CENTER_ID FROM C##CEAS_ADMIN.EXAMINEE WHERE EXAMINEE_ID = :id)',[examinee_id])
    center_details = cursor.fetchone()
    print(center_details)
    return render_template('dashboard.html',examinee_details=examinee_details, center_details=center_details,flash_msg=flash_msg)

@app.route('/merit_list/<int:page>')
def merit_list(page):
    if page > 50 or page <1:
        abort(404)
    
    connection = pool.acquire()
    cursor = connection.cursor()
    query_str = 'SELECT MERIT_POS, EXAMINEE_ID, NAME, PHY_MARK, CHM_MARK, MATH_MARK FROM C##CEAS_ADMIN.EXAMINEE WHERE MERIT_POS IS NOT NULL ORDER BY MERIT_POS'
    cursor.execute(query_str)
    merit_rows = cursor.fetchall()    
    
    return render_template('merit_list.html',merit_rows=merit_rows,page=page)


@app.route('/quota_merit_list')
def quota_merit_list():
    connection = pool.acquire()
    cursor = connection.cursor()
    query_str = 'SELECT QUOTA_POS, EXAMINEE_ID, NAME, PHY_MARK, CHM_MARK, MATH_MARK FROM C##CEAS_ADMIN.EXAMINEE WHERE QUOTA_POS IS NOT NULL ORDER BY QUOTA_POS'
    cursor.execute(query_str)
    quota_rows = cursor.fetchall()
    return render_template('quota_merit_list.html',quota_rows=quota_rows)

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
    app.run(port=int(1520), debug=True)