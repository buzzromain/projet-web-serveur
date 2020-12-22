from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import os

app_dir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///' + os.path.join(app_dir, 'app.db'), convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
def init_db():
    metadata.create_all(bind=engine)