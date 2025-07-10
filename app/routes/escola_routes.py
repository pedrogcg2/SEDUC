from flask import Blueprint, request, jsonify
from services.escola_service import EscolaService

escola_bp = Blueprint('escola', __name__)
escola_service = EscolaService()

@escola_bp.route('/', methods=['GET'])
def get_escolas():
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        # Handle query parameters
        cidade = request.args.get('cidade')
        
        # Ensure reasonable limits
        page = max(1, page)
        per_page = min(max(1, per_page), 100)  # Between 1 and 100
        
        escolas, total, total_pages = escola_service.get_escolas_paginated(
            page, per_page, search, cidade
        )
        
        return jsonify({
            'escolas': escolas,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@escola_bp.route('/<int:id_escola>', methods=['GET'])
def get_escola(id_escola):
    try:
        escola = escola_service.get_escola_by_id(id_escola)
        if escola:
            return jsonify(escola), 200
        return jsonify({'error': 'Escola não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@escola_bp.route('/', methods=['POST'])
def create_escola():
    try:
        data = request.get_json()
        escola = escola_service.create_escola(data)
        return jsonify(escola), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@escola_bp.route('/<int:id_escola>', methods=['PUT'])
def update_escola(id_escola):
    try:
        data = request.get_json()
        escola = escola_service.update_escola(id_escola, data)
        if escola:
            return jsonify(escola), 200
        return jsonify({'error': 'Escola não encontrada'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@escola_bp.route('/<int:id_escola>', methods=['DELETE'])
def delete_escola(id_escola):
    try:
        success = escola_service.delete_escola(id_escola)
        if success:
            return jsonify({'message': 'Escola excluída com sucesso'}), 200
        return jsonify({'error': 'Escola não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 