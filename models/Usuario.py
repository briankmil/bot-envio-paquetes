import database.db as db
from sqlalchemy import Column, Integer, String, Float,DateTime,ForeignKey,func
from sqlalchemy.orm import relationship

class Usuario(db.Base):
    __tablename__ = 'usuarios'
    id = Column('id', String(15), primary_key=True, nullable=False)
    tipo = Column('tipo', String, nullable=False)
    contrasena=Column('contrasena', String, nullable=False)
    nombre=Column('nombre', String, nullable=False)
    estados = relationship('Estado', back_populates='usuarios')

  
    def __init__(self,id,tipo,contrasena,nombre):
        self.id = id
        self.tipo = tipo
        self.contrasena = contrasena
        self.nombre = nombre
     
    
    def __repr__(self):
        return f"<Usuario id: {self.id}, tipo: {self.tipo}, contraseña: {self.contrasena}, nombre: {self.nombre}>"