from flask import Blueprint, jsonify, request
from sqlalchemy import func, desc, asc, case
from models import Aluno, Escola, Disciplina, Matricula
from app import db

bi_bp = Blueprint('bi', __name__)

@bi_bp.route('/test', methods=['GET'])
def test():
    """Test endpoint for BI"""
    try:
        # Test simple query
        from sqlalchemy import text
        query = text("SELECT COUNT(*) as total FROM escola")
        result = db.session.execute(query).fetchone()
        
        # Debug schools data
        schools_debug = text("""
            SELECT 
                e.nome as school_name,
                e.cidade as city,
                COUNT(DISTINCT m.matricula_aluno) as unique_students,
                COUNT(m.id) as total_enrollments,
                AVG(m.nota) as avg_grade
            FROM escola e
            JOIN matricula m ON e.id_escola = m.id_escola
            GROUP BY e.id_escola, e.nome, e.cidade
            ORDER BY e.nome
            LIMIT 5
        """)
        
        schools_result = db.session.execute(schools_debug).fetchall()
        schools_data = []
        for row in schools_result:
            schools_data.append({
                'school_name': row.school_name,
                'city': row.city,
                'unique_students': row.unique_students,
                'total_enrollments': row.total_enrollments,
                'avg_grade': float(row.avg_grade)
            })
        
        return jsonify({
            'success': True,
            'message': 'BI endpoints are working!',
            'total_schools': result[0] if result else 0,
            'debug_schools': schools_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bi_bp.route('/schools-performance', methods=['GET'])
def schools_performance():
    """Get schools performance data for BI"""
    try:
        # Query to get average performance by school using subquery to avoid duplicates
        from sqlalchemy import text
        
        query = text("""
            WITH school_stats AS (
                SELECT 
                    e.id_escola,
                    e.nome,
                    e.cidade,
                    AVG(m.nota) as average_grade,
                    COUNT(DISTINCT m.matricula_aluno) as total_students,
                    SUM(CASE WHEN m.status = true THEN 1 ELSE 0 END) as approved_count,
                    AVG(CASE WHEN m.status = true THEN 1.0 ELSE 0.0 END) * 100 as approval_rate
                FROM escola e
                JOIN matricula m ON e.id_escola = m.id_escola
                GROUP BY e.id_escola, e.nome, e.cidade
                HAVING COUNT(DISTINCT m.matricula_aluno) > 0
            )
            SELECT 
                nome as school_name,
                cidade as city,
                average_grade,
                total_students,
                approved_count,
                approval_rate
            FROM school_stats
            ORDER BY average_grade DESC
        """)
        
        schools_data = db.session.execute(query).fetchall()
        
        result = []
        for school in schools_data:
            result.append({
                'school_name': school.school_name,
                'city': school.city,
                'average_grade': float(school.average_grade),
                'total_students': school.total_students,
                'approved_count': school.approved_count,
                'approval_rate': float(school.approval_rate * 100)
            })
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bi_bp.route('/subjects-performance', methods=['GET'])
def subjects_performance():
    """Get subjects performance data for BI"""
    try:
        # Query to get average performance by subject using raw SQL
        from sqlalchemy import text
        
        query = text("""
            WITH subject_stats AS (
                SELECT 
                    d.nome,
                    AVG(m.nota) as average_grade,
                    COUNT(DISTINCT m.matricula_aluno) as total_students,
                    SUM(CASE WHEN m.status = true THEN 1 ELSE 0 END) as approved_count,
                    AVG(CASE WHEN m.status = true THEN 1.0 ELSE 0.0 END) * 100 as approval_rate
                FROM disciplina d
                JOIN matricula m ON d.id_disciplina = m.id_disciplina
                GROUP BY d.nome
                HAVING COUNT(DISTINCT m.matricula_aluno) > 0
            )
            SELECT 
                nome as subject_name,
                average_grade,
                total_students,
                approved_count,
                approval_rate
            FROM subject_stats
            ORDER BY average_grade DESC
        """)
        
        subjects_data = db.session.execute(query).fetchall()
        
        result = []
        for subject in subjects_data:
            result.append({
                'subject_name': subject.subject_name,
                'average_grade': float(subject.average_grade),
                'total_students': subject.total_students,
                'approved_count': subject.approved_count,
                'approval_rate': float(subject.approval_rate * 100)
            })
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bi_bp.route('/yearly-trends', methods=['GET'])
def yearly_trends():
    """Get yearly performance trends"""
    try:
        # Query to get performance trends by year
        yearly_data = db.session.query(
            Matricula.ano.label('year'),
            func.avg(Matricula.nota).label('average_grade'),
            func.count(func.distinct(Matricula.matricula_aluno)).label('total_students'),
            func.avg(case((Matricula.status == True, 1), else_=0)).label('approval_rate')
        ).group_by(Matricula.ano)\
         .order_by(Matricula.ano)\
         .all()
        
        result = []
        for year in yearly_data:
            result.append({
                'year': year.year,
                'average_grade': float(year.average_grade),
                'total_students': year.total_students,
                'approval_rate': float(year.approval_rate * 100)
            })
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bi_bp.route('/city-performance', methods=['GET'])
def city_performance():
    """Get performance by city"""
    try:
        # Query to get performance by city
        city_data = db.session.query(
            Escola.cidade.label('city'),
            func.avg(Matricula.nota).label('average_grade'),
            func.count(func.distinct(Matricula.matricula_aluno)).label('total_students'),
            func.avg(case((Matricula.status == True, 1), else_=0)).label('approval_rate')
        ).join(Matricula, Escola.id_escola == Matricula.id_escola)\
         .group_by(Escola.cidade)\
         .order_by(desc(func.avg(Matricula.nota)))\
         .all()
        
        result = []
        for city in city_data:
            result.append({
                'city': city.city,
                'average_grade': float(city.average_grade),
                'total_students': city.total_students,
                'approval_rate': float(city.approval_rate * 100)
            })
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bi_bp.route('/grade-distribution', methods=['GET'])
def grade_distribution():
    """Get grade distribution for histogram"""
    try:
        # Query to get grade distribution
        grade_data = db.session.query(
            func.floor(Matricula.nota).label('grade_range'),
            func.count(Matricula.id).label('count')
        ).group_by(func.floor(Matricula.nota))\
         .order_by(func.floor(Matricula.nota))\
         .all()
        
        result = []
        for grade in grade_data:
            result.append({
                'grade_range': int(grade.grade_range),
                'count': grade.count
            })
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bi_bp.route('/debug-schools', methods=['GET'])
def debug_schools():
    """Debug endpoint to check schools data"""
    try:
        from sqlalchemy import text
        
        # Query simples para ver todas as escolas
        query = text("""
            SELECT DISTINCT e.id_escola, e.nome, e.cidade
            FROM escola e
            ORDER BY e.nome
        """)
        
        schools = db.session.execute(query).fetchall()
        
        # Query para ver matrículas por escola
        enrollments_query = text("""
            SELECT 
                e.nome as school_name,
                COUNT(m.id) as total_enrollments,
                COUNT(DISTINCT m.matricula_aluno) as unique_students
            FROM escola e
            LEFT JOIN matricula m ON e.id_escola = m.id_escola
            GROUP BY e.id_escola, e.nome
            ORDER BY e.nome
        """)
        
        enrollments = db.session.execute(enrollments_query).fetchall()
        
        return jsonify({
            'success': True,
            'total_schools': len(schools),
            'schools': [{'id': s.id_escola, 'nome': s.nome, 'cidade': s.cidade} for s in schools],
            'enrollments': [{'school': e.school_name, 'total': e.total_enrollments, 'unique': e.unique_students} for e in enrollments]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 