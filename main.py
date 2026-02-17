from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep
app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    # Check if the ID exists BEFORE trying to access it
    if id not in db.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sheep not found")

    return db.get_sheep(id)

@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    # Check if the sheep ID already exists to avoid duplication
    if sheep.id in db.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sheep with this ID already exists")

    # Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep # Return the newly added sheep data

@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    # Check if the ID exists in the db
    if id not in db.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sheep with this ID does not exist")

    # Delete sheep with ID from db
    db.delete_sheep(id)