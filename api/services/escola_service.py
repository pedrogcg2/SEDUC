from typing import List, Optional, Dict, Any
from ..repositories.escola_repository import EscolaRepository

class EscolaService:
    def __init__(self):
        self.repository = EscolaRepository()
    
    def get_all_escolas(self) -> List[Dict[str, Any]]:
        escolas = self.repository.get_all()
        return [escola.to_dict() for escola in escolas]
    
    def get_escola_by_id(self, id_escola: int) -> Optional[Dict[str, Any]]:
        escola = self.repository.get_by_id(id_escola)
        return escola.to_dict() if escola else None
    
    def create_escola(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Validate required fields
        required_fields = ['nome', 'endereco', 'cidade']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo obrigatório '{field}' não fornecido")
        
        escola = self.repository.create(data)
        return escola.to_dict()
    
    def get_escolas_by_cidade(self, cidade: str) -> List[Dict[str, Any]]:
        escolas = self.repository.get_by_cidade(cidade)
        return [escola.to_dict() for escola in escolas] 