from sqlalchemy import create_engine
engine = create_engine('sqlite:///grader.db', echo=True)
engine.execute('INSERT INTO "user" ("name","token") VALUES ("user1","dasdada23234ddfdfdsf")')
engine.execute('INSERT INTO "user" ("name","token") VALUES ("user2","dasdada23234ddfdfdsf")')
engine.execute('INSERT INTO "user" ("name","token") VALUES ("user3","dasdada23234ddfdfdsf")')
engine.execute('INSERT INTO "user" ("name","token") VALUES ("user4","dasdada23234ddfdfdsf")')

select = engine.execute('SELECT * FROM "user";')
for r in select:
    print(r)