from typing import Collection
from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import interfaces
from sqlalchemy.orm import relation, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql.elements import collate
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.selectable import FromClause
from sqlalchemy.sql.traversals import COMPARE_FAILED
from .con import Base


association_table = Table('association', Base.metadata,
    Column('usuarios', ForeignKey('usuarios.id'), primary_key=True),
    Column('cursos', ForeignKey('cursos.id'), primary_key=True))


class User(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20))
    hashed_password = Column(String(100))
    nombre = Column(String(200))
    rol = Column(String(20))
    estado = Column(Integer)    
    cursos = relationship("Cursos", secondary=association_table, back_populates="integrantes")

    def __init__(self) -> None:
        super().__init__()

class Cursos(Base):
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    descripcion = Column(String(200))
    estado = Column(Integer)
    integrantes = relationship("User", secondary=association_table,back_populates="cursos",collection_class=attribute_mapped_collection('nombre'))


class Token(Base):
    __tablename__ = 'tokenusuario'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(200))
    user_id = Column(Integer, ForeignKey("usuarios.id"))

class Client(Base):
    __tablename__ = 'client_id'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50))
    client_secret = Column(String(50))
    exp = Column(Integer)


