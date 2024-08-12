from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relationship definitions
    changeover_times_from = relationship("ChangeoverTime", foreign_keys="ChangeoverTime.from_part_id", back_populates="from_part")
    changeover_times_to = relationship("ChangeoverTime", foreign_keys="ChangeoverTime.to_part_id", back_populates="to_part")

class ChangeoverTime(Base):
    __tablename__ = "changeover_times"

    id = Column(Integer, primary_key=True, index=True)
    from_part_id = Column(Integer, ForeignKey('parts.id'), index=True)
    to_part_id = Column(Integer, ForeignKey('parts.id'), index=True)
    time = Column(Float)

    # Relationship definitions
    from_part = relationship("Part", foreign_keys=[from_part_id],  back_populates="changeover_times_from")
    to_part = relationship("Part", foreign_keys=[to_part_id],  back_populates="changeover_times_to")