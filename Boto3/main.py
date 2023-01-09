import json, os,boto3

ACCESS_ID = os.getenv("ACCESS_ID")
ACCESS_KEY = os.getenv("ACCESS_KEY")

runtime= boto3.client('runtime.sagemaker',region_name="ap-northeast-1",
    aws_access_key_id=ACCESS_ID,
    aws_secret_access_key= ACCESS_KEY)

body=json.dumps({"inputs":[
    "The population of Singapore is 5.6 million people.</s>",
    "The native Ehtnic group of Australia is the Aboriginals.</s>"
]})

response = runtime.invoke_endpoint(
    EndpointName='huggingface-pytorch-inference-2023-01-09-06-08-46-264',
    Body=body,
    ContentType='application/json',
)

response_body = response['Body']
response_str = response_body.read().decode('utf-8')

print(response_str)