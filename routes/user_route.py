from flask import Blueprint, request, Response, make_response, jsonify, current_app
from controllers.user_controller import user_register, user_login, get_single_user_details, \
    get_all_users, fetch_current_user, update_user_privilege, delete_user_by_admin, logout_user
from utils.tokenization import token_required
from flask_cors import cross_origin

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix='/api/v1/admin')


@user_blueprint.route('/auth', methods=['POST'])
@token_required
@cross_origin(origin=["*"], supports_credentials=True)
def auth_profile():
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    res = fetch_current_user(token=token)
    return res


@user_blueprint.route('/login', methods=['POST'])
@cross_origin(origin=["*"], supports_credentials=True)
def login():
    content = request.get_json(silent=True)
    res = user_login(data=content)
    return res


@user_blueprint.route('/register', methods=['POST'])
@cross_origin(origin=["*"], supports_credentials=True)
def register():
    content = request.get_json(silent=True)
    res = user_register(data=content)
    return res


@user_blueprint.route('/logout', methods=['GET'])
@token_required
@cross_origin(origin=["*"], supports_credentials=True)
def logout():
    res = logout_user()
    return res


@user_blueprint.route('/auth-test', methods=['POST'])
@token_required
def auth_test():
    return 'granted'


@user_blueprint.route('/users', methods=['GET'])
@token_required
def users():
    if request.args.get('id'):
        res = get_single_user_details(_id=request.args.get('id'))
    else:
        res = get_all_users(token=request.headers.get('Authorization'))
    return res


@user_blueprint.route('/users/<user_id>', methods=['GET'])
@token_required
def single_user(user_id):
    res = get_single_user_details(_id=user_id)
    return res


@user_blueprint.route('/users/<user_id>', methods=['PUT'])
@token_required
def users_put(user_id):
    # request.args.get('id')
    content = request.get_json(silent=True)
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    res = update_user_privilege(token=token,
                                user_id_update=user_id, privilege=content['privilege'])
    return res


@user_blueprint.route('/users/<user_id>', methods=['DELETE'])
@token_required
def users_delete(user_id):
    token = request.headers.get('Authorization') if request.headers.get('Authorization') else request.cookies.get(
        'token')
    res = delete_user_by_admin(token=token, user_id_update=user_id)
    return res
