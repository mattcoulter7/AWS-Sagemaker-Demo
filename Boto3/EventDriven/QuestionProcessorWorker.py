import json, os,boto3,sagemaker,uuid
from urllib.parse import urlparse
from S3Utility import upload_file, download_file

ENDPOINT_NAME_QA = os.getenv("ENDPOINT_NAME_QA")

# PROCESS QUESTION MODEL OUPUTS -> QUESTION ANSWER MODEL INPUTS
def handle(message):
    # Connections
    s3_client = boto3.client("s3")
    sess = sagemaker.session.Session()
    s3_bucket = sess.default_bucket()
    
    output_s3_location = message['responseParameters']['outputLocation']
    o = urlparse(output_s3_location, allow_fragments=False)
    output_bucket = o.netloc
    output_key = o.path.lstrip('/')

    output = download_file(sess,output_bucket,output_key)
    output = json.loads(output)
    payload = transform_output_to_input(output)

    input_key = f'async_inference_input/{ENDPOINT_NAME_QA}/{str(uuid.uuid4())}.in'

    upload_file(s3_client,payload,s3_bucket,input_key)

def transform_output_to_input(output):
    inputs = []
    for o in output:
        o_inputs = o['generated_text'].split('<sep> ')
        o_inputs = map(lambda i: f'question: {i} </s>',o_inputs)
        inputs.extend(o_inputs)

    return {'inputs':inputs}


if __name__ == '__main__':
    with open('./Boto3/EventDriven/SampleEvents/OutputNotification-S3-Q.json', 'r') as data:
        obj = json.load(data)
        handle(obj)
