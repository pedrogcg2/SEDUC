from typing import List
from repositories.base_repository import BaseRepository
from models.escola import Escola

class EscolaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Escola)
    
    def get_by_cidade(self, cidade: str) -> List[Escola]:
        return Escola.query.filter_by(cidade=cidade).all()
    
    def search_by_name(self, nome: str) -> List[Escola]:
        return Escola.query.filter(Escola.nome.ilike(f'%{nome}%')).all() 