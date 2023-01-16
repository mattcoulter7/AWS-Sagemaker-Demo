import json
import boto3
import os
from flask import Blueprint, request
from pathlib import Path

question_bp = Blueprint('question', __name__)

ENDPOINT_NAME_Q = os.getenv("ENDPOINT_NAME_Q")

# PROCESS QUESTION MODEL INPUTS
@question_bp.route('/', methods=["POST"])
def handle():
    try:
        body = json.loads(request.data)
        runtime = boto3.client('runtime.sagemaker')

        for record in body["Records"]:
            bucket = record["s3"]["bucket"]["name"]
            key = record["s3"]["object"]["key"]
            text_block_id = Path(key).stem
            location = f's3://{bucket}/{key}'

            response = runtime.invoke_endpoint_async(
                EndpointName=ENDPOINT_NAME_Q,
                ContentType='application/json',
                InputLocation=location,
                CustomAttributes=json.dumps({
                    'text_block_id': text_block_id
                })
            )

            print(response)

        return {}, 200
    except Exception as e:
        return repr(e), 400
