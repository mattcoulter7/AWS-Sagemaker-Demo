import json,boto3,os
from flask import Blueprint

question_bp = Blueprint('question', __name__)

ENDPOINT_NAME_Q = os.getenv("ENDPOINT_NAME_Q")

# PROCESS QUESTION MODEL INPUTS
@question_bp.route('/',methods=["POST"])
def handle(message):
    runtime = boto3.client('runtime.sagemaker')
    
    for record in message["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        file_name = key.split('/')
        location = f's3://{bucket}/{key}'

        response = runtime.invoke_endpoint_async(
            EndpointName=ENDPOINT_NAME_Q,
            ContentType='application/json',
            InputLocation=location,
            CustomAttributes={
                'text_block_id':''
            }
        )

        print(response)
    
    return {}, 200

if __name__ == '__main__':
    with open('./Boto3/EventDriven/SampleEvents/InputNotification-S3-Q.json', 'r') as data:
        obj = json.load(data)
        handle(obj)
