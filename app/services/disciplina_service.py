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
        required_fields = ['nome']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo obrigatório '{field}' não fornecido")
        
        disciplina = self.repository.create(data)
        return disciplina.to_dict()
    
    def update_disciplina(self, id_disciplina: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Validate required fields
        required_fields = ['nome']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo obrigatório '{field}' não fornecido")
        
        disciplina = self.repository.update(id_disciplina, data)
        return disciplina.to_dict() if disciplina else None
    
    def delete_disciplina(self, id_disciplina: int) -> bool:
        return self.repository.delete(id_disciplina)
    
    def search_disciplinas_by_name(self, nome: str) -> List[Dict[str, Any]]:
        disciplinas = self.repository.search_by_name(nome)
        return [disciplina.to_dict() for disciplina in disciplinas]
    
    def get_disciplinas_paginated(self, page: int, per_page: int, search: str = '') -> tuple:
        """Get disciplines with pagination and search"""
        disciplinas, total, total_pages = self.repository.get_paginated(page, per_page, search)
        return [disciplina.to_dict() for disciplina in disciplinas], total, total_pages 