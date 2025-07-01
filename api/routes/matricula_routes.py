from flask import Blueprint, request, jsonify
from ..services.matricula_service import MatriculaService

matricula_bp = Blueprint('matricula', __name__)
matricula_service = MatriculaService()

@matricula_bp.route('/', methods=['GET'])
def get_matriculas():
    try:
        aluno_id = request.args.get('aluno_id', type=int)
        escola_id = request.args.get('escola_id', type=int)
        disciplina_id = request.args.get('disciplina_id', type=int)
        ano = request.args.get('ano', type=int)
        serie = request.args.get('serie', type=int)
        status = request.args.get('status', type=lambda v: v.lower() == 'true')
        
        if aluno_id:
            matriculas = matricula_service.get_matriculas_by_aluno(aluno_id)
        elif escola_id:
            matriculas = matricula_service.get_all_matriculas()  # Filter by escola_id in service
            matriculas = [m for m in matriculas if m['id_escola'] == escola_id]
        elif disciplina_id:
            matriculas = matricula_service.get_all_matriculas()  # Filter by disciplina_id in service
            matriculas = [m for m in matriculas if m['id_disciplina'] == disciplina_id]
        elif ano:
            matriculas = matricula_service.get_all_matriculas()  # Filter by ano in service
            matriculas = [m for m in matriculas if m['ano'] == ano]
        elif serie:
            matriculas = matricula_service.get_all_matriculas()  # Filter by serie in service
            matriculas = [m for m in matriculas if m['serie'] == serie]
        elif status is not None:
            matriculas = matricula_service.get_all_matriculas()  # Filter by status in service
            matriculas = [m for m in matriculas if m['status'] == status]
        else:
            matriculas = matricula_service.get_all_matriculas()
        
        return jsonify(matriculas), 200
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

# Performance routes
@matricula_bp.route('/performance/<int:matricula_aluno>', methods=['GET'])
def get_aluno_performance(matricula_aluno):
    try:
        ano = request.args.get('ano', type=int)
        matriculas = matricula_service.get_aluno_performance(matricula_aluno, ano)
        return jsonify(matriculas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 