import json, os,boto3

ENDPOINT_NAME = os.getenv("ENDPOINT_NAME")

runtime= boto3.client('runtime.sagemaker')

body=json.dumps({"inputs":[
    "The population of Singapore is 5.6 million people.</s>",
    "The native Ethnic group of Australia is the Aboriginals.</s>"
]})

response = runtime.invoke_endpoint(
    EndpointName=ENDPOINT_NAME,
    Body=body,
    ContentType='application/json',
)

response_body = response['Body']
response_str = response_body.read().decode('utf-8')

print(response_str)