from typing import List
from repositories.base_repository import BaseRepository
from models.disciplina import Disciplina

class DisciplinaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Disciplina)
    
    def search_by_name(self, nome: str) -> List[Disciplina]:
        return Disciplina.query.filter(Disciplina.nome.ilike(f'%{nome}%')).all()
    
    def get_paginated(self, page: int, per_page: int, search: str = '') -> tuple:
        """Get paginated disciplines with optional search"""
        query = Disciplina.query
        
        if search:
            query = query.filter(Disciplina.nome.ilike(f'%{search}%'))
        
        total = query.count()
        total_pages = (total + per_page - 1) // per_page
        
        disciplinas = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return disciplinas, total, total_pages 