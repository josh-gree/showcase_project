from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ResponseTime(Base):
    """
    Represent a record of an endpoints response time
    """

    __tablename__ = "responsetimes"
    id = Column(Integer, primary_key=True)
    route = Column(String)
    time = Column(Integer)
