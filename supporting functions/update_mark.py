import random

fhand = open('update_marks.sql','w')
mark_ranges = range(40,260,20)
print(mark_ranges)

offsets = range(-10,11)

#for i in range(111111,111893):
for i in range(111111,143110):
    mark_range = random.choice(mark_ranges)
    phy = str(mark_range + random.choice(offsets))
    chm = str(mark_range + random.choice(offsets))
    math = str(mark_range + random.choice(offsets))
    query_str = 'UPDATE EXAMINEE SET PHY_MARK= '+ phy +', MATH_MARK= '+ math +', CHM_MARK= '+ chm +' WHERE EXAMINEE_ID = '+ str(i) +'\n'
    fhand.write(query_str)