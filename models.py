import atexit

from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DSN = 'postgresql://postgres:postgres@localhost:5432/flask_db'
engine = create_engine(DSN)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Ad(Base):
    __tablename__ = "Ad"

    id = Column(Integer, primary_key=True)
    header = Column(String, nullable=False)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)

Base.metadata.create_all()
