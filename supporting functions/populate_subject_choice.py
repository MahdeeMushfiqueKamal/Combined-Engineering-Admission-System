import random
outfile = open('3.choice_list.sql','w')

choiceList = list()
for i in range(1,55):
    choiceList.append(i)

for i in range(2,5001):
    random.shuffle(choiceList)
    for j in range(1,11):
        query_str = 'INSERT INTO CHOICE_LIST(MERIT_POS,PRIORITY_NO,UNI_SUB_ID) VALUES ('+str(i) +',' +str(j)+ ',' + str(choiceList[j]) + ');\n'
        #print(query_str)
        outfile.write(query_str)

for i in range(1,5001):
    query_str = '''UPDATE MERIT_LIST SET ADMISSION_STATUS = 'Y' WHERE MERIT_POS = '''+str(i) + ';\n'
    outfile.write(query_str)