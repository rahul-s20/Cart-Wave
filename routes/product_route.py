from flask import Blueprint, request, Response, make_response, jsonify
from controllers.product_controller import ProductC
from utils.tokenization import token_required

product_c = ProductC()

product_blueprint = Blueprint('product_blueprint', __name__, url_prefix='/product')


@product_blueprint.route('/new', methods=['POST'])
@token_required
def create_new_product():
    file = request.files['file']
    content = request.get_json(silent=True)
    res = product_c.create_product(data=content, files=file, token=request.headers.get('Authorization'))
    return res
