from app import db
from sqlalchemy import Column, Integer, SmallInteger, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Matricula(db.Model):
    __tablename__ = 'matricula'
    
    id = Column(Integer, primary_key=True)
    ano = Column(Integer, nullable=False)
    matricula_aluno = Column(Integer, ForeignKey('aluno.matricula'), nullable=False)
    id_escola = Column(Integer, ForeignKey('escola.id_escola'), nullable=False)
    id_disciplina = Column(Integer, ForeignKey('disciplina.id_disciplina'), nullable=False)
    serie = Column(SmallInteger, nullable=False)
    nota = Column(Float, nullable=False)
    status = Column(Boolean, nullable=False)
    
    # Relationships
    aluno = relationship('Aluno', back_populates='matriculas')
    escola = relationship('Escola', back_populates='matriculas')
    disciplina = relationship('Disciplina', back_populates='matriculas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ano': self.ano,
            'matricula_aluno': self.matricula_aluno,
            'id_escola': self.id_escola,
            'id_disciplina': self.id_disciplina,
            'serie': self.serie,
            'nota': self.nota,
            'status': self.status
        } 