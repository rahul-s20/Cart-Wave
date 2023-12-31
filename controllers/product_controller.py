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
        try:
            decoded_token = decode_token(token=token)
            if files:
                all_keys = self.s3_obj.upload_files(uid=decoded_token['sub'], files=files, key='CART_WAVE_DEV/PRODUCTS',
                                                    bucket_name=env['BUCKET'],
                                                    base_url=env['OBJECT_BASE_URL'])

            else:
                all_keys = self.s3_obj.upload_files_from_str(uid=decoded_token['sub'], files=data['images'],
                                                             key='CART_WAVE_DEV/PRODUCTS', bucket_name=env['BUCKET'],
                                                             base_url=env['OBJECT_BASE_URL'])
            for i in all_keys:
                objt = Image(public_id=i.split('/')[-1], url=i)
                img_list.append(objt)
            if len(img_list) > 0:
                self.product_model.images = img_list

            for key, value in data.items():
                if key == "colors":
                    value = value.split(',') if isinstance(value, str) else value
                    setattr(self.product_model, key, value)
                elif key == "sizes":
                    value = value.split(',') if isinstance(value, str) else value
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
            print(er)
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
                        for i in data['images']:
                            if not i.__contains__('url'):
                                print("xxxxxxxxxxxxxxxxxxxxxxxxx")
                                print(i)
                                all_keys = self.s3_obj.upload_files_from_str(uid=decoded_token['sub'], files=[i],
                                                                             key='CART_WAVE_DEV/PRODUCTS',
                                                                             bucket_name=env['BUCKET'],
                                                                             base_url=env['OBJECT_BASE_URL'])
                                for j in all_keys:
                                    objt = Image(public_id=j.split('/')[-1], url=j)
                                    img_list.append(objt)
                            else:
                                objt = Image(public_id=i['public_id'], url=i['url'])
                                img_list.append(objt)
                            find_product.images = img_list

                    for key, value in data.items():
                        if key == "colors":
                            value = value.split(',') if isinstance(value, str) else value
                            setattr(find_product, key, value)
                        elif key == "sizes":
                            value = value.split(',') if isinstance(value, str) else value
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
    list_prods = list()

    if curr_users_prv == 'super':
        all_prd = Products.objects()
    elif curr_users_prv in ['moderate', 'low']:
        all_prd = Products.objects(is_active=True)
    else:
        return make_response(jsonify({'success': False, 'data': "Invalid: privilege invalid"}), 400)

    if len(all_prd) > 0:
        for i in all_prd:
            list_prods.append({
                "id": str(i.id),
                "name": i.name,
                "price": i.price,
                "image": i.images[0].url,
                "colors": i.colors,
                "company": i.company,
                "description": i.description,
                "category": i.category,
                "stock": i.stock,
                "shipping": i.shipping,
                "featured": i.featured,

            })

    return make_response(jsonify({'success': True, 'data': list_prods}), 200)


def fetch_single_product(token: str, product_id: str):
    curr_users_prv, _id = check_user_privilege(token=token)

    if curr_users_prv == 'super':
        prd = Products.objects().filter(id=ObjectId(product_id)).first()
    elif curr_users_prv in ['moderate', 'low']:
        prd = Products.objects().filter(Q(id=ObjectId(product_id)) and Q(is_active=True)).first()
    else:
        return make_response(jsonify({'success': False, 'data': "Invalid: privilege invalid"}), 400)

    return make_response(jsonify({'success': False, 'data': prd}), 200)
