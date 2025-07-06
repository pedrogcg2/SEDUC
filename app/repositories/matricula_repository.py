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