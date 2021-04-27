from sqlalchemy import create_engine
engine = create_engine('sqlite:///grader.db', echo=True)
engine.execute('INSERT INTO "user" ("name","token") VALUES ("user1","dasdada23234ddfdfdsf")')
engine.execute('INSERT INTO "user" ("name","token") VALUES ("user2","dasdada23234ddfdfdsf")')
engine.execute('INSERT INTO "user" ("name","token") VALUES ("user3","dasdada23234ddfdfdsf")')
engine.execute('INSERT INTO "user" ("name","token") VALUES ("user4","dasdada23234ddfdfdsf")')
engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture1","WS21","AU.294",false)')
engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture2","WS20","AU.297",true)')
engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture3","SS22","AU.212",false)')
engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture4","SS21","AU.194",false)')
engine.execute('INSERT INTO "takepart" ("userid","lectid","role") VALUES (1,1,"student")')
engine.execute('INSERT INTO "takepart" ("userid","lectid","role") VALUES (1,2,"student")')
engine.execute('INSERT INTO "takepart" ("userid","lectid","role") VALUES (2,1,"student")')
engine.execute('INSERT INTO "takepart" ("userid","lectid","role") VALUES (2,2,"student")')

engine.execute('INSERT INTO "assignment" ("name","lectid","duedate","path","points") VALUES ("assign1",1,"2021-06-06","home/ins/",20)')
engine.execute('INSERT INTO "assignment" ("name","lectid","duedate","path","points") VALUES ("assign2",1,"2021-07-07","home/ssa/",10)')

engine.execute('INSERT INTO "submission" ("date","assignid","userid") VALUES ("2021-05-05",1,1)')
engine.execute('INSERT INTO "submission" ("date","assignid","userid") VALUES ("2021-05-07",1,1)')

engine.execute('INSERT INTO "file" ("name","assignid","path","exercise","points") VALUES ("exercise1.nb",1,"home/assi1",true,5)')
engine.execute('INSERT INTO "file" ("name","assignid","path","exercise") VALUES ("dataset.csv",1,"home/assi1",false)')






select = engine.execute('SELECT * FROM "assignment";')
for r in select:
    print(list(r))