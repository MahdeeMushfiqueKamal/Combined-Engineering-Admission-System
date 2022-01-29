import random
fhand = open('Full_Names.txt')
NAMES = list()

for line in fhand.readlines():
    line = line.strip()
    NAMES.append(line)
fhand.close()

fhand = open('2.populate_examinee.sql','w')
#just a housekeeping before write query
querystr = '''
UPDATE EXAM_CENTER SET FILLED = 0 WHERE CENTER_ID = 'BUET';
UPDATE EXAM_CENTER SET FILLED = 0 WHERE CENTER_ID = 'CUET';
UPDATE EXAM_CENTER SET FILLED = 0 WHERE CENTER_ID = 'KUET';
UPDATE EXAM_CENTER SET FILLED = 0 WHERE CENTER_ID = 'RUET';
UPDATE EXAM_CENTER SET FILLED = 0 WHERE CENTER_ID = 'SUST';
'''
fhand.write(querystr)

DAY = range(1,29)
MONTH = range(1,13)
YEAR = [2003,2004]
LOCATION = ['BUET','RUET','CUET','SUST']
HSC_ROLL_pool = range(1234567,6666666)
HSC_REG_pool = range(123456789, 666666666)

HSC_ROLL = list()
HSC_REG = list()

for i in range(40000):
    HSC_ROLL.append(random.choice(HSC_ROLL_pool))
    HSC_REG.append(random.choice(HSC_REG_pool))

HSC_ROLL = list(set(HSC_ROLL))
HSC_REG = list(set(HSC_REG))

mark_ranges = range(40,160,20)
offsets = range(-10,11)

for i in range(7000):
    birthday = str(random.choice(YEAR))+'/'+str(random.choice(MONTH))+'/'+str(random.choice(DAY))
    quota_status ='\'Y\'' if 'Chakma' in NAMES[i] or 'Marma' in NAMES[i] else '\'N\''
    center_id = random.choice(LOCATION)
    center_id = 'KUET'
    querystr = 'INSERT INTO EXAMINEE(EXAMINEE_ID,HSC_ROLL,HSC_REG,NAME,BIRTHDATE,QUOTA_STATUS,CENTER_ID) VALUES(new_sequence.NEXTVAL,'+ str(HSC_ROLL[i])+','+ str(HSC_REG[i])+',\''+NAMES[i].strip()+'\',TO_DATE(\''+birthday+'\',\'YYYY/MM/DD\'),'+quota_status+',\''+center_id+'\');\n'
    fhand.write(querystr)
    querystr = 'UPDATE EXAM_CENTER SET FILLED = (SELECT FILLED FROM EXAM_CENTER WHERE CENTER_ID=\''+ center_id +'\' ) + 1 WHERE CENTER_ID=\''+center_id+'\';\n' 
    fhand.write(querystr)

    mark_range = random.choice(mark_ranges)
    phy = str(mark_range + random.choice(offsets))
    chm = str(mark_range + random.choice(offsets))
    math = str(mark_range + random.choice(offsets))
    query_str = 'UPDATE EXAMINEE SET PHY_MARK= '+ phy +', MATH_MARK= '+ math +', CHM_MARK= '+ chm +' WHERE HSC_ROLL = '+ str(HSC_ROLL[i]) +';\n'
    fhand.write(query_str)

for i in range(7001,len(NAMES)):
    birthday = str(random.choice(YEAR))+'/'+str(random.choice(MONTH))+'/'+str(random.choice(DAY))
    quota_status ='\'Y\'' if 'Chakma' in NAMES[i] or 'Marma' in NAMES[i] else '\'N\''
    center_id = random.choice(LOCATION)
    
    querystr = 'INSERT INTO EXAMINEE(EXAMINEE_ID,HSC_ROLL,HSC_REG,NAME,BIRTHDATE,QUOTA_STATUS,CENTER_ID) VALUES(new_sequence.NEXTVAL,'+ str(HSC_ROLL[i])+','+ str(HSC_REG[i])+',\''+NAMES[i].strip()+'\',TO_DATE(\''+birthday+'\',\'YYYY/MM/DD\'),'+quota_status+',\''+center_id+'\');\n'
    fhand.write(querystr)
    querystr = 'UPDATE EXAM_CENTER SET FILLED = (SELECT FILLED FROM EXAM_CENTER WHERE CENTER_ID=\''+ center_id +'\' ) + 1 WHERE CENTER_ID=\''+center_id+'\';\n' 
    fhand.write(querystr)

    mark_range = random.choice(mark_ranges)
    phy = str(mark_range + random.choice(offsets))
    chm = str(mark_range + random.choice(offsets))
    math = str(mark_range + random.choice(offsets))
    query_str = 'UPDATE EXAMINEE SET PHY_MARK= '+ phy +', MATH_MARK= '+ math +', CHM_MARK= '+ chm +' WHERE HSC_ROLL = '+ str(HSC_ROLL[i]) +';\n'
    fhand.write(query_str)
