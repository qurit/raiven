import os

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from typing import List

from api import session
from api.schemas import destination
from api.models.destination import Destination


router = APIRouter()


@router.get("/", response_model=List[destination.Destination])
def get_all_destinations(db: Session = Depends(session)):
    return db.query(Destination).all()


@router.post("/")
def create_destination(host: str, port: int, db: Session = Depends(session)):
    destination = Destination(host=host, port=port, full_name=host + str(port))
    destination.save(db)
    return destination
