import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey,func
from sqlalchemy.orm import relationship
class Paquete(db.Base):
    __tablename__ = 'paquetes'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    when = Column('when', DateTime, server_default=func.now(),nullable=True)
    estados_id = Column('estados_id', Integer , ForeignKey('estados.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    estados = relationship('Estado', back_populates='paquetes')
    usuarios_id = Column('usuarios_id', Integer, ForeignKey('usuarios.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    fechaActual=Column('fechaActual', DateTime, server_default=func.now(),nullable=True)
    nombreRemitente=Column('nombreRemitente', String, nullable=False)
    peso=Column('nombreRemitente', Float, nullable=False)
    direccionDestino=Column('direccionDestino', String, nullable=False)
    
    def __init__(self,id, when,estados_id,usuarios_id,fechaActual,nombreRemitente,peso,direccionDestino):
        self.id = id
        self.when = when
        self.estados_id = estados_id
        self.usuarios_id = usuarios_id
        self.fechaActual = fechaActual
        self.nombreRemitente = nombreRemitente
        self.peso = peso
        self.direccionDestino = direccionDestino
        
    
    def __repr__(self):
        return f"<Paquete {self.id}>"