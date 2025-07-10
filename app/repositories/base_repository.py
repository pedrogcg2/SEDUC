from typing import List, Optional, Dict, Any
from app import db

class BaseRepository:
    def __init__(self, model):
        self.model = model
    
    def get_all(self) -> List[Any]:
        return self.model.query.all()
    
    def get_by_id(self, id: int) -> Optional[Any]:
        return self.model.query.get(id)
    
    def create(self, data: Dict[str, Any]) -> Any:
        instance = self.model(**data)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[Any]:
        instance = self.get_by_id(id)
        if instance:
            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            db.session.commit()
        return instance
    
    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False 