@echo off
SET OVERRIDE_S3_ENDPOINT=http://localhost:9000/
SET BUCKET=STARK_DEV
SET ACCESS_KEY=minioadmin
SET SECRET_KEY=minioadmin
SET REGION=ap-south-1
SET OBJECT_BASE_URL=http://localhost:9000/STARK_DEV/CART_WAVE_DEV/PRODUCTS/
SET JWT_SECRET=rsarkar123456
SET MONGODB_URI=mongodb://localhost:27017/cart_wave_dev
SET TIMEZONE=Asia/Kolkata

echo ====================== cart-wave ========================
python run.py