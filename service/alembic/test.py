from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
engine = create_engine(DataBaseManager.get_database_url(), echo=True)
engine.execute('INSERT INTO "user" ("name") VALUES ("user1")')
engine.execute('INSERT INTO "user" ("name") VALUES ("user2")')
engine.execute('INSERT INTO "user" ("name") VALUES ("user3")')
engine.execute('INSERT INTO "user" ("name") VALUES ("user4")')
engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture1","WS21","AU.294",false)')
engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture2","WS20","AU.297",true)')
engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture3","SS22","AU.212",false)')
engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture4","SS21","AU.194",false)')
engine.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user1",1,"student")')
engine.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user1",2,"student")')
engine.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user2",1,"student")')
engine.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user2",2,"student")')

engine.execute('INSERT INTO "assignment" ("name","lectid","duedate","path","points") VALUES ("assign1",1,"2021-06-06","home/ins/",20)')
engine.execute('INSERT INTO "assignment" ("name","lectid","duedate","path","points") VALUES ("assign2",1,"2021-07-07","home/ssa/",10)')

engine.execute('INSERT INTO "submission" ("date","assignid","username") VALUES ("2021-05-05",1,"user1")')
engine.execute('INSERT INTO "submission" ("date","assignid","username") VALUES ("2021-05-07",1,"user1")')

engine.execute('INSERT INTO "file" ("name","assignid","path","exercise","points") VALUES ("exercise1.nb",1,"home/assi1",true,5)')
engine.execute('INSERT INTO "file" ("name","assignid","path","exercise") VALUES ("dataset.csv",1,"home/assi1",false)')






select = engine.execute('SELECT * FROM "assignment";')
for r in select:
    print(list(r))