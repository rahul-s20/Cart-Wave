import boto3
from botocore.client import Config
from datetime import datetime
import os
from utils.helper import current_date_time

REQUIRED_ENVS = ['ACCESS_KEY', 'SECRET_KEY', 'REGION']


def warn_and_help(OVERRIDE_S3_ENDPOINT):
    print('', end='\n')
    if OVERRIDE_S3_ENDPOINT is None:
        print(f'Configured to connect to Real S3,'
              f' to connect to Minio, provide environment variable `OVERRIDE_S3_ENDPOINT`', end='\n')
    else:
        print(f'Configured to connect to Fake S3(minio),'
              f' to connect to real S3, remove the environment variable `OVERRIDE_S3_ENDPOINT`', end='\n')
    for en_var in REQUIRED_ENVS:
        if en_var not in os.environ:
            print("Code might not work because {} is not set. Following variables are required: [{}]"
                  .format(en_var, REQUIRED_ENVS))
            return


class S3_Io:
    def __init__(self, OVERRIDE_S3_ENDPOINT=None, ACCESS_KEY=None, SECRET_KEY=None, REGION=None):
        warn_and_help(OVERRIDE_S3_ENDPOINT)
        if OVERRIDE_S3_ENDPOINT is not None:
            self.__s3_client = boto3.client('s3', endpoint_url=OVERRIDE_S3_ENDPOINT, aws_access_key_id=ACCESS_KEY,
                                            aws_secret_access_key=SECRET_KEY, region_name=REGION,
                                            config=Config(signature_version='s3v4'))
            self.__s3_resource = boto3.resource('s3', endpoint_url=OVERRIDE_S3_ENDPOINT, aws_access_key_id=ACCESS_KEY,
                                                aws_secret_access_key=SECRET_KEY, region_name=REGION,
                                                config=Config(signature_version='s3v4'))
        else:
            self.__s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,
                                            region_name=REGION)
            self.__s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,
                                                region_name=REGION)

    def upload_files(self, uid: str, files, key: str, bucket_name: str, base_url: str = ''):
        key_loc, all_keys = list(), ''
        try:
            s3bucket = self.__s3_resource.Bucket(bucket_name)
            if type(files) is list:
                if len(files) > 0:
                    for file in files:
                        ext = get_file_extension(file.filename)
                        file.filename = f"{uid}_{datetime.now().timestamp()}"
                        s3bucket.put_object(Key=f'{key}/{file.filename}.{ext}', Body=file.stream, ACL='public-read',
                                            ContentType="image", ContentDisposition='inline')
                        key_loc.append(f'{key}/{file.filename}.{ext}')
            else:
                ext = get_file_extension(files.filename)
                files.filename = f"{uid}_{current_date_time()}"
                s3bucket.put_object(Key=f'{key}/{files.filename}.{ext}', Body=files.stream, ACL='public-read',
                                    ContentType="image", ContentDisposition='inline')
                key_loc.append(f'{key}/{files.filename}.{ext}')
            all_keys = [f"{base_url + i}" for i in key_loc]
            return all_keys
        except Exception as er:
            print(f"Upload not working: {er}")
            raise er


def get_file_extension(fname: str):
    f_name_analyze = fname.split('.')
    return f_name_analyze[1]
