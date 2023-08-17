from flask import Blueprint, request, Response, make_response, jsonify
from controllers.user_controller import user_register, user_login, get_single_user_details, \
    get_all_users, fetch_current_user, update_user_privilege, delete_user_by_admin
from utils.tokenization import token_required

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix='/auth')


@user_blueprint.route('/register', methods=['POST'])
def register():
    content = request.get_json(silent=True)
    res = user_register(data=content)
    return res


@user_blueprint.route('/auth-test', methods=['POST'])
@token_required
def auth_test():
    return 'granted'


@user_blueprint.route('/login', methods=['POST'])
def login():
    print("login...........")
    content = request.get_json(silent=True)
    res = user_login(data=content)
    return res


@user_blueprint.route('/users', methods=['GET'])
@token_required
def users():
    if request.args.get('id'):
        res = get_single_user_details(_id=request.args.get('id'))
    else:
        res = get_all_users(token=request.headers.get('Authorization'))
    return res


@user_blueprint.route('/auth', methods=['post'])
@token_required
def auth_profile():
    res = fetch_current_user(token=request.headers.get('Authorization'))
    return res


@user_blueprint.route('/users', methods=['PUT'])
@token_required
def users_put():
    # request.args.get('id')
    content = request.get_json(silent=True)
    res = update_user_privilege(token=request.headers.get('Authorization'),
                                user_id_update=request.args.get('id'), privilege=content['privilege'])
    return res


@user_blueprint.route('/users', methods=['DELETE'])
@token_required
def users_delete():
    res = delete_user_by_admin(token=request.headers.get('Authorization'), user_id_update=request.args.get('id'))
    return res