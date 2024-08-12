from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.responses import FileResponse
import pandas as pd
import tempfile
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/parts/", response_model=schemas.Part)
def create_part(part: schemas.PartCreate, db: Session = Depends(get_db)):
    return crud.create_part(db=db, part=part)

@app.get("/parts/", response_model=List[schemas.Part])
def read_parts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_parts(db, skip=skip, limit=limit)

@app.post("/changeover-times/", response_model=schemas.ChangeoverTime)
def create_changeover_time(changeover_time: schemas.ChangeoverTimeCreate, db: Session = Depends(get_db)):
    return crud.create_changeover_time(db=db, changeover_time=changeover_time)

@app.get("/changeover-times/", response_model=List[schemas.ChangeoverTime])
def read_changeover_times(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_changeover_times(db, skip=skip, limit=limit)

@app.post("/import-excel/")
async def import_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(400, detail="Invalid file format. Please upload an Excel file.")
    
    df = pd.read_excel(file.file)
    for _, row in df.iterrows():
        part = schemas.PartCreate(name=row['Part Name'])
        crud.create_part(db, part)
    
    return {"message": "Data imported successfully"}

@app.get("/export-excel/")
async def export_excel(db: Session = Depends(get_db)):
    parts = crud.get_parts(db)
    changeover_times = crud.get_changeover_times(db)
    
    df_parts = pd.DataFrame([{"Part Name": part.name} for part in parts])
    df_changeover = pd.DataFrame([{
        "From Part": ct.from_part_id,
        "To Part": ct.to_part_id,
        "Time": ct.time
    } for ct in changeover_times])
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        with pd.ExcelWriter(tmp.name) as writer:
            df_parts.to_excel(writer, sheet_name='Parts', index=False)
            df_changeover.to_excel(writer, sheet_name='Changeover Times', index=False)
    
    return FileResponse(tmp.name, filename="parts_changeover_data.xlsx")