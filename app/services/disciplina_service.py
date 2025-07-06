from typing import List, Optional, Dict, Any
from repositories.disciplina_repository import DisciplinaRepository

class DisciplinaService:
    def __init__(self):
        self.repository = DisciplinaRepository()
    
    def get_all_disciplinas(self) -> List[Dict[str, Any]]:
        disciplinas = self.repository.get_all()
        return [disciplina.to_dict() for disciplina in disciplinas]
    
    def get_disciplina_by_id(self, id_disciplina: int) -> Optional[Dict[str, Any]]:
        disciplina = self.repository.get_by_id(id_disciplina)
        return disciplina.to_dict() if disciplina else None
    
    def create_disciplina(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Validate required fields
        if 'nome' not in data:
            raise ValueError("Campo obrigatório 'nome' não fornecido")
        
        disciplina = self.repository.create(data)
        return disciplina.to_dict() 