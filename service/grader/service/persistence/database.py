from sqlalchemy import create_engine

def get_all(table):
    engine = create_engine('sqlite:///grader.db', echo=True)
    select = 'SELECT * FROM %s;' % table
    result = engine.execute(select)
    return result
