from flask import Blueprint, request, jsonify
from ..services.escola_service import EscolaService

escola_bp = Blueprint('escola', __name__)
escola_service = EscolaService()

@escola_bp.route('/', methods=['GET'])
def get_escolas():
    try:
        cidade = request.args.get('cidade')
        nome = request.args.get('nome')
        
        if cidade:
            escolas = escola_service.get_escolas_by_cidade(cidade)
        elif nome:
            escolas = escola_service.get_all_escolas()  # Filter by nome in service
            escolas = [e for e in escolas if nome.lower() in e['nome'].lower()]
        else:
            escolas = escola_service.get_all_escolas()
        
        return jsonify(escolas), 200
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