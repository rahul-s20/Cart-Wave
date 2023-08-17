from flask import Blueprint, request, Response, make_response, jsonify
from controllers.order_controller import create_order
from utils.tokenization import token_required
from utils.helper import filter_objects

order_blueprint = Blueprint('order_blueprint', __name__, url_prefix='/order')


@order_blueprint.route('/new', methods=['POST'])
@token_required
def create_new_product():
    content = request.get_json(silent=True)
    res = create_order(data=content)
    return res
