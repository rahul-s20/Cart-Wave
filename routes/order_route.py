from flask import Blueprint, request, Response, make_response, jsonify
from controllers.order_controller import create_order, get_all_orders, get_single_order
from utils.tokenization import token_required
from utils.helper import filter_objects
from flask_cors import cross_origin

order_blueprint = Blueprint('order_blueprint', __name__, url_prefix='/api/v1/orders')


@order_blueprint.route('/new', methods=['POST'])
@token_required
def create_new_order():
    content = request.get_json(silent=True)
    res = create_order(data=content)
    return res


@order_blueprint.route('/<order_id>', methods=['PUT'])
@token_required
def update_orders(order_id):
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    res = get_all_orders(token=token)
    return res


@order_blueprint.route('', methods=['GET'])
@token_required
@cross_origin(origin=["*"], supports_credentials=True)
def get_orders():
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    res = get_all_orders(token=token)
    return res


@order_blueprint.route('/<order_id>', methods=['GET'])
@token_required
@cross_origin(origin=["*"], supports_credentials=True)
def get_single_order(order_id):
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    res = get_single_order(token=token, order_id=order_id)
    return res
