from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'postgresql://master:HgAXVS5uWph3@localhost/sqldb-seduc'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from .routes import aluno_bp, escola_bp, disciplina_bp, matricula_bp
    app.register_blueprint(aluno_bp, url_prefix='/api/alunos')
    app.register_blueprint(escola_bp, url_prefix='/api/escolas')
    app.register_blueprint(disciplina_bp, url_prefix='/api/disciplinas')
    app.register_blueprint(matricula_bp, url_prefix='/api/matriculas')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'SEDUC API is running'}
    
    return app 