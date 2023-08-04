from flask import jsonify, make_response, request, Response
from models.users import Users
from utils.helper import filter_objects
from utils.helper import hashing, check_hash
from utils.tokenization import encode_token, decode_token
from bson import ObjectId
from mongoengine import Q


def user_register(data: dict):
    user_model = Users()
    filtered_data = filter_objects(data, {'email', 'name', 'password'})
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
    filtered_data = filter_objects(data, {'email', 'password'})
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
            response.set_cookie('token', token)
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
            response.set_cookie('token', token)
            return response
        else:
            return make_response(jsonify({'success': False, 'data': "User not found"}), 400)
    else:
        return make_response(jsonify({'success': False, 'data': "Invalid Token"}), 400)
