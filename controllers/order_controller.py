from flask import jsonify, make_response, request, Response
from models.products import Products, Image, Review
from models.orders import Orders, User, Items, ShippingInformation, PaymentInformation
from utils.helper import filter_objects
from utils.s3.s3_io import S3_Io
from utils.tokenization import decode_token
from os import environ as env
from bson import ObjectId
from controllers.user_controller import check_user_privilege
from mongoengine import Q


def create_order(data: dict):
    oder_obj = Orders()
    user_obj = User()
    items_obj = Items()
    shipping_obj = ShippingInformation()
    payment_obj = PaymentInformation()
    items_list = list()
    try:
        for key, value in data['shippingInfo'].items():
            setattr(shipping_obj, key, value)

        for key, value in data['paymentInfo'].items():
            setattr(payment_obj, key, value)

        for i in data['orderItems']:
            for key, value in i.items():
                if key == 'product':
                    value = ObjectId(value)
                    find_product = Products.objects.filter(Q(id=ObjectId(value)) & Q(is_active=True)).first()
                    if find_product is None:
                        return make_response(jsonify({'success': False, 'data': f"The product does not exists"}), 400)
                setattr(items_obj, key, value)
            items_list.append(items_obj)

        for key, value in data.items():
            if key == 'name' or key == 'email':
                setattr(user_obj, key, value)
            elif key != 'shippingInfo' and key != 'paymentInfo' and key != 'orderItems':
                setattr(oder_obj, key, value)
        if len(items_list) > 0:
            oder_obj.orderItems = items_list
        oder_obj.shippingInfo = shipping_obj
        oder_obj.paymentInfo = payment_obj
        oder_obj.save()
        return make_response(jsonify({'success': True, 'data': "Order created successfully"}), 200)
    except Exception as er:
        return make_response(jsonify({'success': False, 'data': f"{er}"}), 500)


def get_all_orders(token: str):
    curr_users_prv, _id = check_user_privilege(token=token)

    if curr_users_prv == 'super':
        all_orders = Orders.objects()
        return make_response(jsonify({'success': True, 'data': all_orders}), 200)
    else:
        return make_response(jsonify({'success': False, 'data': "Invalid: privilege invalid"}), 400)