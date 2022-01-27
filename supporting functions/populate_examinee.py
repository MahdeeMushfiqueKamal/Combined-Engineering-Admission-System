import random
fhand = open('Full_Names.txt')
NAMES = list()

for line in fhand.readlines():
    line = line.strip()
    NAMES.append(line)
fhand.close()

fhand = open('populate_examinee.sql','w')
DAY = range(1,29)
MONTH = range(1,13)
YEAR = [2003,2004]
LOCATION = ['BUET','RUET','CUET','SUST']
HSC_ROLL_pool = range(1234567,9999999)
HSC_REG_pool = range(123456789, 400000000)

HSC_ROLL = list()
HSC_REG = list()

for i in range(40000):
    HSC_ROLL.append(random.choice(HSC_ROLL_pool))
    HSC_REG.append(random.choice(HSC_REG_pool))

HSC_ROLL = list(set(HSC_ROLL))
HSC_REG = list(set(HSC_REG))


for i in range(7000):
    birthday = str(random.choice(YEAR))+'/'+str(random.choice(MONTH))+'/'+str(random.choice(DAY))
    quota_status ='\'Y\'' if 'Chakma' in NAMES[i] or 'Marma' in NAMES[i] else '\'N\''
    center_id = random.choice(LOCATION)
    center_id = 'KUET'
    querystr = 'INSERT INTO EXAMINEE(EXAMINEE_ID,HSC_ROLL,HSC_REG,NAME,BIRTHDATE,QUOTA_STATUS,CENTER_ID) VALUES(new_sequence.NEXTVAL,'+ str(HSC_ROLL[i])+','+ str(HSC_REG[i])+',\''+NAMES[i].strip()+'\',\''+birthday+'\','+quota_status+',\''+center_id+'\');\n'
    fhand.write(querystr)
    querystr = 'UPDATE EXAM_CENTER SET FILLED = (SELECT FILLED FROM EXAM_CENTER WHERE CENTER_ID=\''+ center_id +'\' ) + 1 WHERE CENTER_ID=\''+center_id+'\';\n' 
    fhand.write(querystr)

for i in range(7001,len(NAMES)):
    birthday = str(random.choice(YEAR))+'/'+str(random.choice(MONTH))+'/'+str(random.choice(DAY))
    quota_status ='\'Y\'' if 'Chakma' in NAMES[i] or 'Marma' in NAMES[i] else '\'N\''
    center_id = random.choice(LOCATION)
    
    querystr = 'INSERT INTO EXAMINEE(EXAMINEE_ID,HSC_ROLL,HSC_REG,NAME,BIRTHDATE,QUOTA_STATUS,CENTER_ID) VALUES(new_sequence.NEXTVAL,'+ str(HSC_ROLL[i])+','+ str(HSC_REG[i])+',\''+NAMES[i].strip()+'\',\''+birthday+'\','+quota_status+',\''+center_id+'\');\n'
    fhand.write(querystr)
    querystr = 'UPDATE EXAM_CENTER SET FILLED = (SELECT FILLED FROM EXAM_CENTER WHERE CENTER_ID=\''+ center_id +'\' ) + 1 WHERE CENTER_ID=\''+center_id+'\';\n' 
    fhand.write(querystr)
