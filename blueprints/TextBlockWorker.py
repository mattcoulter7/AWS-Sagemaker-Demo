import json, os,boto3,sagemaker
from utility.S3Utility import upload_file
from flask import Blueprint,request

text_block_bp = Blueprint('text_block', __name__)

ENDPOINT_NAME_Q = os.getenv("ENDPOINT_NAME_Q")

# PROCESS TEXT BLOCKS -> QUESTION MODEL INPUTS
@text_block_bp.route('/',methods=["POST"])
def handle():
    body = json.loads(request.data)
    # Connections
    text_block_id = body['data']['payload']['text_block']['_id']
    s3_client = boto3.client("s3")
    sess = sagemaker.session.Session()

    # upload the file
    content = body['data']['payload']['text_block']['text']
    payload = {"inputs": content}
    s3_bucket = sess.default_bucket()
    key = f'async_inference_input/{ENDPOINT_NAME_Q}/{text_block_id}.in'

    upload_file(s3_client,payload,s3_bucket,key)

    return {}, 200