from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Escola(db.Model):
    __tablename__ = 'escola'
    
    id_escola = Column(String(20), primary_key=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(100), nullable=False)
    cidade = Column(String(50), nullable=False)
    
    # Relationships
    alunos = relationship('Aluno', back_populates='escola')
    matriculas = relationship('Matricula', back_populates='escola')
    
    def to_dict(self):
        return {
            'id_escola': self.id_escola,
            'nome': self.nome,
            'endereco': self.endereco,
            'cidade': self.cidade
        } 