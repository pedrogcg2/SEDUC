from typing import List
from repositories.base_repository import BaseRepository
from models.disciplina import Disciplina

class DisciplinaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Disciplina)
    
    def search_by_name(self, nome: str) -> List[Disciplina]:
        return Disciplina.query.filter(Disciplina.nome.ilike(f'%{nome}%')).all() 