import json, os,boto3,sagemaker,io,time
from urllib.parse import urlparse
from botocore.exceptions import ClientError
import uuid

ENDPOINT_NAME = os.getenv("ENDPOINT_NAME_Q")

# Connections
s3_client = boto3.client("s3")
sess = sagemaker.session.Session()
s3_bucket = sess.default_bucket()
runtime= boto3.client('runtime.sagemaker')

def upload_file(payload):
    payload = json.dumps(payload)
    fo = io.BytesIO(bytes(payload,'UTF-8'))
    key = f'async_inference_input/{ENDPOINT_NAME}/{str(uuid.uuid4())}.in'
    s3_client.upload_fileobj(fo, s3_bucket,key)
    return f's3://{s3_bucket}/{key}'

def download_file(path):
    o = urlparse(path, allow_fragments=True)
    bucket = o.netloc
    key = o.path.lstrip('/')
    file_name = key.split('/')[-1]
    # keep making request until the file is found
    while True:
        try:
            return sess.read_s3_file(bucket=bucket, key_prefix=key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                print("waiting for output...")
                time.sleep(2)
                continue
            raise

def main():
    # 1. Prepare Async Payload via S3
    input_s3_location = upload_file({"inputs":[
        "The population of Singapore is 5.6 million people.</s>",
        "The native Ethnic group of Australia is the Aboriginals.</s>"
    ]})

    # 2. Invoke the payload to the endpoint
    response = runtime.invoke_endpoint_async(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json',
        InputLocation=input_s3_location
    )
    output_s3_location = response['OutputLocation']

    # 3. Read the output from S3
    result = download_file(output_s3_location)
    result = json.loads(result)

    print(result)

if __name__ == '__main__':
    main()