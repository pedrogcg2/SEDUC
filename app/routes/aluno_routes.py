from flask import Blueprint, request, jsonify
from services.aluno_service import AlunoService
from datetime import datetime

aluno_bp = Blueprint('aluno', __name__)
aluno_service = AlunoService()

@aluno_bp.route('/', methods=['GET'])
def get_alunos():
    try:
        # Handle query parameters
        escola_id = request.args.get('escola_id', type=int)
        serie = request.args.get('serie', type=int)
        turno = request.args.get('turno')
        nome = request.args.get('nome')
        
        if escola_id:
            alunos = aluno_service.get_alunos_by_escola(escola_id)
        elif serie:
            alunos = aluno_service.get_all_alunos()  # Filter by serie in service
            alunos = [a for a in alunos if a['serie'] == serie]
        elif turno:
            alunos = aluno_service.get_all_alunos()  # Filter by turno in service
            alunos = [a for a in alunos if a['turno'] == turno]
        elif nome:
            alunos = aluno_service.search_alunos_by_name(nome)
        else:
            alunos = aluno_service.get_all_alunos()
        
        return jsonify(alunos), 200
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