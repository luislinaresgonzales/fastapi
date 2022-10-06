#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#fastapi
from fastapi import FastAPI, Query
from fastapi import Body, Query

app = FastAPI()

#Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"hello" : "work"}

#request and response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person    


# validaciones query param

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: str = Query(...)
):   
    return {name: age}