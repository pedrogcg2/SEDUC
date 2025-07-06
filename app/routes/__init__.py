from routes.aluno_routes import aluno_bp
from routes.escola_routes import escola_bp
from routes.disciplina_routes import disciplina_bp
from routes.matricula_routes import matricula_bp
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp

__all__ = [
    'aluno_bp',
    'escola_bp', 
    'disciplina_bp', 
    'matricula_bp',
    'auth_bp',
    'user_bp'
] 