from flask import Blueprint, request, jsonify
from ..services.disciplina_service import DisciplinaService

disciplina_bp = Blueprint('disciplina', __name__)
disciplina_service = DisciplinaService()

@disciplina_bp.route('/', methods=['GET'])
def get_disciplinas():
    try:
        nome = request.args.get('nome')
        
        if nome:
            disciplinas = disciplina_service.get_all_disciplinas()  # Filter by nome in service
            disciplinas = [d for d in disciplinas if nome.lower() in d['nome'].lower()]
        else:
            disciplinas = disciplina_service.get_all_disciplinas()
        
        return jsonify(disciplinas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@disciplina_bp.route('/<int:id_disciplina>', methods=['GET'])
def get_disciplina(id_disciplina):
    try:
        disciplina = disciplina_service.get_disciplina_by_id(id_disciplina)
        if disciplina:
            return jsonify(disciplina), 200
        return jsonify({'error': 'Disciplina não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@disciplina_bp.route('/', methods=['POST'])
def create_disciplina():
    try:
        data = request.get_json()
        disciplina = disciplina_service.create_disciplina(data)
        return jsonify(disciplina), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500 