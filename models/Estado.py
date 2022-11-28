import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey,func
from sqlalchemy.orm import relationship
class Estado(db.Base):
    __tablename__ = 'estados'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    tipo = Column('tipo', String, nullable=False)
    fechaHora=Column('contrasena', String, nullable=False)
    when = Column('when', DateTime, server_default=func.now(),nullable=True)
    paquetes_id = Column('paquetes_id', Integer, ForeignKey('paquetes.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    paquetes = relationship('Paquete', back_populates='estados')
  
    def __init__(self,id,tipo,fechaHora, when, paquetes_id):
        self.id = id
        self.tipo = tipo
        self.fechaHora = fechaHora
        self.when = when
        self.paquetes_id = paquetes_id
   
    def __repr__(self):
        return f"<Estado {self.id}>"