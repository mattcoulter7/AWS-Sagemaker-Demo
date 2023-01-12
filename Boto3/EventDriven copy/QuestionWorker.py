import json,boto3
from ..main_async_q import download_file

# Receives Input from TextBlock
def handle(message):
    runtime = boto3.client('runtime.sagemaker')
    
    for record in message["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        location = f's3://{bucket}/{key}'

        response = runtime.invoke_endpoint_async(
            EndpointName='', # TODO Question Generation Endpoint Name
            ContentType='application/json',
            InputLocation=location
        )

if __name__ == '__main__':
    with open('./Boto3/EventDriven/SampleEvents/InputNotification-S3.json', 'r') as data:
        obj = json.load(data)
        handle(obj)
