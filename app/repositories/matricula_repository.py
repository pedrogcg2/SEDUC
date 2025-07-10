from typing import List
from repositories.base_repository import BaseRepository
from models.matricula import Matricula

class MatriculaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Matricula)
    
    def get_by_aluno(self, matricula_aluno: int) -> List[Matricula]:
        return Matricula.query.filter_by(matricula_aluno=matricula_aluno).all()
    
    def get_by_escola(self, id_escola: int) -> List[Matricula]:
        return Matricula.query.filter_by(id_escola=id_escola).all()
    
    def get_by_disciplina(self, id_disciplina: int) -> List[Matricula]:
        return Matricula.query.filter_by(id_disciplina=id_disciplina).all()
    
    def get_by_ano(self, ano: int) -> List[Matricula]:
        return Matricula.query.filter_by(ano=ano).all()
    
    def get_by_serie(self, serie: int) -> List[Matricula]:
        return Matricula.query.filter_by(serie=serie).all()
    
    def get_by_status(self, status: bool) -> List[Matricula]:
        return Matricula.query.filter_by(status=status).all()
    
    def get_aluno_performance(self, matricula_aluno: int, ano: int = None) -> List[Matricula]:
        query = Matricula.query.filter_by(matricula_aluno=matricula_aluno)
        if ano:
            query = query.filter_by(ano=ano)
        return query.all() 
    
    def get_paginated(self, page: int, per_page: int, search: str = '') -> tuple:
        """Get paginated enrollments with search"""
        query = Matricula.query
        
        # Apply search filter (search in related data)
        if search:
            # Join with related tables for search
            from models.aluno import Aluno
            from models.escola import Escola
            from models.disciplina import Disciplina
            from app import db
            
            query = query.join(Aluno, Matricula.matricula_aluno == Aluno.matricula)\
                        .join(Escola, Matricula.id_escola == Escola.id_escola)\
                        .join(Disciplina, Matricula.id_disciplina == Disciplina.id_disciplina)\
                        .filter(
                            db.or_(
                                Aluno.nome.ilike(f'%{search}%'),
                                Escola.nome.ilike(f'%{search}%'),
                                Disciplina.nome.ilike(f'%{search}%')
                            )
                        )
        
        total = query.count()
        total_pages = (total + per_page - 1) // per_page
        
        matriculas = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return matriculas, total, total_pages 