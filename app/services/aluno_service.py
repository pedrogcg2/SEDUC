from typing import List, Optional, Dict, Any
from repositories.aluno_repository import AlunoRepository

class AlunoService:
    def __init__(self):
        self.repository = AlunoRepository()
    
    def get_all_alunos(self) -> List[Dict[str, Any]]:
        alunos = self.repository.get_all()
        return [aluno.to_dict() for aluno in alunos]
    
    def get_aluno_by_id(self, matricula: int) -> Optional[Dict[str, Any]]:
        aluno = self.repository.get_by_id(matricula)
        return aluno.to_dict() if aluno else None
    
    def create_aluno(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Validate required fields
        required_fields = ['nome', 'data_mat', 'turno', 'serie', 'id_escola']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo obrigatório '{field}' não fornecido")
        
        aluno = self.repository.create(data)
        return aluno.to_dict()
    
    def update_aluno(self, matricula: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Validate required fields
        required_fields = ['nome', 'data_mat', 'turno', 'serie', 'id_escola']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo obrigatório '{field}' não fornecido")
        
        aluno = self.repository.update(matricula, data)
        return aluno.to_dict() if aluno else None
    
    def delete_aluno(self, matricula: int) -> bool:
        return self.repository.delete(matricula)
    
    def get_alunos_by_escola(self, id_escola: int) -> List[Dict[str, Any]]:
        alunos = self.repository.get_by_escola(id_escola)
        return [aluno.to_dict() for aluno in alunos]
    
    def search_alunos_by_name(self, nome: str) -> List[Dict[str, Any]]:
        alunos = self.repository.search_by_name(nome)
        return [aluno.to_dict() for aluno in alunos]
    
    def get_alunos_paginated(self, page: int, per_page: int, search: str = '', 
                            escola_id: int = None, serie: int = None, turno: str = None) -> tuple:
        """Get students with pagination and filters"""
        alunos, total, total_pages = self.repository.get_paginated(page, per_page, search, escola_id, serie, turno)
        return [aluno.to_dict() for aluno in alunos], total, total_pages 