from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from sqlalchemy import text

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'postgresql://master:HgAXVS5uWph3@localhost/sqldb-seduc?client_encoding=utf8'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Initialize extensions with app
    db.init_app(app)
    # Teste de conexão com o banco de dados
    try:
        with app.app_context():
            # Executa uma consulta simples para testar a conexão
            db.session.execute(text('SELECT 1'))
        print('Conexão com o banco de dados estabelecida com sucesso!')
    except Exception as e:
        print(f'Erro ao conectar ao banco de dados: {e}')
    migrate.init_app(app, db)
    
    # Register blueprints
    from routes import aluno_bp, escola_bp, disciplina_bp, matricula_bp, auth_bp, user_bp
    from routes.bi_routes import bi_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(aluno_bp, url_prefix='/api/alunos')
    app.register_blueprint(escola_bp, url_prefix='/api/escolas')
    app.register_blueprint(disciplina_bp, url_prefix='/api/disciplinas')
    app.register_blueprint(matricula_bp, url_prefix='/api/matriculas')
    app.register_blueprint(bi_bp, url_prefix='/api/bi')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'SEDUC API is running'}
    
    # Frontend routes
    @app.route('/')
    def index():
        return send_from_directory('templates', 'login.html')
    
    @app.route('/login')
    def login_page():
        return send_from_directory('templates', 'login.html')
    
    @app.route('/dashboard')
    def dashboard_page():
        return send_from_directory('templates', 'dashboard.html')
    
    @app.route('/admin')
    def admin_page():
        return send_from_directory('templates', 'admin.html')
    
    @app.route('/bi')
    def bi_dashboard():
        return send_from_directory('templates', 'bi_dashboard.html')
    
    return app 