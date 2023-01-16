import json, os,boto3,sagemaker,uuid
from urllib.parse import urlparse
from utility.S3Utility import upload_file, download_file
from flask import Blueprint,request

question_processor_bp = Blueprint('question_processor', __name__)

ENDPOINT_NAME_QA = os.getenv("ENDPOINT_NAME_QA")

# PROCESS QUESTION MODEL OUPUTS -> QUESTION ANSWER MODEL INPUTS
@question_processor_bp.route('/',methods=["POST"])
def handle():
    try:
        body = json.loads(request.data)
        # Connections
        s3_client = boto3.client("s3")
        sess = sagemaker.session.Session()
        s3_bucket = sess.default_bucket()
        
        request_parameters = json.loads(body['requestParameters']['customAttributes'])
        text_block_id = request_parameters['text_block_id']

        output_s3_location = body['responseParameters']['outputLocation']
        o = urlparse(output_s3_location, allow_fragments=False)
        output_bucket = o.netloc
        output_key = o.path.lstrip('/')

        output = download_file(sess,output_bucket,output_key)
        output = json.loads(output)
        payload = transform_output_to_input(output)

        input_key = f'async_inference_input/{ENDPOINT_NAME_QA}/{text_block_id}.in'

        upload_file(s3_client,payload,s3_bucket,input_key)
        return {}, 200
    except Exception as e:
        return repr(e), 400

def transform_output_to_input(output):
    inputs = []
    for o in output:
        o_inputs = o['generated_text'].split('<sep> ')
        o_inputs = map(lambda i: f'question: {i} </s>',o_inputs)
        inputs.extend(o_inputs)

    return {'inputs':inputs}