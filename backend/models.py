from sqlalchemy import Column, Integer, String, Float
from database import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class ChangeoverTime(Base):
    __tablename__ = "changeover_times"

    id = Column(Integer, primary_key=True, index=True)
    from_part_id = Column(Integer, index=True)
    to_part_id = Column(Integer, index=True)
    time = Column(Float)