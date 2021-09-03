"""test_data

Revision ID: b7dbb0f93187
Revises: a1791b1371ed
Create Date: 2021-05-18 08:19:34.321594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7dbb0f93187'
down_revision = 'a1791b1371ed'
branch_labels = None
depends_on = None


def upgrade():
    ## Users
    op.execute('INSERT INTO "user" ("name") VALUES ("user1")')
    op.execute('INSERT INTO "user" ("name") VALUES ("user2")')
    op.execute('INSERT INTO "user" ("name") VALUES ("user3")')
    op.execute('INSERT INTO "user" ("name") VALUES ("user4")')
    op.execute('INSERT INTO "user" ("name") VALUES ("fjaeger")')
    op.execute('INSERT INTO "user" ("name") VALUES ("ubuntu")')

    ## Lectures
    op.execute('INSERT INTO "lecture" ("name","semester","code", "state", "deleted") VALUES ("lecture1","WS21","21wle1","active","active")')
    op.execute('INSERT INTO "lecture" ("name","semester","code", "state", "deleted") VALUES ("lecture1","SS21","21sle1","active","active")')
    op.execute('INSERT INTO "lecture" ("name","semester","code", "state", "deleted") VALUES ("lecture2","WS20","20wle2","active","active")')
    op.execute('INSERT INTO "lecture" ("name","semester","code", "state", "deleted") VALUES ("lecture3","SS22","22sle3","active","active")')
    op.execute('INSERT INTO "lecture" ("name","semester","code", "state", "deleted") VALUES ("lecture4","SS21","21sle4","active","active")')
    op.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user1",1,"student")')
    op.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user1",2,"student")')
    op.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user2",1,"student")')
    op.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user2",2,"student")')

    op.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("fjaeger",1,"instructor")')
    op.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("ubuntu",1,"instructor")')
    op.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("fjaeger",3,"student")')
    op.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("ubuntu",3,"instructor")')

    # ## Assignments
    # op.execute('INSERT INTO "assignment" ("name","lectid","duedate","points","status", "type") VALUES ("assignment_1",1,"2021-09-21 23:59:00.000",20,"released","user")')
    # op.execute('INSERT INTO "assignment" ("name","lectid","duedate","points","status", "type") VALUES ("assignment_2",1,"2021-09-22 23:59:00.000",10,"created","user")')
    # ## Submissions
    # op.execute('INSERT INTO "submission" ("date","status","assignid","username","commit_hash") VALUES ("2021-05-05 14:43:35.863","not_graded",1,"user1", "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')
    # op.execute('INSERT INTO "submission" ("date","status","assignid","username","score","commit_hash") VALUES ("2021-05-07 14:44:35.863","manually_graded",1,"user1",10, "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')

    # op.execute('INSERT INTO "submission" ("date","status","assignid","username","commit_hash") VALUES ("2021-05-06 14:43:35.863 ","not_graded",1,"fjaeger", "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')
    # op.execute('INSERT INTO "submission" ("date","status","assignid","username","score","commit_hash") VALUES ("2021-05-08 14:44:35.863","manually_graded",1,"fjaeger",10,"e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')

    # op.execute('INSERT INTO "submission" ("date","status","assignid","username","commit_hash") VALUES ("2021-05-05 14:43:35.863","not_graded",1,"ubuntu", "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')
    # op.execute('INSERT INTO "submission" ("date","status","assignid","username","score","commit_hash") VALUES ("2021-05-07 14:44:35.863","manually_graded",1,"ubuntu",10, "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')

    # for i in range(0,100):
    #     op.execute('INSERT INTO "submission" ("date","status","assignid","username","commit_hash") VALUES ("2021-05-05 14:43:35.863","not_graded",1,"user1", "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')
    #     op.execute('INSERT INTO "submission" ("date","status","assignid","username","score","commit_hash") VALUES ("2021-05-07 14:44:35.863","manually_graded",1,"user1",10, "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')

    #     op.execute('INSERT INTO "submission" ("date","status","assignid","username","commit_hash") VALUES ("2021-05-06 14:43:35.863","not_graded",1,"fjaeger", "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')
    #     op.execute('INSERT INTO "submission" ("date","status","assignid","username","score","commit_hash") VALUES ("2021-05-08 14:44:35.863","manually_graded",1,"fjaeger",10, "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')

    #     op.execute('INSERT INTO "submission" ("date","status","assignid","username","commit_hash") VALUES ("2021-05-05 14:43:35.863","not_graded",1,"ubuntu", "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')
    #     op.execute('INSERT INTO "submission" ("date","status","assignid","username","score","commit_hash") VALUES ("2021-05-07 14:44:35.863","manually_graded",1,"ubuntu",10, "e93ae2b2369cb0ddb647f1c608148ccda59e22a1")')   
    

def downgrade():
    pass
