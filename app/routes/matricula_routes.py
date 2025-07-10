from flask import Blueprint, request, jsonify
from services.matricula_service import MatriculaService

matricula_bp = Blueprint('matricula', __name__)
matricula_service = MatriculaService()

@matricula_bp.route('/', methods=['GET'])
def get_matriculas():
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        # Ensure reasonable limits
        page = max(1, page)
        per_page = min(max(1, per_page), 100)  # Between 1 and 100
        
        matriculas, total, total_pages = matricula_service.get_matriculas_paginated(
            page, per_page, search
        )
        
        return jsonify({
            'enrollments': matriculas,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matricula_bp.route('/<int:id>', methods=['GET'])
def get_matricula(id):
    try:
        matricula = matricula_service.get_matricula_by_id(id)
        if matricula:
            return jsonify(matricula), 200
        return jsonify({'error': 'Matrícula não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matricula_bp.route('/', methods=['POST'])
def create_matricula():
    try:
        data = request.get_json()
        matricula = matricula_service.create_matricula(data)
        return jsonify(matricula), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matricula_bp.route('/<int:id>', methods=['PUT'])
def update_matricula(id):
    try:
        data = request.get_json()
        matricula = matricula_service.update_matricula(id, data)
        if matricula:
            return jsonify(matricula), 200
        return jsonify({'error': 'Matrícula não encontrada'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matricula_bp.route('/<int:id>', methods=['DELETE'])
def delete_matricula(id):
    try:
        success = matricula_service.delete_matricula(id)
        if success:
            return jsonify({'message': 'Matrícula excluída com sucesso'}), 200
        return jsonify({'error': 'Matrícula não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Performance routes
@matricula_bp.route('/performance/<int:matricula_aluno>', methods=['GET'])
def get_aluno_performance(matricula_aluno):
    try:
        ano = request.args.get('ano', type=int)
        matriculas = matricula_service.get_aluno_performance(matricula_aluno, ano)
        return jsonify(matriculas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 