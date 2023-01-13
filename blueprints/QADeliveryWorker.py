import json
import sagemaker
from urllib.parse import urlparse
from utility.S3Utility import download_file
from flask import Blueprint

qa_delivery_bp = Blueprint('qa_delivery', __name__)

# PROCESS QUESTION ANSWER MODEL OUTPUTS


@qa_delivery_bp.route('/', methods=["POST"])
def handle(message):
    sess = sagemaker.session.Session()

    output_s3_location = message['responseParameters']['outputLocation']
    o = urlparse(output_s3_location, allow_fragments=False)
    output_bucket = o.netloc
    output_key = o.path.lstrip('/')

    content = download_file(sess, output_bucket, output_key)
    content = json.loads(content)
    # notify complete document

    print(content)

    return {}, 200

if __name__ == '__main__':
    with open('./Boto3/EventDriven/SampleEvents/OutputNotification-S3-QA.json', 'r') as data:
        obj = json.load(data)
        handle(obj)
