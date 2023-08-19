from flask import jsonify, make_response, request, Response
from models.users import Users
from utils.helper import filter_objects_strict
from utils.helper import hashing, check_hash, cookie_expiration_set
from utils.tokenization import encode_token, decode_token
from bson import ObjectId
from mongoengine import Q
import datetime


def user_register(data: dict):
    user_model = Users()
    filtered_data = filter_objects_strict(data, {'email', 'name', 'password'})
    find_one = Users.objects.filter(email=filtered_data['email']).first()

    if find_one:
        return make_response(jsonify({'success': False, 'data': "User Already exists"}), 200)
    elif not filtered_data['email'] or not filtered_data['name'] or not filtered_data['password']:
        return make_response(jsonify({'success': False, 'data': "Missing fields"}), 400)
    else:
        user_model.name = filtered_data['name']
        user_model.email = filtered_data['email']
        user_model.password = hashing(content=filtered_data['password'])
        user_model.save()

    return make_response(jsonify({'success': True, 'data': {
        "id": str(user_model.id),
        "name": user_model.name,
        "email": user_model.email,
        "privilege": user_model.privilege
    }}), 200)


def user_login(data: dict):
    filtered_data = filter_objects_strict(data, {'email', 'password'})
    find_one = Users.objects.filter(email=filtered_data['email']).first()

    if find_one:
        check_pass = check_hash(content=data['password'], hashed_content=find_one.password)
        if check_pass:
            token, options = encode_token(user_id=str(find_one.id))
            response = make_response(jsonify({'success': True, 'data': {
                "id": str(find_one.id),
                "name": find_one.name,
                "email": find_one.email,
                "privilege": find_one.privilege,
                'token': token
            }}), 200)
            response.set_cookie('token', token, expires=cookie_expiration_set(), domain=None,
                                secure=True, httponly=True, samesite='none')
            return response
        else:
            return make_response(jsonify({'success': False, 'data': "Invalid password"}), 401)
    elif not filtered_data['email'] or not filtered_data['password']:
        return make_response(jsonify({'success': False, 'data': "Missing fields"}), 400)
    else:
        return make_response(jsonify({'success': False, 'data': "Please register yourself"}), 401)


def get_single_user_details(_id):
    find_one = Users.objects.filter(id=ObjectId(_id)).first()
    if find_one:
        return make_response(jsonify({'success': True, 'data': {
            "id": str(find_one.id),
            "name": find_one.name,
            "email": find_one.email,
        }}), 200)
    else:
        return make_response(jsonify({'success': False, 'data': "User not found"}), 400)


def get_all_users(token):
    decoded_user = decode_token(token)
    find_users = Users.objects(id__ne=ObjectId(decoded_user['sub']))
    find_users = [{'id': str(i.id), 'name': i.name, 'email': i.email, 'privilege': i.privilege} for i in find_users]
    return make_response(jsonify({'success': True, 'data': find_users}), 200)


def fetch_current_user(token):
    decoded_user = decode_token(token)
    if decoded_user:
        find_user = Users.objects.filter(Q(id=ObjectId(decoded_user['sub'])) and Q(is_active=True)).first()
        if find_user:
            response = make_response(jsonify({'success': True, 'data': {
                "id": str(find_user.id),
                "name": find_user.name,
                "email": find_user.email,
                "privilege": find_user.privilege,
                'token': token
            }}), 200)
            response.set_cookie('token', token, expires=cookie_expiration_set(), domain=None,
                                secure=True, httponly=True, samesite='none')
            return response
        else:
            return make_response(jsonify({'success': False, 'data': "User not found"}), 400)
    else:
        return make_response(jsonify({'success': False, 'data': "Invalid Token"}), 400)


def update_user_privilege(token: str, user_id_update: str, privilege: str):
    try:
        curr_users_prv, _id = check_user_privilege(token=token)
        if curr_users_prv == 'super':
            if user_id_update is None:
                return make_response(jsonify({'success': False, 'data': "User not found"}), 400)
            elif privilege is None:
                return make_response(jsonify({'success': False, 'data': "Invalid: no data provided"}), 400)
            elif privilege not in ['super', 'moderate', 'low']:
                return make_response(jsonify({'success': False, 'data': "Invalid: privilege invalid"}), 400)
            elif _id == user_id_update:
                return make_response(jsonify({'success': False, 'data': "Cannot change privilege for self"}), 400)
            else:
                find_user_u = Users.objects.filter(Q(id=ObjectId(user_id_update)) & Q(is_active=True)).first()
                if find_user_u is None:
                    return make_response(jsonify({'success': False, 'data': "User not found"}), 400)
                else:
                    find_user_u.privilege = privilege
                    find_user_u.save()
                    return make_response(jsonify({'success': True, 'data': {
                        'id': str(find_user_u.id),
                        'email': find_user_u.email,
                        'name': find_user_u.name,
                        'privilege': find_user_u.privilege,
                        'verified': find_user_u.verified,
                        'is_active': find_user_u.is_active
                    }}), 200)
        else:
            return make_response(jsonify({'success': False, 'data': "You are not authorized to update any privilege"}),
                                 400)
    except Exception as er:
        print(er)
        return make_response(jsonify({'success': False, 'data': "Something went wrong"}), 500)


def delete_user_by_admin(token: str, user_id_update: str):
    try:
        curr_users_prv, _id = check_user_privilege(token=token)
        if curr_users_prv == 'super':
            if user_id_update is None:
                return make_response(jsonify({'success': False, 'data': "User not found"}), 400)
            elif _id == user_id_update:
                return make_response(jsonify({'success': False, 'data': "Cannot delete yourself"}), 400)
            else:
                find_user_u = Users.objects.filter(Q(id=ObjectId(user_id_update)) & Q(is_active=True)).first()
                if find_user_u is None:
                    return make_response(jsonify({'success': False, 'data': "User not found"}), 400)
                else:
                    find_user_u.is_active = False
                    find_user_u.save()
                    return make_response(jsonify({'success': True, 'data': 'User deleted'}), 200)
        else:
            return make_response(jsonify({'success': False, 'data': "You are not authorized to update any user"}),
                                 400)
    except Exception as er:
        print(er)
        return make_response(jsonify({'success': False, 'data': "Something went wrong"}), 500)


def logout_user():
    response = make_response(jsonify({'success': True, 'message': 'Logged Out'}), 200)
    response.set_cookie('token', None, expires=datetime.datetime.now(), domain=None,
                        secure=True, httponly=True, samesite='none')
    return response


def check_user_privilege(token):
    decoded_user = decode_token(token)
    if decoded_user:
        find_user = Users.objects.filter(Q(id=ObjectId(decoded_user['sub'])) and Q(is_active=True)).first()
        if find_user:
            return find_user['privilege'], decoded_user['sub']
        else:
            raise ValueError('User does not exists')
    else:
        raise ValueError("Invalid Token")
