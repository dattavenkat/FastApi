from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from urllib.parse import quote_plus

password = quote_plus("Ldvk@1501")

#SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{password}@127.0.0.1:3306/todosapplicationdatabase"

SQLALCHEMY_DATABASE_URL = 'sqlite:///todos.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)


Base = declarative_base()