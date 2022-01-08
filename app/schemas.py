#implementa un modelo base que nos permite definir el formato de respuesta y el cuerpo de objeto de entrada, cuando se realiza un create o update.
from typing import Optional, List
from pydantic import BaseModel


class CoursesBase(BaseModel):
    id:int
    nombre:str
    descripcion:str
    estado:int

    class Config:
        orm_mode = True

class Course(CoursesBase):  
    integrantes: Optional[List]

    class Config:
        orm_mode = True

class CreateCourse(BaseModel):
    nombre:str
    descripcion:str
    estado:int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str

class User(UserBase):
    id: int
    nombre: str
    hashed_password: str
    estado:int
    rol: str
    cursos: Optional[List]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    nombre: Optional[str]
    rol: Optional[str]
    estado: Optional[int]

    class Config:
        orm_mode = True
    


class Respuesta(BaseModel):
    mensaje: str





class RegistroCursos(BaseModel):

    id = int
    curso_id = int
    estudiante_id = int

    class Config:
        orm_mode = True