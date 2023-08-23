from flask import Blueprint, request, Response, make_response, jsonify
from controllers.product_controller import ProductC, fetch_all_products, fetch_single_product
from utils.tokenization import token_required
from utils.helper import filter_objects
from flask_cors import cross_origin
from controllers.user_controller import fetch_current_user
from utils.helper import crossdomain

product_c = ProductC()

product_blueprint = Blueprint('product_blueprint', __name__, url_prefix='/api/v1/product')


@product_blueprint.route('/new', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
@token_required
def create_new_product():
    content = request.get_json(silent=True)
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    if content:
        res = product_c.create_product(data=content, token=token)
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
        res = product_c.create_product(data=dict_data, files=file, token=token)
    return res


@product_blueprint.route('/<product_id>', methods=['PUT', 'DELETE', 'OPTIONS'])
@cross_origin(supports_credentials=True)
@token_required
def update_product(product_id):
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    if request.method == 'PUT':
        content = request.get_json(silent=True)
        print(">>>>>>>>>>>>>>")
        print(content)
        if content:
            filtered_data = filter_objects(content,
                                           {"name", "description", "price", "colors", "sizes", "company", "category",
                                            "stock",
                                            "images", "is_active"})
            res = product_c.update_product(prd_id=product_id, token=token,
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
            res = product_c.update_product(prd_id=product_id, token=token, data=filtered_data)
        return res
    elif request.method == 'DELETE':
        content = request.get_json(silent=True)
        if content:
            filtered_data = filter_objects(content, {"is_active"})
            res = product_c.update_product(prd_id=product_id, token=token, data=filtered_data)
        else:
            parameters = request.form.to_dict()
            filtered_data = filter_objects(parameters, {"is_active"})
            res = product_c.update_product(prd_id=product_id, token=token,
                                           data=filtered_data)
        return res


@product_blueprint.route('/status/<product_id>', methods=['PUT'])
@token_required
def delete_product(product_id):
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    try:
        content = request.get_json(silent=True)
        if content:
            filtered_data = filter_objects(content, {"is_active"})
            res = product_c.update_product(prd_id=product_id, token=token,
                                           data=filtered_data)
        else:
            parameters = request.form.to_dict()
            filtered_data = filter_objects(parameters, {"is_active"})
            res = product_c.update_product(prd_id=product_id, token=token, data=filtered_data)
        return res
    except Exception as er:
        print(er)
        return make_response(jsonify({'success': False, 'data': f"{er}"}), 500)


@product_blueprint.route('/products', methods=['GET'])
@cross_origin(origin=["*"], supports_credentials=True)
@token_required
def fetch_products():
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    res = fetch_all_products(token=token)
    return res


@product_blueprint.route('/products/<product_id>', methods=['GET'])
@cross_origin(origin=["*"], supports_credentials=True)
@token_required
def fetch_single_prd(product_id):
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    res = fetch_single_product(token=token, product_id=product_id)
    return res
