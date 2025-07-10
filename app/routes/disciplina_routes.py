from flask import Blueprint, request, jsonify
from services.disciplina_service import DisciplinaService

disciplina_bp = Blueprint('disciplina', __name__)
disciplina_service = DisciplinaService()

@disciplina_bp.route('/', methods=['GET'])
def get_disciplinas():
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        # Ensure reasonable limits
        page = max(1, page)
        per_page = min(max(1, per_page), 100)  # Between 1 and 100
        
        disciplinas, total, total_pages = disciplina_service.get_disciplinas_paginated(
            page, per_page, search
        )
        
        return jsonify({
            'disciplinas': disciplinas,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }), 200
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

@disciplina_bp.route('/<int:id_disciplina>', methods=['PUT'])
def update_disciplina(id_disciplina):
    try:
        data = request.get_json()
        disciplina = disciplina_service.update_disciplina(id_disciplina, data)
        if disciplina:
            return jsonify(disciplina), 200
        return jsonify({'error': 'Disciplina não encontrada'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@disciplina_bp.route('/<int:id_disciplina>', methods=['DELETE'])
def delete_disciplina(id_disciplina):
    try:
        success = disciplina_service.delete_disciplina(id_disciplina)
        if success:
            return jsonify({'message': 'Disciplina excluída com sucesso'}), 200
        return jsonify({'error': 'Disciplina não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 