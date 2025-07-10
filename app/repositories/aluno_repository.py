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
    
    def get_paginated(self, page: int, per_page: int, search: str = '', 
                     escola_id: int = None, serie: int = None, turno: str = None) -> tuple:
        """Get paginated students with optional filters"""
        query = Aluno.query
        
        if search:
            query = query.filter(Aluno.nome.ilike(f'%{search}%'))
        
        if escola_id:
            query = query.filter(Aluno.id_escola == escola_id)
        
        if serie:
            query = query.filter(Aluno.serie == serie)
        
        if turno:
            query = query.filter(Aluno.turno == turno)
        
        total = query.count()
        total_pages = (total + per_page - 1) // per_page
        
        alunos = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return alunos, total, total_pages 