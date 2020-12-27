from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from pathlib import Path
import os

app_dir = Path(__file__).parent.parent.parent

engine = create_engine('sqlite:///' + os.path.join(app_dir, 'app.db'), convert_unicode=True)
metadata = MetaData()

"""
Créer une session d'accès à la base de données
"""
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def init_db():
    """
    Initialise la base de données.
    """
    metadata.create_all(bind=engine)