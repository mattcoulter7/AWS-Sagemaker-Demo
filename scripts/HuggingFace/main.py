import requests, json, os

API_URL = "https://runtime.sagemaker.ap-northeast-1.amazonaws.com/endpoints/huggingface-pytorch-inference-2023-01-09-06-08-46-264/invocations"
MY_API_TOKEN = os.getenv("API_TOKEN")

headers = {"Authorization": f"Bearer {MY_API_TOKEN}", "Content-Type": "application/json"}

body=json.dumps({"inputs":[
    "The population of Singapore is 5.6 million people.</s>",
    "The native Ehtnic group of Australia is the Aboriginals.</s>"
]})

response = requests.request("POST", API_URL, headers=headers, data=body)
output = json.loads(response.content.decode("utf-8"))

print(output)