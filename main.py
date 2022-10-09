#Python
from typing import Optional
from enum import Enum

#Pydantic ❯ uvicorn main:app --reload 
from pydantic import BaseModel
from pydantic import Field

#fastapi
from fastapi import FastAPI, Path, Query
from fastapi import Body, Query, Path

app = FastAPI()

#Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blone = "blone"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Luis"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Linares"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example="31"
    )
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)
    password: str = Field(..., min_length=8)

class PersonOut(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Luis"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Linares"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example="31"
    )
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)

    # class Config:
    #     schema_extra = {
    #         "example" : {
    #             "first_name": "Luis",
    #             "last_name": "Linares",
    #             "age": "31",
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }

@app.get("/")
def home():
    return {"hello" : "work"}

#request and response body

@app.post("/person/new", response_model=PersonOut)
def create_person(person: Person = Body(...)):
    return person    


# validaciones query param

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocio"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age, It's required",
        example="25"
        )
):   
    return {name: age}

#validation path param
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123
        )
):
    return {person_id: "It exists!!"}   

#validacions request body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict
    results.update(location.dict())
    return results  
    