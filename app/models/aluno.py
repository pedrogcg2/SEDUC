from app import db
from sqlalchemy import Column, Integer, String, Date, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

class Aluno(db.Model):
    __tablename__ = 'aluno'
    
    matricula = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    data_mat = Column(Date, nullable=False)
    turno = Column(String(10), nullable=False)
    serie = Column(SmallInteger, nullable=False)
    id_escola = Column(String(20), ForeignKey('escola.id_escola'), nullable=False)
    
    # Relationships
    escola = relationship('Escola', back_populates='alunos')
    matriculas = relationship('Matricula', back_populates='aluno')
    
    def to_dict(self):
        return {
            'matricula': self.matricula,
            'nome': self.nome,
            'data_mat': self.data_mat.isoformat() if self.data_mat else None,
            'turno': self.turno,
            'serie': self.serie,
            'id_escola': self.id_escola
        } 