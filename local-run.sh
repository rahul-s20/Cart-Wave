
export OVERRIDE_S3_ENDPOINT='http://localhost:9000/'
export BUCKET='STARK_DEV'
export ACCESS_KEY='minioadmin'
export SECRET_KEY='minioadmin'
export REGION='ap-south-1'
export OBJECT_BASE_URL='http://localhost:9000/STARK_DEV/CART_WAVE_DEV/PRODUCTS/'
export JWT_SECRET='rsarkar123456'
export MONGODB_URI='mongodb://localhost:27017/cart_wave_dev'
export TIMEZONE='Asia/Kolkata'

echo -e "====================== cart-wave ========================"
python run.py