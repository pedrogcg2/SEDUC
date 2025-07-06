from typing import List
from repositories.base_repository import BaseRepository
from models.aluno import Aluno

class AlunoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Aluno)
    
    def get_by_escola(self, id_escola: int) -> List[Aluno]:
        return Aluno.query.filter_by(id_escola=id_escola).all()
    
    def get_by_serie(self, serie: int) -> List[Aluno]:
        return Aluno.query.filter_by(serie=serie).all()
    
    def get_by_turno(self, turno: str) -> List[Aluno]:
        return Aluno.query.filter_by(turno=turno).all()
    
    def search_by_name(self, nome: str) -> List[Aluno]:
        return Aluno.query.filter(Aluno.nome.ilike(f'%{nome}%')).all() 