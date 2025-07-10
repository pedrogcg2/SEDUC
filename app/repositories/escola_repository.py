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
    
    def get_paginated(self, page: int, per_page: int, search: str = '', 
                     cidade: str = None) -> tuple:
        """Get paginated schools with optional filters"""
        query = Escola.query
        
        if search:
            query = query.filter(
                (Escola.nome.ilike(f'%{search}%')) |
                (Escola.cidade.ilike(f'%{search}%'))
            )
        
        if cidade:
            query = query.filter(Escola.cidade == cidade)
        
        total = query.count()
        total_pages = (total + per_page - 1) // per_page
        
        escolas = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return escolas, total, total_pages 