# services/users/project/api/users.py
from flask import Blueprint, jsonify, request
from project.api.models import Auto
from project import db
from sqlalchemy import exc

autos_blueprint = Blueprint('autos', __name__)

@autos_blueprint.route('/autos/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })



@autos_blueprint.route('/autos', methods=['POST'])
def add_autos():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    marca = post_data.get('marca')
    modelo = post_data.get('modelo')
    tipo = post_data.get('tipo')
    color = post_data.get('color')
    placa = post_data.get('placa')

    try:
        auto = Auto.query.filter_by(placa=placa).first()
        if not auto:
            db.session.add(Auto(marca=marca, modelo=modelo, tipo=tipo, color=color, placa=placa))
            db.session.commit()
            response_object['status'] = 'satisfactorio'
            response_object['message'] = f'{placa} a sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['estado'] = 'fallo'
            response_object['mensaje'] = 'Disculpe. Esta placa ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@autos_blueprint.route('/autos/<auto_id>', methods=['GET'])
def get_single_auto(auto_id):
    """Obtener detalles de auto único """
    response_object = {
        'estado': 'fallo',
        'mensaje': 'El auto no existe'
    }
    try:
        auto = Auto.query.filter_by(id=int(auto_id)).first()
        if not auto:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': auto.id,
                    'marca': auto.marca,
                    'modelo': auto.modelo,
                    'tipo': auto.tipo,
                    'color': auto.color,
                    'placa': auto.placa
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

@autos_blueprint.route('/autos', methods=['GET'])
def get_all_auto():
    """Obteniendo todos los usuarios"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'autos': [auto.to_json() for auto in Auto.query.all()]
        }
    }
    return jsonify(response_object), 200

