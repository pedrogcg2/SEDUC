from flask import Blueprint, request, jsonify
from services.aluno_service import AlunoService
from datetime import datetime

aluno_bp = Blueprint('aluno', __name__)
aluno_service = AlunoService()

@aluno_bp.route('/', methods=['GET'])
def get_alunos():
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        # Handle query parameters
        escola_id = request.args.get('escola_id', type=int)
        serie = request.args.get('serie', type=int)
        turno = request.args.get('turno')
        
        # Ensure reasonable limits
        page = max(1, page)
        per_page = min(max(1, per_page), 100)  # Between 1 and 100
        
        alunos, total, total_pages = aluno_service.get_alunos_paginated(
            page, per_page, search, escola_id, serie, turno
        )
        
        return jsonify({
            'students': alunos,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@aluno_bp.route('/<int:matricula>', methods=['GET'])
def get_aluno(matricula):
    try:
        aluno = aluno_service.get_aluno_by_id(matricula)
        if aluno:
            return jsonify(aluno), 200
        return jsonify({'error': 'Aluno não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@aluno_bp.route('/', methods=['POST'])
def create_aluno():
    try:
        data = request.get_json()
        
        # Convert date string to date object
        if 'data_mat' in data:
            data['data_mat'] = datetime.strptime(data['data_mat'], '%Y-%m-%d').date()
        
        aluno = aluno_service.create_aluno(data)
        return jsonify(aluno), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@aluno_bp.route('/<int:matricula>', methods=['PUT'])
def update_aluno(matricula):
    try:
        data = request.get_json()
        
        # Convert date string to date object
        if 'data_mat' in data:
            data['data_mat'] = datetime.strptime(data['data_mat'], '%Y-%m-%d').date()
        
        aluno = aluno_service.update_aluno(matricula, data)
        if aluno:
            return jsonify(aluno), 200
        return jsonify({'error': 'Aluno não encontrado'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@aluno_bp.route('/<int:matricula>', methods=['DELETE'])
def delete_aluno(matricula):
    try:
        success = aluno_service.delete_aluno(matricula)
        if success:
            return jsonify({'message': 'Aluno excluído com sucesso'}), 200
        return jsonify({'error': 'Aluno não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 