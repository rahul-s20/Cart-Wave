from flask import jsonify, make_response, request, Response
from models.products import Products, Image, Review
from utils.helper import filter_objects
from utils.s3.s3_io import S3_Io
from utils.tokenization import decode_token
from os import environ as env
from bson import ObjectId
from controllers.user_controller import check_user_privilege
from mongoengine import Q


class ProductC:
    def __init__(self):
        self.s3_obj = S3_Io(OVERRIDE_S3_ENDPOINT=env['OVERRIDE_S3_ENDPOINT'], ACCESS_KEY=env['ACCESS_KEY'],
                            SECRET_KEY=env['SECRET_KEY'], REGION=env['REGION'])
        self.product_model = Products()

    def create_product(self, data: dict, token, files=None):
        img_list = list()
        image_obj = Image()
        try:
            decoded_token = decode_token(token=token)
            if files:
                all_keys = self.s3_obj.upload_files(uid=decoded_token['sub'], files=files, key='CART_WAVE_DEV/PRODUCTS',
                                                    bucket_name=env['BUCKET'],
                                                    base_url=env['OBJECT_BASE_URL'])

            else:
                all_keys = self.s3_obj.upload_files(uid=decoded_token['sub'], files=data['images'],
                                                    key='CART_WAVE_DEV/PRODUCTS',
                                                    bucket_name=env['BUCKET'],
                                                    base_url=env['OBJECT_BASE_URL'])
            for i in all_keys:
                image_obj.public_id = i.split('/')[-1].replace('.', '')
                image_obj.url = i
                img_list.append(image_obj)

            if len(img_list) > 0:
                self.product_model.images = img_list

            for key, value in data.items():
                if key == "colors":
                    value = value.split(',')
                    setattr(self.product_model, key, value)
                elif key == "sizes":
                    value = value.split(',')
                    setattr(self.product_model, key, value)
                elif key == "price":
                    value = float(value)
                    setattr(self.product_model, key, value)
                elif key != "images":
                    setattr(self.product_model, key, value)
            self.product_model.admin = ObjectId(decoded_token['sub'])
            self.product_model.save()
            return make_response(jsonify({'success': True, 'data': "Product created successfully"}), 200)
        except Exception as er:
            return make_response(jsonify({'success': False, 'data': f"{er}"}), 500)

    def update_product(self, prd_id: str, token: str, data: dict):
        img_list = list()
        image_obj = Image()
        curr_users_prv, _id = check_user_privilege(token=token)
        decoded_token = decode_token(token=token)
        try:
            if curr_users_prv == 'super':
                find_product = Products.objects.filter(Q(id=ObjectId(prd_id)) & Q(is_active=True)).first()
                if find_product is not None:
                    if data.__contains__('images'):
                        if data['images']:
                            all_keys = self.s3_obj.upload_files(uid=decoded_token['sub'], files=data['images'],
                                                                key='CART_WAVE_DEV/PRODUCTS',
                                                                bucket_name=env['BUCKET'],
                                                                base_url=env['OBJECT_BASE_URL'])
                            for i in all_keys:
                                image_obj.public_id = i.split('/')[-1].replace('.', '')
                                image_obj.url = i
                                img_list.append(image_obj)
                            find_product.images = all_keys

                    for key, value in data.items():
                        if key == "colors":
                            value = value.split(',')
                            setattr(find_product, key, value)
                        elif key == "sizes":
                            value = value.split(',')
                            setattr(find_product, key, value)
                        elif key == "price":
                            value = float(value)
                            setattr(find_product, key, value)
                        elif key != "images":
                            setattr(find_product, key, value)
                    find_product.save()
                    return make_response(jsonify({'success': True, 'data': "Product updated successfully"}), 200)
                elif find_product is None:
                    return make_response(jsonify({'success': False, 'data': "Product is deactivated already"}), 400)
            else:
                return make_response(jsonify({'success': False, 'data': "Invalid: privilege invalid"}), 400)
        except Exception as er:
            return make_response(jsonify({'success': False, 'data': f"{er}"}), 500)


def fetch_all_products(token: str):
    curr_users_prv, _id = check_user_privilege(token=token)

    if curr_users_prv == 'super':
        all_prd = Products.objects()
        return make_response(jsonify({'success': True, 'data': all_prd}), 200)
    elif curr_users_prv in ['moderate', 'low']:
        all_prd = Products.objects(is_active=True)
        return make_response(jsonify({'success': True, 'data': all_prd}), 200)
    else:
        return make_response(jsonify({'success': False, 'data': "Invalid: privilege invalid"}), 400)