import json
import sagemaker
from urllib.parse import urlparse
from utility.S3Utility import download_file
from flask import Blueprint,request

qa_delivery_bp = Blueprint('qa_delivery', __name__)

# PROCESS QUESTION ANSWER MODEL OUTPUTS
@qa_delivery_bp.route('/', methods=["POST"])
def handle():
    body = json.loads(request.data)
    sess = sagemaker.session.Session()

    request_parameters = json.loads(body['requestParameters']['customAttributes'])
    text_block_id = request_parameters['text_block_id']

    output_s3_location = body['responseParameters']['outputLocation']
    o = urlparse(output_s3_location, allow_fragments=False)
    output_bucket = o.netloc
    output_key = o.path.lstrip('/')

    content = download_file(sess, output_bucket, output_key)
    content = json.loads(content)
    # notify complete document

    print(content)

    return {}, 200
