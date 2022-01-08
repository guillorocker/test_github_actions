from typing import List
from fastapi import FastAPI,HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.sql.functions import mode
from starlette.responses import RedirectResponse
from . import models, schemas
from .con import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get('/',include_in_schema=False)
def main():
    return RedirectResponse(url="/docs")

#Usuarios ABM

@app.get("/usuarios/",response_model=List[schemas.User])
def show_users(db: Session=Depends(get_db)):
    usuarios = db.query(models.User).all()
    return usuarios

@app.post('/usuarios/',response_model=schemas.User)
def create_users(entrada:schemas.User,db:Session=Depends(get_db)):
    usuario = models.User(username = entrada.username, hashed_password=entrada.hashed_password,nombre=entrada.nombre,estado=entrada.estado)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.put('/usuarios/{usuario_id}',response_model=schemas.User)
def update_users(usuario_id:int,entrada:schemas.UserUpdate,db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()
    usuario.nombre = entrada.nombre if entrada.nombre else usuario.nombre
    usuario.rol = entrada.rol if entrada.rol else usuario.rol
    usuario.estado = entrada.estado if entrada.estado else usuario.estado
    db.commit()
    db.refresh(usuario)
    return usuario

@app.delete('/usuarios/{usuario_id}',response_model=schemas.Respuesta)
def delete_users(usuario_id:int,db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()
    db.delete(usuario)
    db.commit()
    respuesta = schemas.Respuesta(mensaje='Eliminado exitosamente')
    return respuesta


# Cursos ABM

#ver cursos
@app.get("/Course/",response_model=List[schemas.CoursesBase])
def show_all_courses(db: Session=Depends(get_db)):
    cursos = db.query(models.Cursos).all()
    return cursos

@app.get("/Course/{course_id}",response_model=schemas.Course)
def show_course(course_id,db: Session=Depends(get_db)):
    curso = db.query(models.Cursos).filter(models.Cursos.id == course_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso not found")
    return curso

#crear cursos
@app.post('/Course/',response_model=schemas.CreateCourse)
def create_course(entrada:schemas.CreateCourse,db:Session=Depends(get_db)):
    curso = models.Cursos(nombre = entrada.nombre, descripcion= entrada.descripcion,estado=entrada.estado)
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso

# @app.put('/Courses/{usuario_id}',response_model=schemas.User)
# def update_users(usuario_id:int,entrada:schemas.UserUpdate,db:Session=Depends(get_db)):
#     usuario = db.query(models.User).filter_by(id=usuario_id).first()
#     usuario.nombre = entrada.nombre
#     db.commit()
#     db.refresh(usuario)
#     return usuario

# @app.delete('/Courses/{usuario_id}',response_model=schemas.Respuesta)
# def delete_users(usuario_id:int,db:Session=Depends(get_db)):
#     usuario = db.query(models.User).filter_by(id=usuario_id).first()
#     db.delete(usuario)
#     db.commit()
#     respuesta = schemas.Respuesta(mensaje='Eliminado exitosamente')
#     return respuesta


