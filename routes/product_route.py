from flask import Blueprint, request, Response, make_response, jsonify
from controllers.product_controller import ProductC
from utils.tokenization import token_required
from utils.helper import filter_objects

product_c = ProductC()

product_blueprint = Blueprint('product_blueprint', __name__, url_prefix='/product')


@product_blueprint.route('/new', methods=['POST'])
@token_required
def create_new_product():
    content = request.get_json(silent=True)
    if content:
        res = product_c.create_product(data=content, token=request.headers.get('Authorization'))
    else:
        file = request.files.getlist('images')
        dict_data = {
            "name": request.form['name'],
            "description": request.form['description'],
            "price": request.form['price'],
            "colors": request.form['colors'],
            "sizes": request.form['sizes'],
            "company": request.form['company'],
            "category": request.form['category'],
            "stock": request.form['stock']
        }
        res = product_c.create_product(data=dict_data, files=file, token=request.headers.get('Authorization'))
    return res


@product_blueprint.route('/<product_id>', methods=['PUT'])
@token_required
def update_product(product_id):
    content = request.get_json(silent=True)
    if content:
        filtered_data = filter_objects(content,
                                       {"name", "description", "price", "colors", "sizes", "company", "category",
                                        "stock",
                                        "images", "is_active"})
        res = product_c.update_product(prd_id=product_id, token=request.headers.get('Authorization'),
                                       data=filtered_data)
    else:
        parameters = request.form.to_dict()
        filtered_data = filter_objects(parameters,
                                       {"name", "description", "price", "colors", "sizes", "company", "category",
                                        "stock",
                                        "images", "is_active"})
        if request.files.getlist('images'):
            filtered_data["images"] = request.files.getlist('images')
        else:
            filtered_data["images"] = None
        res = product_c.update_product(prd_id=product_id, token=request.headers.get('Authorization'),
                                       data=filtered_data)
    return res


@product_blueprint.route('/status/<product_id>', methods=['PUT'])
@token_required
def delete_product(product_id):
    try:
        content = request.get_json(silent=True)
        if content:
            filtered_data = filter_objects(content, {"is_active"})
            res = product_c.update_product(prd_id=product_id, token=request.headers.get('Authorization'),
                                           data=filtered_data)
        else:
            parameters = request.form.to_dict()
            filtered_data = filter_objects(parameters, {"is_active"})
            res = product_c.update_product(prd_id=product_id, token=request.headers.get('Authorization'),
                                           data=filtered_data)
        return res
    except Exception as er:
        print(er)
        return make_response(jsonify({'success': False, 'data': f"{er}"}), 500)
