import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey,func
from sqlalchemy.orm import relationship
class Estado(db.Base):
    __tablename__ = 'estados'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    tipo = Column('tipo', String, nullable=False)
    fechaHora=Column('contrasena', String, nullable=False)
    when = Column('when', DateTime, server_default=func.now(),nullable=True)
    usuarios_id = Column('usuarios_id', String(15), ForeignKey('usuarios.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    usuarios = relationship('Usuario', back_populates='estados')
    paquetes = relationship('Paquete', back_populates='estados')
  
    def __init__(self,tipo,fechaHora, usuarios_id):
        self.tipo = tipo
        self.fechaHora = fechaHora
        self.usuarios_id = usuarios_id

    def __repr__(self):
        return f"{self.id}"

