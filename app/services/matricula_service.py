from typing import List, Optional, Dict, Any
from repositories.matricula_repository import MatriculaRepository

class MatriculaService:
    def __init__(self):
        self.repository = MatriculaRepository()
    
    def get_all_matriculas(self) -> List[Dict[str, Any]]:
        matriculas = self.repository.get_all()
        return [matricula.to_dict() for matricula in matriculas]
    
    def get_matricula_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        matricula = self.repository.get_by_id(id)
        return matricula.to_dict() if matricula else None
    
    def create_matricula(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Validate required fields
        required_fields = ['ano', 'matricula_aluno', 'id_escola', 'id_disciplina', 'serie', 'nota', 'status']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo obrigatório '{field}' não fornecido")
        
        # Validate nota range
        if not (0 <= data['nota'] <= 10):
            raise ValueError("Nota deve estar entre 0 e 10")
        
        matricula = self.repository.create(data)
        return matricula.to_dict()
    
    def get_matriculas_by_aluno(self, matricula_aluno: int) -> List[Dict[str, Any]]:
        matriculas = self.repository.get_by_aluno(matricula_aluno)
        return [matricula.to_dict() for matricula in matriculas]
    
    def get_aluno_performance(self, matricula_aluno: int, ano: int = None) -> List[Dict[str, Any]]:
        matriculas = self.repository.get_aluno_performance(matricula_aluno, ano)
        return [matricula.to_dict() for matricula in matriculas]
    
    def get_average_grade_by_disciplina(self, id_disciplina: int) -> float:
        matriculas = self.repository.get_by_disciplina(id_disciplina)
        if not matriculas:
            return 0.0
        return sum(m.nota for m in matriculas) / len(matriculas) 