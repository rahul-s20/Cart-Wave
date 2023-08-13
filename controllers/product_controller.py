from flask import jsonify, make_response, request, Response
from models.products import Products
from utils.helper import filter_objects
from utils.s3.s3_io import S3_Io
from utils.tokenization import decode_token
from os import environ as env


class ProductC:
    def __init__(self):
        self.s3_obj = S3_Io(OVERRIDE_S3_ENDPOINT=env['OVERRIDE_S3_ENDPOINT'], ACCESS_KEY=env['ACCESS_KEY'],
                            SECRET_KEY=env['SECRET_KEY'], REGION=env['REGION'])
        self.product_model = Products()

    def create_product(self, data: dict, token, files):
        try:
            # filter_data = filter_objects(obj=data, fields={"name", "description", "price", "images", "colors", "sizes",
            #                                                "company", "category", "stock", "numberOfReviews", "reviews",
            #                                                "admin"})

            decoded_token = decode_token(token=token)
            all_keys = self.s3_obj.upload_files(uid=decoded_token['sub'], files=files, key='CART_WAVE_DEV/PRODUCTS',
                                                bucket_name=env['BUCKET'],
                                                base_url=env['OBJECT_BASE_URL'])
            return make_response(jsonify({'success': True, 'data': "Product created successfully"}), 200)
        except Exception as er:
            return make_response(jsonify({'success': False, 'data': f"{er}"}), 500)
