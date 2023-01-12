import json, os,boto3,sagemaker
import uuid

from S3Utility import upload_file

ENDPOINT_NAME_Q = os.getenv("ENDPOINT_NAME_Q")

# PROCESS TEXT BLOCKS -> QUESTION MODEL INPUTS
def handle(message):
    # Connections
    s3_client = boto3.client("s3")
    sess = sagemaker.session.Session()

    # upload the file
    content = message['data']['payload']['text_block']['text']
    payload = {"inputs": content}
    s3_bucket = sess.default_bucket()
    key = f'async_inference_input/{ENDPOINT_NAME_Q}/{str(uuid.uuid4())}.in'

    upload_file(s3_client,payload,s3_bucket,key)

if __name__ == '__main__':
    with open('./Boto3/EventDriven/SampleEvents/InputNotification-Kafka.json', 'r') as data:
        obj = json.load(data)
        handle(obj)
