from sqlalchemy import create_engine
engine = create_engine('sqlite:///grader.db', echo=True)
# engine.execute('INSERT INTO "user" ("name","token") VALUES ("user1","dasdada23234ddfdfdsf")')
# engine.execute('INSERT INTO "user" ("name","token") VALUES ("user2","dasdada23234ddfdfdsf")')
# engine.execute('INSERT INTO "user" ("name","token") VALUES ("user3","dasdada23234ddfdfdsf")')
# engine.execute('INSERT INTO "user" ("name","token") VALUES ("user4","dasdada23234ddfdfdsf")')
# engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture1","WS21","AU.294",false)')
# engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture2","WS20","AU.297",true)')
# engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture3","SS22","AU.212",false)')
# engine.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture4","SS21","AU.194",false)')

select = engine.execute('SELECT * FROM "user";')
for r in select:
    print(r)