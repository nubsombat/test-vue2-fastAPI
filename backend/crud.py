from sqlalchemy.orm import Session
import models, schemas

def get_part(db: Session, part_id: int):
    return db.query(models.Part).filter(models.Part.id == part_id).first()

def get_parts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Part).offset(skip).limit(limit).all()

def create_part(db: Session, part: schemas.PartCreate):
    db_part = models.Part(name=part.name)
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

def get_changeover_times(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ChangeoverTime).offset(skip).limit(limit).all()

def create_changeover_time(db: Session, changeover_time: schemas.ChangeoverTimeCreate):
    db_changeover_time = models.ChangeoverTime(**changeover_time.dict())
    db.add(db_changeover_time)
    db.commit()
    db.refresh(db_changeover_time)
    return db_changeover_time