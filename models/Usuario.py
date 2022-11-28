import database.db as db
from sqlalchemy import Column, Integer, String, Float,DateTime,ForeignKey,func
from sqlalchemy.orm import relationship

class Usuario(db.Base):
    __tablename__ = 'usuarios'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    tipo = Column('tipo', String, nullable=False)
    contrasena=Column('contrasena', String, nullable=False)
    nombre=Column('nombre', String, nullable=False)
    when = Column('when', DateTime, server_default=func.now(),nullable=True)
    estados = relationship('Estado', back_populates='usuarios')
    paquetes = relationship('Paquete', back_populates='usuarios')
  
    def __init__(self,id,tipo,contrasena,nombre, when):
        self.id = id
        self.tipo = tipo
        self.contrasena = contrasena
        self.nombre = nombre
        self.when = when
    
    def __repr__(self):
        return f"<Usuario {self.id}>"