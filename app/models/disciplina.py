from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Disciplina(db.Model):
    __tablename__ = 'disciplina'
    
    id_disciplina = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    
    # Relationships
    matriculas = relationship('Matricula', back_populates='disciplina')
    
    def to_dict(self):
        return {
            'id_disciplina': self.id_disciplina,
            'nome': self.nome
        } 