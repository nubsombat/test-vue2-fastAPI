from sqlalchemy.orm import Session, aliased
import models, schemas

PartAliasFrom = aliased(models.Part, name='part_from')
PartAliasTo = aliased(models.Part, name='part_to')

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
    results = (
        db.query(models.ChangeoverTime, PartAliasFrom.name.label('from_part_name'), PartAliasTo.name.label('to_part_name'))
        .join(PartAliasFrom, models.ChangeoverTime.from_part_id == PartAliasFrom.id, isouter=True)
        .join(PartAliasTo, models.ChangeoverTime.to_part_id == PartAliasTo.id, isouter=True)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": item[0].id,
            "from_part_id": item[0].from_part_id,
            "to_part_id": item[0].to_part_id,
            "time": item[0].time,
            "from_part_name": item[1],
            "to_part_name": item[2]
        }
        for item in results
    ]
    

def create_changeover_time(db: Session, changeover_time: schemas.ChangeoverTimeCreate):
    db_changeover_time = models.ChangeoverTime(**changeover_time.dict())
    db.add(db_changeover_time)
    db.commit()
    db.refresh(db_changeover_time)
    return db_changeover_time

