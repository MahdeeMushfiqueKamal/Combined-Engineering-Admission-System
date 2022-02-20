from os import sep

outfile = open('populate_table.sql','w')

#populate suniversity
outfile.write('INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES(\'BUET\',\'Bangladesh University of Engineering and Technology\', \'Dhaka-1000\');\n')
outfile.write('INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES(\'CUET\',\'Chittagong University of Engineering and Technology\', \'Chittagong\');\n')
outfile.write('INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES(\'KUET\',\'Khulna University of Engineering and Technology\', \'Fulbarigate,Khulna\');\n')
outfile.write('INSERT INTO UNIVERSITY(UNI_ID,NAME,LOCATION) VALUES(\'RUET\',\'Rajshahi University of Engineering and Technology\', \'Kazla, Rajshahi-6204\');\n')

#populate subject
fhand1 = open('sub.txt')
for line in fhand1.readlines():
    line = line.split(',')

    query_str = 'INSERT INTO SUBJECT(SUB_ID,NAME) VALUES(\''+line[0]+'\',\''+line[1].strip()+'\');\n'
    outfile.write(query_str)
fhand1.close()

#populate uni-sub
i=1
fhand1 = open('uni_sub.csv')
for line in fhand1.readlines():
    line = line.split(',')

    query_str = 'INSERT INTO UNI_SUB(UNI_SUB_ID,UNI_ID,SUB_ID,CAPASITY,QUOTA_CAPASITY) VALUES( '+ str(i) +',\''+line[0]+'\',\''+line[1]+'\','+line[2]+','+line[3].strip()+');\n'
    outfile.write(query_str)
    i+=1
fhand1.close()


#populate exam-center
outfile.write('INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES(\'BUET\',\'Bangladesh University of Engineering and Technology\', \'Dhaka-1000\',8000);\n')
outfile.write('INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES(\'CUET\',\'Chittagong University of Engineering and Technology\', \'Pahartoli, Raozan-4349, Chittagong\',7000);\n')
outfile.write('INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES(\'KUET\',\'Khulna University of Engineering and Technology\', \'Fulbarigate,Khulna\',7000);\n')
outfile.write('INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES(\'RUET\',\'Rajshahi University of Engineering and Technology\', \'Kazla, Rajshahi-6204\',7000);\n')
outfile.write('INSERT INTO EXAM_CENTER(CENTER_ID,NAME,LOCATION,CAPASITY) VALUES(\'SUST\',\'Sylhet University of Science and Technology\', \'University Ave, Sylhet 3114\',7000);\n')
