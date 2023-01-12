import json,boto3,os

ENDPOINT_NAME_QA = os.getenv("ENDPOINT_NAME_QA")

# PROCESS QUESTION ANSWER MODEL INPUTS
def handle(message):
    runtime = boto3.client('runtime.sagemaker')
    
    for record in message["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        location = f's3://{bucket}/{key}'

        response = runtime.invoke_endpoint_async(
            EndpointName=ENDPOINT_NAME_QA, 
            ContentType='application/json',
            InputLocation=location
        )

        print(response)

if __name__ == '__main__':
    with open('./Boto3/EventDriven/SampleEvents/InputNotification-S3-QA.json', 'r') as data:
        obj = json.load(data)
        handle(obj)
