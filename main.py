from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from exceptions import NoteNotFoundError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import models, schemas
from database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/echo")
def echo(message: str = "hello"):
    return {"echo": message}


@app.post("/notes", response_model=schemas.NoteResponse, status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.NoteModel(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.get("/notes", response_model=list[schemas.NoteResponse])
def list_notes(db: Session = Depends(get_db)):
    return db.query(models.NoteModel).all()


@app.get("/notes/{note_id}", response_model=schemas.NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.NoteModel).filter(models.NoteModel.id == note_id).first()
    if not note:
        raise NoteNotFoundError(note_id)
    return note


@app.get("/crash-test")
def crash_test():
    return 1/0


@app.put("/notes/{note_id}", response_model=schemas.NoteResponse)
def update_note(
    note_id: int, updated: schemas.NoteCreate, db: Session = Depends(get_db)
):
    note = db.query(models.NoteModel).filter(models.NoteModel.id == note_id).first()
    if not note:
        raise NoteNotFoundError(note_id)
    note.title = updated.title
    note.content = updated.content
    db.commit()
    db.refresh(note)
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.NoteModel).filter(models.NoteModel.id == note_id).first()
    if not note:
        raise NoteNotFoundError(note_id)
    db.delete(note)
    db.commit()


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "Something went wrong on our end",
        },
    )
